import pandas as pd

def clean_data(df, column):
    # Example: Remove missing values in a column
    df = df.dropna(subset=[column])
    return df

def preprocess_data(df, column):
    # Example: Normalize the column
    df[column] = (df[column] - df[column].mean()) / df[column].std()
    return df
