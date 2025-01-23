################################################
# Functions for CMBD data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 09/12/2024
################################################
import pandas as pd
import numpy as np

def unify_missing_values(df):
    """ Replace various representations of missing values with a unified version."""
    return df.replace([pd.NA, np.nan, 'nan', 'NaN', ''], np.nan)

def most_frequent(group):
    """
    Get the most common label for each group.
    """
    mode = group.mode()
    return mode.iloc[0] if not mode.empty else None


def clean_dataframe(df, entity_name):
    """
    Remove empty rows and duplicates from the dataframe.
    """
    # Replace empty strings with NaN for easier null checks
    df = unify_missing_values(df)

    # Drop empty rows, duplicates, and rows with no significant information
    df = df.dropna(how='all').drop_duplicates()
    if 'episodi_id' in df.columns:
        df = df[df.drop('episodi_id', axis=1).notna().any(axis=1)]
    
    return df


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


def preprocess_file(filepath, column_casts, entity_name):
    """
    General function to read, clean, cast, and return a dataframe.
    """
    try:
        df = pd.read_csv(filepath, sep="|")
    except Exception as e:
        print(f"Error reading {entity_name} file: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

    df = clean_dataframe(df, entity_name)
    df = cast_columns(df, column_casts)
    return df


def process_df(df, entity_name):
    """ General function to preprocess files and make entity-specific adjustments."""
    if entity_name == "Episodis":
        # Convert date columns
        date_cols = ['data_ingres', 'data_alta']
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Extract reference year from data_alta
        if 'data_alta' in df.columns:
            df['any_referencia'] = pd.to_numeric(df['data_alta'].dt.year, errors='coerce')

    elif entity_name in ["Diagnostics", "Procediments"]:
        label_col = 'dx' if entity_name == "Diagnostics" else 'px'
        group_cols = [f"{label_col}_c", f"catalegcim_{label_col}"]
        
        if all(col in df.columns for col in group_cols):
            most_common_label = df.groupby(group_cols)[label_col].agg(most_frequent)
            df[label_col] = df.set_index(group_cols).index.map(most_common_label.to_dict())
    
    return df

def fix_inconsistencies(episodis, df, entity_name):
    """ Detect and filter duplicated diagnostics or procediments from the dataframe."""

    if entity_name not in {"Diagnostics", "Procediments"}:
        raise ValueError("Invalid df_nom value. Choose either 'Diagnostics' or 'Procediments'.")

    # Step 1: Merge episodis_small with the main dataframe `df`
    merged = pd.merge(episodis, df, on="episodi_id", how="right")

    label_col = 'dx' if entity_name == "Diagnostics" else 'px'
    
    # Step 2: Define catalog mapping and filter conditions
    catalog_mapping = {
        "Diagnostics": {"post_2018": "CIM10MC", "pre_2018": "CIM9MC"},
        "Procediments": {"post_2018": "CIM10SCP", "pre_2018": "CIM9MC"}
    }
    catalogs = catalog_mapping[entity_name]

    # Remove duplicates based on year and catalog
    remove_condition = (
        (merged['any_referencia'] >= 2018) & (merged[f'catalegcim_{label_col}'] == catalogs["pre_2018"]) |
        (merged['any_referencia'] < 2018) & (merged[f'catalegcim_{label_col}'] == catalogs["post_2018"])
    )
    filtered_merged = merged[~remove_condition].copy()

    # Step 3: Adjust `episodi_id` for post-2018 records
    update_condition = (
        (filtered_merged['any_referencia'] >= 2018) & 
        (filtered_merged[f'catalegcim_{label_col}'] == catalogs["post_2018"])
    )
    filtered_merged.loc[update_condition, 'episodi_id'] = filtered_merged['episodi_id'].abs()

    # Step 4: Drop episodi-related info
    columns_to_drop = ["codi_p", "any_referencia"]
    filtered_df = filtered_merged.drop(columns=[col for col in columns_to_drop if col in filtered_merged.columns])

    return filtered_df
