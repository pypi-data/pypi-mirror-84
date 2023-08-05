import numpy as np
import torch
from torch import optim, device, cat, rand, ones
from torch.nn import functional

from synthetig.models.CTGAN.transformer import DataTransformer
from synthetig.models.CTGAN.sampler import Sampler
from synthetig.models.CTGAN.models import Generator, Discriminator
from synthetig.models.CTGAN.conditional import ConditionalGenerator


class CTGAN():
    """Main CTGAN model.
    Args:
        embedding_dim (int):
            Size of the random sample passed to the Generator, default = 128.
        gen_dim (tuple or list of int):
            Size of the output samples for each Residual, default = (256, 256).
        dis_dim (tuple or list of int):
            Size of the output samples for each Discriminator layer, a linear layer
            will be created for each value provided, default = (256, 256).
        l2scale (float):
            Weight Decay for Adam Optimiser, default = 1e-6.
        batch_size (int):
            Number of data samples to process in each step.
    Attributes:
        device (bool or str):
            If 'True', use CUDA. If 'str', use indicated device. If 'False', do not use CUDA.
        trained_epochs (int):
            Number of trained epochs.
    """


    def __init__(self, embedding_dim=128, gen_dim=(256, 256), dis_dim=(256, 256),
                 l2scale=1e-6, batch_size=50):
        self.embedding_dim = embedding_dim
        self.gen_dim = gen_dim
        self.dis_dim = dis_dim
        self.l2scale = l2scale
        self.batch_size = batch_size
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.transformer = DataTransformer()

    def _apply_activate(self, data):
        """
        Apply tanh activation function for continuous data and apply gumbel softmax activation
        for discrete data.

        Args:
            data:

        Returns:


        """
        data_t = []
        st = 0
        for item in self.transformer.output_info:
            if item[1] == 'tanh':
                ed = st + item[0]
                data_t.append(torch.tanh(data[:, st:ed]))
                st = ed
            elif item[1] == 'softmax':
                ed = st + item[0]
                data_t.append(functional.gumbel_softmax(data[:, st:ed], tau=0.2))
                st = ed
            else:
                assert 0

        return torch.cat(data_t, dim=1)

    def _cond_loss(self, data, c, m):
        """Calculate conditional loss.
        Args:
            data:
            c:
            m:
        Returns:
            loss
        """

        loss = []
        st = 0
        st_c = 0
        skip = False
        for item in self.transformer.output_info:
            if item[1] == 'tanh':
                st += item[0]
                skip = True

            elif item[1] == 'softmax':
                if skip:
                    skip = False
                    st += item[0]
                    continue

                ed = st + item[0]
                ed_c = st_c + item[0]
                tmp = functional.cross_entropy(
                    data[:, st:ed],
                    torch.argmax(c[:, st_c:ed_c], dim=1),
                    reduction='none'
                )
                loss.append(tmp)
                st = ed
                st_c = ed_c

            else:
                assert 0

        loss = torch.stack(loss, dim=1)

        return (loss * m).sum() / data.size()[0]

    def fit(self, train_data, discrete_columns=tuple(), epochs=300, log_frequency=True):
        """
        Fit the CTGAN Synthesizer models to the training data.

        Args:
            train_data:
            discrete_columns:
            epochs:
            log_frequency:

        Returns:

        """
        # transforming the data
        self.transformer.fit(train_data, discrete_columns)
        train_data = self.transformer.transform(train_data)
        data_dim = self.transformer.output_dimensions
        data_sampler = Sampler(train_data, self.transformer.output_info)

        self.cond_generator = ConditionalGenerator(
            train_data,
            self.transformer.output_info,
            log_frequency
        )

        self.generator = Generator(
            self.embedding_dim + self.cond_generator.n_opt,
            self.gen_dim,
            data_dim
        ).to(self.device)

        self.discriminator = Discriminator(
            data_dim + self.cond_generator.n_opt,
            self.dis_dim
        ).to(self.device)

        self.optimizerG = optim.Adam(
            self.generator.parameters(), lr=2e-4, betas=(0.5, 0.9),
            weight_decay=self.l2scale
        )

        self.optimizerD = optim.Adam(
            self.discriminator.parameters(), lr=2e-4, betas=(0.5, 0.9))


        assert self.batch_size % 2 == 0
        mean = torch.zeros(self.batch_size, self.embedding_dim, device=self.device)
        std = mean + 1

        steps_per_epoch = max(len(train_data) // self.batch_size, 1)

        for trained_epoch in range(epochs):
            for id_ in range(steps_per_epoch):
                fakez = torch.normal(mean=mean, std=std)

                condvec = self.cond_generator.sample(self.batch_size)
                if condvec is None:
                    c1, m1, col, opt = None, None, None, None
                    real = data_sampler.sample(self.batch_size, col, opt)
                else:
                    c1, m1, col, opt = condvec
                    c1 = torch.from_numpy(c1).to(self.device)
                    m1 = torch.from_numpy(m1).to(self.device)
                    fakez = torch.cat([fakez, c1], dim=1)

                    perm = np.arange(self.batch_size)
                    np.random.shuffle(perm)
                    real = data_sampler.sample(self.batch_size, col[perm], opt[perm])
                    c2 = c1[perm]

                fake = self.generator(fakez)
                fakeact = self._apply_activate(fake)

                real = torch.from_numpy(real.astype('float32')).to(self.device)

                if c1 is not None:
                    fake_cat = torch.cat([fakeact, c1], dim=1)
                    real_cat = torch.cat([real, c2], dim=1)
                else:
                    real_cat = real
                    fake_cat = fake

                y_fake = self.discriminator(fake_cat)
                y_real = self.discriminator(real_cat)

                pen = self.discriminator.calc_gradient_penalty(
                    real_cat, fake_cat, self.device)
                loss_d = -(torch.mean(y_real) - torch.mean(y_fake))

                self.optimizerD.zero_grad()
                pen.backward(retain_graph=True)
                loss_d.backward()
                self.optimizerD.step()

                fakez = torch.normal(mean=mean, std=std)
                condvec = self.cond_generator.sample(self.batch_size)

                if condvec is None:
                    c1, m1, col, opt = None, None, None, None
                else:
                    c1, m1, col, opt = condvec
                    c1 = torch.from_numpy(c1).to(self.device)
                    m1 = torch.from_numpy(m1).to(self.device)
                    fakez = torch.cat([fakez, c1], dim=1)

                fake = self.generator(fakez)
                fakeact = self._apply_activate(fake)

                if c1 is not None:
                    y_fake = self.discriminator(torch.cat([fakeact, c1], dim=1))
                else:
                    y_fake = self.discriminator(fakeact)

                if condvec is None:
                    cross_entropy = 0
                else:
                    cross_entropy = self._cond_loss(fake, c1, m1)

                loss_g = -torch.mean(y_fake) + cross_entropy

                self.optimizerG.zero_grad()
                loss_g.backward()
                self.optimizerG.step()

            print("Epoch %d, Loss G: %.4f, Loss D: %.4f" %
                  (trained_epoch + 1, loss_g.detach().cpu(), loss_d.detach().cpu()),
                  flush=True)

    def sample(self, n: int, condition_column=None, condition_value=None):
        """

        Args:
            n:
            condition_column:
            condition_value:

        Returns:

        """

        if condition_column is not None and condition_value is not None:
            condition_info = self.transformer.covert_column_name_value_to_id(
                condition_column, condition_value)
            global_condition_vec = self.cond_generator.generate_cond_from_condition_column_info(
                condition_info, self.batch_size)
        else:
            global_condition_vec = None

        steps = n // self.batch_size + 1
        data = []
        for i in range(steps):
            mean = torch.zeros(self.batch_size, self.embedding_dim)
            std = mean + 1
            fakez = torch.normal(mean=mean, std=std).to(self.device)

            if global_condition_vec is not None:
                condvec = global_condition_vec.copy()
            else:
                condvec = self.cond_generator.sample_zero(self.batch_size)

            if condvec is None:
                pass
            else:
                c1 = condvec
                c1 = torch.from_numpy(c1).to(self.device)
                fakez = torch.cat([fakez, c1], dim=1)

            fake = self.generator(fakez)
            fakeact = self._apply_activate(fake)
            data.append(fakeact.detach().cpu().numpy())

        data = np.concatenate(data, axis=0)
        data = data[:n]

        return self.transformer.inverse_transform(data, None)
