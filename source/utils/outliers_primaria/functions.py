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
    merged_df['trust_year'] = 1909 # First birth year in CORDELIA - CAN BE MODIFIED

    # Convert the date columns to datetime format
    merged_df['data_defuncio'] = pd.to_datetime(merged_df['data_defuncio'], errors='coerce', dayfirst=False, format = "%Y-%m-%d")
    merged_df['data_ingres'] = pd.to_datetime(merged_df['data_ingres'], errors='coerce', dayfirst=False, format = "%Y-%m-%d")
    merged_df['data_alta'] = pd.to_datetime(merged_df['data_alta'], errors='coerce', dayfirst=False, format = "%Y-%m-%d")

    # Apply the first condition: data_ingres can be at most 7 days later than data_defuncio
    condition1 = (merged_df['data_defuncio'].isna()) | (merged_df['data_ingres'] < merged_df['data_defuncio'] + pd.Timedelta(days=7))

    # Apply the second condition: any_referencia >= anaix (cast anaix to int)
    condition2 = merged_df['any_referencia'].astype(int) > merged_df['trust_year']

    # Apply the third condition: data_ingres ha de ser abans que la data_alta
    condition3 = (merged_df['data_alta'].isna()) | (merged_df['data_ingres'] < merged_df['data_alta'])

    # Filter the dataframe based on both conditions
    filtered_df = merged_df[condition1 & condition2 & condition3].copy()

    # Drop the columns 'data_defuncio' and 'anaix'
    filtered_df = filtered_df.drop(['data_defuncio', 'trust_year'], axis=1)

    return filtered_df

def generate_report(df, entity, report_path, preprocessing_df):
    """ If --report is on, a report will be generated in the same outpath."""
    def count_na(df):
        na_counts = df.isna().sum()
        total_rows = len(df)
        for col, na in na_counts.items():
            pct = (na / total_rows) * 100 if total_rows else 0
            f.write(f"  - {col}: {na} ({pct:.2f}%)\n\n")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Report for entity: {entity}\n")
        f.write("-"*50 + "\n")
        f.write(f"Rows before processing: {len(preprocessing_df)}\n")
        f.write(f"Rows after processing: {len(df)}\n\n")

        f.write("Missing values per column (before processing):\n")
        count_na(preprocessing_df)

        f.write("Missing values per column (after processing):\n")
        count_na(df)

        f.write("\nData types:\n")  # Now works with utf-8!
        for col, dtype in df.dtypes.items():
            f.write(f"  - {col}: {dtype}\n")