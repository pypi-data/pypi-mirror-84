import pandas as pd

DEMO_URL = 'http://ctgan-data.s3.amazonaws.com/census.csv.gz'


def load_demo():
    """Load demo data.
    Returns:
        demo data in pandas DataFrame
    """
    return pd.read_csv(DEMO_URL, compression='gzip')
