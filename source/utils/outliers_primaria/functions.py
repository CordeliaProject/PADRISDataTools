# Functions to remove outliers in primaria data
import pandas as pd
from datetime import datetime

def remove_non_coherent_cie(df, cie9_df, cie10_df):
    """ Remove non-existing or non-coherent diagnostics based on CIE-10 standard codes."""
        
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

    return df

def remove_date_outliers(df, mortalitat):
    """ Remove from primaria all those diagnostics that are not possible based on date."""
    # REMOVE NON-COHERENT DATES
    # Step 1: Merge the two dataframes based on 'codi_p' both mortalitat and bd_cordelia
    merged_df = pd.merge(df, mortalitat[['codi_p', 'data_defuncio']], on='codi_p', how='left')

    # Fill NaN values in 'anaix' with a default value (e.g., 1920) before comparison
    merged_df['birth_year'] = pd.NA
    year_minus_100 = datetime.now().year - 100 # Filtering the diagnostics that are possible.
    merged_df['birth_year'] = merged_df['birth_year'].fillna(year_minus_100).astype(int)

    # Convert the date columns to datetime format
    merged_df['data_defuncio'] = pd.to_datetime(merged_df['data_defuncio']).dt.tz_localize(None)
    merged_df['data_ingres'] = pd.to_datetime(merged_df['data_ingres']).dt.tz_localize(None)
    merged_df['data_alta'] = pd.to_datetime(merged_df['data_alta']).dt.tz_localize(None)

    # Apply the first condition: data_ingres can be at most 7 days later than data_defuncio
    condition1 = (merged_df['data_defuncio'].isna()) | (merged_df['data_ingres'] < merged_df['data_defuncio'] + pd.Timedelta(days=7))

    # Apply the second condition: any_referencia >= anaix (cast anaix to int)
    condition2 = merged_df['any_referencia'].astype(int) > merged_df['birth_year']

    # Apply the third condition: data_ingres ha de ser abans que la data_alta
    condition3 = (merged_df['data_alta'].isna()) | (merged_df['data_ingres'] < merged_df['data_alta'])

    # Filter the dataframe based on both conditions
    filtered_df = merged_df[condition1 & condition2 & condition3].copy()

    # Drop the columns 'data_defuncio' and 'anaix'
    filtered_df = filtered_df.drop(['data_defuncio', 'birth_year'], axis=1)

    return filtered_df
