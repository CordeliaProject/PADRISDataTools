################################################
# Functions for measurements data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 16/12/2024
################################################

import pandas as pd
import numpy as np
from utils.ranges import ranges, unitats

def unify_missing_values(df):
    """ Replace various representations of missing values with a unified version."""
    return df.replace([pd.NA, np.nan, 'nan', 'NaN', ''], np.nan)

# Filter dataframe
def filter_by_range(row):
    codi = row['Prova_codi']
    value = row['Prova_resultat']
    valid_range = ranges.get(codi, None)
    if valid_range:
        return valid_range[0] <= value <= valid_range[1]
    return False
        

def process_df(df, codis):
    """ Function to unify missing values, cast columns and correct data formats."""
    # Step 1: Unify missing values
    df = unify_missing_values(df)

    # Step 2: Select only interesting columns
    df = df[df['Prova_codi'].isin(codis.keys())]

    # Step 3: Remove outliers
    df = df[df.apply(filter_by_range, axis = 1)]

    # Step 4: Rename columns to match lab results
    df.rename(columns={"Prova_data": "data", "Prova_resultat": "resultat", "Prova_codi": "codi_prova", "Prova_descripcio":"prova"}, inplace=True)

    # Step 5: Add unitat_mesura column
    df['unitat_mesura'] = df['codi_prova'].map(unitats)

    return df

def export(df, outpath):
    """ Function used to export the data."""
    df.to_csv(outpath, sep = "|", index = False)