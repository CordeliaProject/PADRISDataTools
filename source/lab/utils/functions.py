################################################
# Functions to clean lab data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 10/12/2024
################################################

# This script is not used directly, in here you'll find the functions used to clean lab data from PADRIS
# The data from lab are expected to be quite large so it is handled in chuncks.
# The size of the chunck can be modified.

# ------------------------------------------
# Imports
# ------------------------------------------

import pandas as pd
import string
import re
from .factors import patterns_unitats
from .unit_converter import convert, unit_to_base

def clean_unit(unit):
    """ Using the pattern_unitats dictionary, searches each patterns and transforms the unitat to the corresponding unit """
    if isinstance(unit, str):
        # Remove leading and trailing whitespace
        unit = unit.strip()
        
        # Remove spaces around "/"
        unit = unit.replace(" /", "/").replace("/ ", "/")
        
        # Remove punctuation at the end
        unit = unit.rstrip(string.punctuation.replace("%", ""))

        for pattern, replacement in patterns_unitats.items():
            if re.match(pattern, unit):
                return replacement
    return unit  # Return original unit if no match is found

def preprocessing(chunk):
    """ Pre-process lab data. Basically checks for the correct data format and performs harmonization."""
    # Remove empty lab_resultat
    chunk = chunk.dropna(subset=['lab_resultat'], axis=0)

    # Convert to correct data types:
    chunk = (
        chunk.astype({'Any_prova': 'Int64'})
        .assign(Data_prova=pd.to_datetime(chunk['Data_prova'], errors='coerce').dt.strftime('%d/%m/%Y'))
        .assign(ref_min=pd.to_numeric(chunk['ref_min'].astype(str).str.replace(',', '.'), errors='coerce'))
        .assign(ref_max=pd.to_numeric(chunk['ref_max'].astype(str).str.replace(',', '.'), errors='coerce'))
    )

    # Replace comma with a dot and attempt to convert only numeric-like strings
    chunk['lab_resultat'] = chunk['lab_resultat'].apply(
        lambda x: pd.to_numeric(x.replace(',', '.'), errors='coerce')
        if isinstance(x, str) and x.replace(',', '.').replace('.', '').isdigit() else x
    )

    # Convert to lowercase the unitat_mesura
    chunk['unitat_mesura'] = chunk['unitat_mesura'].apply(lambda x: x.lower() if isinstance(x, str) else x)

    # Apply clean unit to transform to harmonized unit 
    chunk['unitat_mesura'] = chunk['unitat_mesura'].apply(clean_unit)

    return chunk

def add_commons(chunk, label_counts, unit_counts):
    """ Updates label and unit counts and adds columns for the most common label and unit """

    # Group by 'lab_prova_c' to get value counts for 'lab_prova'
    label_counts_per_group = chunk.groupby('lab_prova_c')['lab_prova'].value_counts()

    # Update label_counts dictionary with the aggregated counts
    label_counts_per_group.groupby(level=0).apply(lambda x: label_counts[x.name].update(x.to_dict()))

    # Get the most common 'lab_prova' for each 'lab_prova_c'
    most_common_labels = label_counts_per_group.groupby(level=0).idxmax().apply(lambda x: x[1])

    # If unit_counts is required, process similarly to label_counts
    if unit_counts is not None:
        unit_counts_per_group = chunk.groupby('lab_prova_c')['unitat_mesura'].value_counts()
        unit_counts_per_group.groupby(level=0).apply(lambda x: unit_counts[x.name].update(x.to_dict()))
        most_common_units = unit_counts_per_group.groupby(level=0).idxmax().apply(lambda x: x[1])
        chunk['common_unit'] = chunk['lab_prova_c'].map(most_common_units)
    else:
        most_common_units = None

    # Map the most common labels back to the 'lab_prova' column
    chunk['lab_prova'] = chunk['lab_prova_c'].map(most_common_labels)
    

    return chunk

def processing(df):
    """Processes a DataFrame to convert values from one unit to another."""
    # Make a copy of the DataFrame to avoid modifying the original
    df = df.copy()

    def convert_column(row, column):
        """Helper function to convert a specific column value."""
        try:
            # Check if the value in the column is numeric
            if pd.api.types.is_number(row[column]):
                from_base = unit_to_base(row["unitat_mesura"])
                to_base = unit_to_base(row["common_units"])

                # Skip conversion if units are invalid
                if from_base is None or to_base is None:
                    return row[column]  # Return the original value

                # Perform the unit conversion
                return convert(row[column], row["unitat_mesura"], row["common_units"])
            else:
                return row[column]  # Return the original value
        except (ValueError, TypeError) as e:
            return row[column]  # Return the original value

    # Apply conversions to the relevant columns
    transformable_cols = ["lab_resultat", "ref_min", "ref_max"]
    for column in transformable_cols:
        df[column] = df.apply(lambda row: convert_column(row, column), axis=1)

    return df