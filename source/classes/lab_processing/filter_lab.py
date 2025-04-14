################################################
# Functions to filter lab data
import pandas as pd
import openpyxl

def read_conversion_file(lab_conversion):
    """ Read file with lab variables conversion."""
    if not lab_conversion:
        print("No lab conversion file provided.")
        return None

    try:
        conversion = pd.read_excel(lab_conversion)
        return conversion
    except FileNotFoundError:
        print(f"File not found: {lab_conversion}")


def filter_lab_codi(df, conversion):
    """ Filter lab data based on codi_prova from the conversion file. """
    df = df.copy()

    df = df[df['codi_prova'].isin(list(conversion['codi_prova'].values))]

    return df

def convert_reference_unit(df, conversion, conversion_factors_dict):
    """ Convert units to the reference unit."""

    df = df.copy()
    df = df.rename(columns = {'clean_unit': 'from_unit'}) # Rename the clean_unit column to from_unit

    # Add the reference unit to the lab dataframe
    conversion_short = conversion[['codi_prova', 'to_unit']].drop_duplicates()
    df.loc[:, 'to_unit'] = df['codi_prova'].map(conversion_short.set_index('codi_prova')['to_unit'])

    # Filter to get only numeric results and convert the data type
    df = [df['num_type'] == 'n1']
    df.loc[:, 'clean_result'] = pd.to_numeric(df['clean_result'], errors='coerce')
    
    # Merge the conversion dataframe to get the conversion factors
    conversion_no_group = conversion[['codi_prova', 'from_unit', 'to_unit', 'factor']]
    merged_df = df.merge(conversion_no_group, on=['codi_prova', 'from_unit', 'to_unit'], how='left')
  
    # 1. Add factor when from_unit is equal to to_unit
    merged_df.loc[merged_df['from_unit'] == merged_df['to_unit'], 'factor'] = 1

    # 2. Add factor when it is not in the conversion file but the factor is in the conversion factors dict
    merged_df.loc[merged_df['factor'].isna(), 'factor'] = merged_df.apply(
            lambda row: conversion_factors_dict.get((row['from_unit'], row['to_unit']), pd.NA), axis=1
        )

    # FINAL: Convert the result using the factor
    merged_df['converted_result'] = (merged_df['clean_result'] * merged_df['factor']).round(2)

    # ADD group
    conversion_group = conversion[['codi_prova', 'group']].drop_duplicates()
    result_df = merged_df.merge(conversion_group, on='codi_prova', how='left')
    
    return result_df

def prepare_lab_unified(df):
    """ Prepare the lab data to be output. """
    # Identify the individual identificator col
    id_col = df.columns[0]
    # Select relevant columns
    if 'group' in df.columns:
        df = df[[id_col, 'peticio_id', 'any', 'data', 'codi_prova', 'prova','clean_result', 'from_unit', 'converted_result', 'to_unit', 'group']].copy()
    else:
        df = df[[id_col, 'peticio_id', 'any', 'data', 'codi_prova', 'prova','clean_result', 'from_unit', 'converted_result', 'to_unit']].copy()

    # If there is no unit, converted_result is empty
    df.loc[df['from_unit'].isna(),'converted_result'] = pd.NA
    
    #Rename columns
    df = df.rename(columns = {'from_unit': 'unit', 'to_unit': 'converted_unit'})

    return df

