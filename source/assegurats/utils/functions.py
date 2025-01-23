################################################
# Functions for Assegurats data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 09/12/2024
################################################

import pandas as pd
import numpy as np
from utils.casts import casts

def unify_missing_values(df):
    """ Replace various representations of missing values with a unified version."""
    return df.replace([pd.NA, np.nan, 'nan', 'NaN', ''], np.nan)

def cast_columns(df, column_casts):
    """
    Safely cast dataframe columns to specified types.
    """
    for col, dtype in column_casts.items():
        try:
            df[col] = df[col].astype(dtype)
        except Exception as e:
            print(f"Warning: Failed to convert column '{col}' to '{dtype}': {e}")
    return df

def process_df(df, column_casts):
    """ Function to unify missing values, cast columns and correct data formats."""
    # Step 1: Unify missing values
    df = unify_missing_values(df)

    # Step 2: Convert columns to correct data type
    df = cast_columns(df, column_casts)

    # Convert also 'Data_defuncio' to date
    df['data_defuncio'] = pd.to_datetime(df['data_defuncio'], errors='coerce')

    # Step 3. Generate a new column for the year based on 'Data_defuncio'
    df['any_defuncio'] = df['data_defuncio'].dt.year
    df = df.astype({
        'any_defuncio': 'Int64',})
    
    return df

def export(df, outpath):
    """ Function used to export the data."""
    df.to_csv(outpath, sep = "|", index = False)