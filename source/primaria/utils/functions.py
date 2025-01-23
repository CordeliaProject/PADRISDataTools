################################################
# Functions to clean problemes salut a primaria
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 16/01/2024
################################################
import pandas as pd
import numpy as np
from utils.casts import casts

def unify_missing_values(df):
    """ Replace various representations of missing values with a unified version."""
    return df.replace([pd.NA, np.nan, 'nan', 'NaN', ''], np.nan)
        
def rename_columns(df):
    """ Rename columns from the dataframe to get same variables as in CMBD"""
    df = df.rename(columns={'any_problema_salut':'any_referencia','data_problema_salut': 'data_ingres', 'data_problema_salut_baixa': 'data_alta', 'catalegcim_problema_salut_c': 'catalegcim_dx', 'problema_salut_c': 'dx_c', 'problema_salut': 'dx'})

    return df

def process_df(df):
    """ Function to unify missing values, cast columns and correct data formats."""
    # Step 1: Unify missing values
    df = unify_missing_values(df)
    # Ensure rows where there is no information about the problema_salut or data_problema_salut are removed
    df = df.dropna(subset=['problema_salut', 'problema_salut_c', 'data_problema_salut'])

    # Step 2: Get columns in the correct format
    for column, dtype in casts.items():
        if dtype == 'datetime64[ns]':
            # Convert to datetime using pd.to_datetime
            df[column] = pd.to_datetime(df[column], errors='coerce')
        else:
            # Apply other types
            df[column] = df[column].astype(dtype)

    # Step 3: Rename columns
    df = rename_columns(df)

    # Step 4: Replace values in the 'catalegcim' column
    df['catalegcim_dx'] = df['catalegcim_dx'].replace({
        'CIM-10-MC': 'CIM10MC',
    })

    # Step 5: Order by codi_p
    df = df.sort_values("codi_p")

    return df

def remove_outliers(df):
    """ Function to remove non-existing diagnostics or diagnostics done when people were death."""
    # Import data
    bd_cordelia = pd.read_csv(r"U:\Estudis\B52_CORDELIA\Dades\PADRIS\01_BD_PADRIS_clean\bd_cordelia_20240503_OK_V1.csv", sep = "|", usecols=['codi_p', 'anaix']) 
    mortalitat = pd.read_csv(r"U:\Estudis\B52_CORDELIA\Dades\PADRIS\01_BD_PADRIS_clean\Mortalitat.csv", sep = "|", usecols=['codi_p', 'data_defuncio'])

    # Read the reference for CIM10 and CIM9
    cie10_df = pd.read_excel(r"U:\Estudis\B52_CORDELIA\Analisis\PADRIS\utils\referencies_cie\Diagnosticos_ES2024_TablaReferencia_30_06_2023.xlsx", sheet_name='ES2024 Finales', usecols=['Código'])
    cie9_df = pd.read_excel(r"U:\Estudis\B52_CORDELIA\Analisis\PADRIS\utils\referencies_cie\CIE9MC_9_2014_REF_20210601_2362183957514564327.xls", sheet_name='cie9mc2014', usecols=['Tab.D'])

    # REMOVE NON-EXISTING CIM-10 AND CIM-9
    # Step 1: Prepare the reference dataframes to be used
    # For CIE9 dataframe
    cie9_df.rename(columns={"Tab.D": "codi"}, inplace=True)
    # For CIE10 dataframe
    cie10_df.rename(columns={"Código": "codi"}, inplace=True)

    # Display the first few rows to understand the structure of the dataframe
    cie10_df['codi'] = cie10_df['codi'].str.replace('.', '', regex=False)
    cie9_df['codi'] = cie9_df['codi'].str.replace('.', '', regex=False)

    # Step 2: Prepare the DX_C column
    df['dx_c'] = df['dx_c'].str.replace('-', '', regex=False)

    # Step 3:  Update 'catalegcim' to "CIM10MC" where 'problema_salut_c' exists in CIE10 dataframe
    df.loc[
        (df['catalegcim_dx'] == 'CIM10') & 
        (df['dx_c'].isin(cie10_df['codi'])),
        'catalegcim_dx'
    ] = 'CIM10MC'

    # Step 4: Update 'catalegcim' to "CIM9MC" where 'problema_salut_c' exists in CIE9 dataframe
    df.loc[
        (df['catalegcim_dx'] == 'CIM10') & 
        (df['dx_c'].isin(cie9_df['codi'])),
        'catalegcim_dx'
    ] = 'CIM9MC'

    # Step 5: Remove all those problemes in which catalegcim != CIM10MC or CIM9MC
    df = df[df['catalegcim_dx'].isin(["CIM10MC", "CIM9MC"])]

    # REMOVE NON-COHERENT DATES
    # Step 1: Merge the two dataframes based on 'codi_p' both mortalitat and bd_cordelia
    merged_df = pd.merge(df, mortalitat[['codi_p', 'data_defuncio']], on='codi_p', how='left')
    merged_df = pd.merge(merged_df, bd_cordelia[['codi_p', 'anaix']], on='codi_p', how='left')

    # Fill NaN values in 'anaix' with a default value (e.g., 1920) before comparison
    merged_df['anaix'] = merged_df['anaix'].fillna(1920).astype(int)

    # Convert the date columns to datetime format
    merged_df['data_defuncio'] = pd.to_datetime(merged_df['data_defuncio'], format='%d/%m/%Y').dt.tz_localize(None)
    merged_df['data_ingres'] = pd.to_datetime(merged_df['data_ingres'], format='%d/%m/%Y').dt.tz_localize(None)
    merged_df['data_alta'] = pd.to_datetime(merged_df['data_alta'], format='%d/%m/%Y').dt.tz_localize(None)
    # Apply the first condition: data_ingres can be at most 7 days later than data_defuncio
    condition1 = (merged_df['data_defuncio'].isna()) | (merged_df['data_ingres'] < merged_df['data_defuncio'] + pd.Timedelta(days=7))

    # Apply the second condition: any_referencia >= anaix (cast anaix to int)
    condition2 = merged_df['any_referencia'].astype(int) > merged_df['anaix'].astype(int)

    # Apply the third condition: data_ingres ha de ser abans que la data_alta
    condition3 = (merged_df['data_alta'].isna()) | (merged_df['data_ingres'] < merged_df['data_alta'])

    # Filter the dataframe based on both conditions
    filtered_df = merged_df[condition1 & condition2 & condition3].copy()

    # Drop the columns 'data_defuncio' and 'anaix'
    filtered_df.drop(['data_defuncio', 'anaix'], axis=1, inplace=True)

    return filtered_df

def export(df, outpath):
    """ Function used to export the data."""
    df.to_csv(outpath, sep = "|", index = False)