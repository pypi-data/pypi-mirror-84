import json
import numpy as np
import pandas as pd


def read_csv(path_csv, path_metadata=None, header=True, discrete=None):
    """Read data in CSV format.
    Args:
        path_csv (str):
            path of CSV, compulsory.
        path_metadata (str):
            path of meta data, default = None
        header (bool):
            whether columns have headers, default = True
        discrete (str):
            whether the values in a column are discrete
    Returns:
        data (pandas.DataFrame):
            data in pandas DataFrame
        discrete_columns (list):
            list of discrete columns from data
    """
    
    data = pd.read_csv(path_csv, header="infer" if header else None)

    if path_metadata:
        with open(path_metadata) as meta_file:
            metadata = json.load(meta_file)
        discrete_columns = [
            column['name']
            for column in metadata['columns']
            if column['type'] != 'continuous'
        ]
    elif discrete:
        discrete_columns = discrete.split(",")
        if not header:
            discrete_columns = [int(i) for i in discrete_columns]
    else:
        discrete_columns = []

    return data, discrete_columns
