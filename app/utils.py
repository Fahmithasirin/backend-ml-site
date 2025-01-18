import pandas as pd

def clean_data(df, column):
    df = df.dropna(subset=[column])
    return df

def preprocess_data(df, column):
    df[column] = (df[column] - df[column].mean()) / df[column].std()
    return df
