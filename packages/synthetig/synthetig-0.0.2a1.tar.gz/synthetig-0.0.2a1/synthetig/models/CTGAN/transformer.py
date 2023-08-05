import pickle
import numpy as np
import pandas as pd

from sklearn.exceptions import ConvergenceWarning
from sklearn.mixture import BayesianGaussianMixture
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils.testing import ignore_warnings


class DataTransformer():
    """Data transformer. Model continuous columns with a Bayesian GMM and normalise
    to a scalar [0,1] and a vector. Discrete columns are encoded using a scikit-learn
    one hot encoder.
    Args:
        n_clusters (int): number of modes.
        epsilon (float): epsilon value.
    """

    def __init__(self, n_clusters: int = 10, epsilon: int = 0.005):
        """

        Args:
            n_clusters:
            epsilon:
        """
        self.n_clusters = n_clusters
        self.epsilon = epsilon
        self.output_info = []
        self.output_dimensions = 0




    def fit(self, data: pd.DataFrame, discrete_columns: object = tuple()) -> None:
        """
        creates a meta object that has a dic for each of the columns of the data with keys, values give info
        other functions to create the encodings
        Args:
            data:
            discrete_columns:
        """

        self.dtypes = data.infer_objects().dtypes
        self.meta = []
        for column in data.columns:
            column_data = data[[column]].values
            if column in discrete_columns:
                meta = self._fit_discrete(column, column_data)
            else:
                meta = self._fit_continuous(column, column_data)

            self.output_info += meta['output_info']
            self.output_dimensions += meta['output_dimensions']
            self.meta.append(meta)

    def _fit_discrete(self, column, data):
        """Encode discrete columns using a scikit-learn one hot encoder.
        Args:
            column: the name of the column
            data: a list of list of the values of the named column
        Returns:
            A dict mapping keys to the corresponding value for the column
            the rows are represented as a tuple of strings. For
            example:


            {'name': 'relationship',
            'encoder': OneHotEncoder(sparse=False),
            'output_info': [(6, 'softmax')],
            'output_dimensions': 6}

        """
        one_hot = OneHotEncoder(sparse=False)
        one_hot.fit(data)
        categories = len(one_hot.categories_[0])

        return {
            "name": column,
            "encoder": one_hot,
            "output_info": [(categories, "softmax")],
            "output_dimensions": categories
        }

    @ignore_warnings(category=ConvergenceWarning)
    def _fit_continuous(self, column, data):
        """Model continuous columns with a Bayesian GMM and normalise to a scalar [0,1]
        and a vector.
        Args:
            column: the name of the column
            data: a list of list of the values of the named column
        Returns:
            {'name': 'age',
             'model': BayesianGaussianMixture(n_components=10,weight_concentration_prior=0.001),
             'components':array([ True,  True,  True,  True,  True,  True,  True,  True,  True,True]),
             'output_info': [(1, 'tanh'), (10, 'softmax')],
             'output_dimensions': 11}


        """
        gaussian_model = BayesianGaussianMixture(
            self.n_clusters,
            weight_concentration_prior_type='dirichlet_process',
            weight_concentration_prior=0.001,
            n_init=1
        )
        gaussian_model.fit(data)
        components = gaussian_model.weights_ > self.epsilon
        num_components = components.sum()

        return {
            "name": column,
            "model": gaussian_model,
            "components": components,
            "output_info": [(1, "tanh"), (num_components, "softmax")],
            "output_dimensions": 1 + num_components
        }


    def transform(self, data: pd.DataFrame):
        """

        Args:
            data:

        Returns:
            An array of the transform data.
        """
        values = []

        for meta in self.meta:
            column_data = data[[meta['name']]].values
            if 'model' in meta:
                values += (self._transform_continuous(meta, column_data))
            else:
                values.append(self._transform_discrete(meta, column_data))

        return np.concatenate(values, axis=1).astype(float)


    def _transform_continuous(self, column_meta, data):
        """

        Args:
            column_meta: the meta data for the given column
            data: the value for the given column

        Returns:
            a list for the features probs_onehot this is talked about in the paper

        """
        components = column_meta["components"]
        model = column_meta["model"]

        means = model.means_.reshape((1, self.n_clusters))
        stds = np.sqrt(model.covariances_).reshape((1, self.n_clusters))
        features = (data - means) / (4 * stds)

        probs = model.predict_proba(data)

        n_opts = components.sum()
        features = features[:, components]
        probs = probs[:, components]

        opt_sel = np.zeros(len(data), dtype="int")
        for i in range(len(data)):
            pp = probs[i] + 1e-6
            pp = pp / pp.sum()
            opt_sel[i] = np.random.choice(np.arange(n_opts), p=pp)

        idx = np.arange((len(features)))
        features = features[idx, opt_sel].reshape([-1, 1])
        features = np.clip(features, -.99, .99)

        probs_onehot = np.zeros_like(probs)
        probs_onehot[np.arange(len(probs)), opt_sel] = 1
        return [features, probs_onehot]

    def _transform_discrete(self, column_meta, data):
        """
            Transform data using one-hot encoding give in the meta dict.

        Args:
            column_meta: meta object for the give column
            data: a List of the data for the give column

        Returns:
            A Sparse matrix

        """
        encoder = column_meta['encoder']
        return encoder.transform(data)

    def inverse_transform(self, data, sigmas):
        start = 0
        output = []
        column_names = []
        for meta in self.meta:
            dimensions = meta['output_dimensions']
            columns_data = data[:, start:start + dimensions]

            if 'model' in meta:
                sigma = sigmas[start] if sigmas else None
                inverted = self._inverse_transform_continuous(
                    meta, columns_data, sigma)
            else:
                inverted = self._inverse_transform_discrete(meta, columns_data)

            output.append(inverted)
            column_names.append(meta['name'])
            start += dimensions

        output = np.column_stack(output)
        output = pd.DataFrame(output, columns=column_names).astype(self.dtypes)

        return output


    def _inverse_transform_continuous(self, meta, data, sigma):
        model = meta['model']
        components = meta['components']

        u = data[:, 0]
        v = data[:, 1:]

        if sigma is not None:
            u = np.random.normal(u, sigma)

        u = np.clip(u, -1, 1)
        v_t = np.ones((len(data), self.n_clusters)) * -100
        v_t[:, components] = v
        v = v_t
        means = model.means_.reshape([-1])
        stds = np.sqrt(model.covariances_).reshape([-1])
        p_argmax = np.argmax(v, axis=1)
        std_t = stds[p_argmax]
        mean_t = means[p_argmax]
        column = u * 4 * std_t + mean_t

        return column

    def _inverse_transform_discrete(self, meta, data):
        encoder = meta['encoder']
        return encoder.inverse_transform(data)



    def covert_column_name_value_to_id(self, column_name, value):
        discrete_counter = 0
        column_id = 0
        for info in self.meta:
            if info["name"] == column_name:
                break
            if len(info["output_info"]) == 1:  # is discrete column
                discrete_counter += 1
            column_id += 1

        return {
            "discrete_column_id": discrete_counter,
            "column_id": column_id,
            "value_id": np.argmax(info["encoder"].transform([[value]])[0])
        }
