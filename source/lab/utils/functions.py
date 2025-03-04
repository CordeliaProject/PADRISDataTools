################################################
# Functions to clean lab data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 03/02/2024
################################################

import re
import pandas as pd
import numpy as np

# -----------------------------------------
# ----- General functions
def standardize_number(value):
    """ Standardizes the format of numeric values in the lab data."""
    if not isinstance(value, str):
        return value  # If value is not a string, return it as is

    # Step 1: Apply specific rules for Spanish-formatted numbers.
    # Mask 1: Remove commas in strings with two or more commas
    if re.search(r'\d{1,3},0{3},0{3}', value):  # Matches '1,000,000' or similar
        value = re.sub(r',', '', value)

    # Mask 2: Remove commas in '10,000' or '100,000'
    elif re.search(r'10{1,2},000', value):  # Matches '10,000' or '100,000'
        value = re.sub(r',', '', value)

    # Mask 3: Adjust values like ',1234' to '0,1234'
    if value.startswith(',') or value.startswith('.'):
        value = '0' + value  # Convert to 0.xxxx format

    # Step 2: Transform commas to dots for decimal numbers (e.g., '1,23' -> '1.23')
    value = re.sub(r',', '.', value)

    # Step 3: Remove leading zeros unless it's a decimal (e.g., '01.23' -> '1.23')
    value = re.sub(r'^0+(\d)', r'\1', value)  # Remove leading zeros before digits
    value = re.sub(r'^0+(\.\d+)', r'0\1', value)  # Ensure '0.' is kept for decimals

    # Step 4: Round to 4 decimals
    if '.' in value:
        value = re.sub(r'(\.\d{4})\d+', r'\1', value)  # Keep up to 3 decimal places
        value = value.rstrip('0').rstrip('.')  # Remove trailing zeros and possibly the decimal point

    return value

def standardize_n2(value):
    """ Standardizes the format of numeric values of num_type n2 in the lab data."""
    # Ensure there are no spaces in the value
    value = re.sub(r" ", "", value)

    # Step 1: Extract the non numerical parts:
    non_numerical = re.findall("[<>=]", value)
    numerical = re.sub("[<>=]", "", value)

    # Step 2: Standardize numbers
    standardized_value = list(standardize_number(numerical))

    # Add all together and generate the result
    result = non_numerical + standardized_value
    result = "".join(result)
    
    return result

def unify_missing_values(df):
    """ Standardizes missing values in lab data """
    return df.replace([pd.NA, np.nan, 'nan', 'NaN', ''], pd.NA)


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

# -----------------------------------------
# ----- Step 1: Clear typos
def clear_typos(df):
    """Initial data cleaning by removing typographical errors and extraneous characters from the result values."""
    # Apply the cleaning steps to the specified column
    df["clean_result"] = df["lab_resultat"].apply(lambda x: re.sub(r'[!#$&\'();?@_`{|}~"\[\]]', '', x))  # Remove special characters
    df["clean_result"] = df["clean_result"].apply(lambda x: re.sub(r'^=|=$', '', x))  # Remove leading and trailing equal signs
    df["clean_result"] = df["clean_result"].apply(lambda x: re.sub(r'^\s+|\s+$', '', x))  # Remove leading/trailing spaces
    df["clean_result"] = df["clean_result"].apply(lambda x: re.sub(r'^\t+|\t+$', '', x))  # Remove leading/trailing tabs

    return df

# -----------------------------------------
# ----- Step 2: Handle extra variables in the result
def handle_extra_variables(df, patterns_common_words, numeric_patterns, report=False):
    """Cleans df['clean_result'] by handling flags, units, and interpretative comments."""
    # Ensure 'comentari' column exists:
    if 'comentari' not in df.columns:
        df['comentari'] = pd.NA

    def add_cleaning_comment(mask, comment):
        """Helper function to add a cleaning comment."""
        # Only update rows where the comment is not already present
        df.loc[mask, 'comentari'] = df.loc[mask, 'comentari'].apply(
            lambda x: f"{x}, {comment}".strip(', ') if pd.notna(x) and comment not in x else comment if pd.isna(x) else x
        )

    # Step 1: Handle interpretative flags (positive, negative, normal, etc.)
    for flag, patterns in patterns_common_words.items():
        for pattern in patterns:
            # Use str.extract to directly capture matching groups
            mask_literal = df['clean_result'].str.contains(pattern, na=False, flags=re.IGNORECASE, regex=True) # Filter dataframe to only include rows where the pattern is found

            # Update the cleaning_comments column for affected rows
            add_cleaning_comment(mask_literal, 'literal')

            # Apply the replacement to the clean_result column only for rows that match the pattern
            df.loc[mask_literal, 'clean_result'] = flag
    # Handle all those cases in which there are no numeric values but are not already flagged as literal
    mask_else_literal = (df["comentari"].isna()) & (df['clean_result'].str.match(r'^[a-zA-Z]+$', na=False)) # Filter dataframe to only include rows where the pattern is found
    add_cleaning_comment(mask_else_literal, 'literal') # Add a comment to the 'comentari' column.

    # Step 2: Handle units and flags adjacent to numbers
    adjacent_units1 = r'^(' + numeric_patterns['n1'] + r')\s*(' + numeric_patterns['units']  + r')$'
    adjacent_units2 = r'^(' + numeric_patterns['units'] + r')\s*(' + numeric_patterns['n1'] + r')$'

    # Case 1: Units after the result
    mask_units_after = df['clean_result'].str.contains(adjacent_units1, na=False, flags=re.IGNORECASE, regex=True) #Filter dataframe to only include rows where the pattern is found.
    unit_extracted = df.loc[mask_units_after, 'clean_result'].str.extract(adjacent_units1) # Extract parts from the matched string.
    add_cleaning_comment(mask_units_after, 'units') # Add a comment to the 'comentari' column.
    df.loc[mask_units_after, 'clean_result'] = df.loc[mask_units_after, 'clean_result'].str.replace(
        adjacent_units1, r'\1', flags=re.IGNORECASE, regex=True
    ) # Replace the matched string with the first group of the extracted string.
    
    # Fix: Use str.extract to get the correct unit for unitat_mesura
    df.loc[mask_units_after, 'unitat_mesura'] = unit_extracted[2] # Assign the third group of the extracted string to the 'unitat_mesura' column.

    # Case 2: Units before the result
    mask_units_before = df['clean_result'].str.contains(adjacent_units2, na=False, flags=re.IGNORECASE, regex=True) #Filter dataframe to only include rows where the pattern is found.
    unit_extracted = df.loc[mask_units_before, 'clean_result'].str.extract(adjacent_units2) # Extract parts from the matched string.
    add_cleaning_comment(mask_units_before, 'units') # Add a comment to the 'comentari' column.
    df.loc[mask_units_before, 'clean_result'] = df.loc[mask_units_before, 'clean_result'].str.replace(
        adjacent_units2, r'\2', flags=re.IGNORECASE, regex=True
    ) # Replace the matched string with the first group of the extracted string
    
    # Fix: Use str.extract to get the correct unit for unitat_mesura
    df.loc[mask_units_before, 'unitat_mesura'] = unit_extracted[0]

    # Step 3: Handle positive
    for sign, _ in [("\\+", "positive")]:
        pattern = rf"^{sign}\s*({numeric_patterns['n1']})$" # Define the pattern to match.
        mask_sign = df['clean_result'].str.contains(pattern, na=False, regex=True) # Filter dataframe to only include rows where the pattern is found.
        add_cleaning_comment(mask_sign, 'flag') # Add a comment to the 'comentari' column.
        df.loc[mask_sign, 'clean_result'] = df.loc[mask_sign, 'clean_result'].str.replace(
            pattern, r'\1', regex=True
        ) # Replace the matched string with the first group of the extracted string.

    # Step 4: Handle percent
    percent_pattern = rf"^({numeric_patterns['n1']}) *(%)$" # Define the pattern to match.
    mask_percent = df['clean_result'].str.contains(percent_pattern, na=False, regex=True) # Filter dataframe to only include rows where the pattern is found.
    percent_result = df.loc[mask_percent, 'clean_result'].str.extract(percent_pattern) # Extract parts from the matched string.
    add_cleaning_comment(mask_percent, 'percent')
    df.loc[mask_percent, 'clean_result'] = df.loc[mask_percent, 'clean_result'].str.replace(
        percent_pattern, r'\1', regex=True
    ) # Replace the matched string with the first group of the extracted string.
    df.loc[mask_percent, 'unitat_mesura'] = percent_result[2]

    # Step 5: Handle exponents
    exponent_pattern = rf"^({numeric_patterns['exponent']})$" # Define the pattern to match.
    mask_exponent = df['clean_result'].str.contains(exponent_pattern, na=False, regex=True) # Filter dataframe to only include rows where the pattern is found.
    add_cleaning_comment(mask_exponent, 'exponents') # Add comment
    # Extract base number and exponent separately
    extracted = df.loc[mask_exponent, 'clean_result'].str.extract(exponent_pattern)
    # Apply standardization to the base number (n1)
    df.loc[mask_exponent, 'clean_result'] = extracted[0].apply(standardize_number) + extracted[2] # Clean the number and add the exponent
    
    # Clean up stray characters from exponents
    #df['clean_result'] = df['clean_result'].str.replace(r"[\*\^]", "", regex=True)

    # Reporting
    if report:
        flagged_records = df['comentari'].notna().sum()
        flagged_percent = flagged_records / len(df) * 100 if len(df) > 0 else 0
        print(f"{flagged_records} records flagged ({flagged_percent:.2f}% of total).")

    return df

# -----------------------------------------
# ----- Step 3: Classify the numeric result
def classify_numeric_results(df,  numeric_patterns):
    """ Classifies numeric results into n1, n2, n3, and n4 scales based on patterns."""
    # Ensure 'comentari' column exists:
    if 'num_type' not in df.columns:
        df['num_type'] = pd.NA

    # Step 1: Assign n1 scale type for inequality patterns
    df['num_type'] = df['num_type'].where(
        (~df['clean_result'].astype(str).str.match(f"^{numeric_patterns['n1']}$")) | (df['comentari'] == "exponents"), "n1")
    
    # Step 2: Assign n2 scale type for inequality patterns
    df['num_type'] = df['num_type'].where(
        ~df['clean_result'].astype(str).str.match(f"^{numeric_patterns['n2']}$"), "n2")
    
    # Step 3: Assign n3 for range patterns separated by hypens
    df['num_type'] = df['num_type'].where(
        ~df['clean_result'].astype(str).str.match(f"^{numeric_patterns['n3']}$"), "n3")

    # Step 4: Assign n4 for titer patterns. When a number is divided by a second integer. Separated by ":" or "/"
    df['num_type'] = df['num_type'].where(
        ~df['clean_result'].astype(str).str.match(f"^{numeric_patterns['n4']}$"), "n4")

    return df

# -----------------------------------------
# ----- Step 4: Standardize numeric results based in classification
def standardize_numeric_results(df, report=False):
    """ Standardizes the lab data by cleaning the result values and assigning scale types."""
    def report_num_type(df, num_type):
        """ Function to report the number and percentage of records assigned to a given scale type"""
        # Filter records by scale type
        scale_records = df[df['num_type'] == num_type]
        
        # Calculate the number of records
        scale_records_n = len(scale_records)
        
        # Calculate the percentage of total records
        total_n_records = len(df)
        scale_records_percent = (scale_records_n / total_n_records * 100) if total_n_records else np.nan
        
        # Report the results
        print(f"{scale_records_n} result records of scale type '{num_type}' ({scale_records_percent:.2f}%).")

    # Step 1: Harmonize n1 results.
    mask_n1 = df['num_type'] == 'n1' # Create a mask for the conditions
    df.loc[mask_n1, 'clean_result'] = df.loc[mask_n1, 'clean_result'].apply(standardize_number) # Apply transformation using the mask (vectorized)

    # Step 2: Harmonize n2, n3, n4 results.
    # Create the mask for the conditions
    num_types = ['n2', 'n3', 'n4']

    for num_type in num_types:
        mask = df['num_type'] == num_type
        # Apply transformation using the mask (vectorized)
        df.loc[mask, 'clean_result'] = df.loc[mask, 'clean_result'].apply(
            lambda x: re.sub(r" ", "", re.sub(r"/", ":", x))
        )
        if num_type == 'n2':
            # Apply the specific transformation for n2
            df.loc[mask, 'clean_result'] = df.loc[mask, 'clean_result'].apply(standardize_n2)
    
    # Step 3: Check that n3 results are plausible: first number must be lower than second.
    mask_n3 = df['num_type'] == 'n3'
    # Extract the first and second numbers using vectorized string methods for 'n3' rows
    df.loc[mask_n3, 'first_number'] = df.loc[mask_n3, 'clean_result'].str.extract(r"^([0-9]+)-")[0].apply(standardize_number)
    df.loc[mask_n3, 'second_number'] = df.loc[mask_n3, 'clean_result'].str.extract(r"-([0-9]+)$")[0].apply(standardize_number)

    # Convert the extracted values to numeric, replacing non-numeric entries with NaN
    df['first_number'] = pd.to_numeric(df['first_number'], errors='coerce')
    df['second_number'] = pd.to_numeric(df['second_number'], errors='coerce')

    # Remove scale type where the second number is lower than the first
    df.loc[mask_n3 & (df['second_number'] < df['first_number']), 'num_type'] = pd.NA

    # Drop temporary columns 'first_number' and 'second_number'
    df = df.drop(columns=['first_number', 'second_number'])

    
    # Reporting numbers of records assigned to each number type
    if report:
        for num_type in ['n1', 'n2', 'n3', 'n4']:
            report_num_type(df, num_type)

    return df


# -----------------------------------------
# ----- Step 5: Standardize unit.
def standardize_unit(df, unit_patterns, report = False):
    """ Standardizes the format of units in the lab data."""
    df = df.copy()
    total_n_records = len(df)
    # Ensure "clean_unit" column exists.
    if "clean_unit" not in df.columns:
        df["clean_unit"] = df["unitat_mesura"]
        df['comentari_unitat'] = pd.NA
    
    # For each unit in the unit_patterns dictionary, if it is found in the "unitat_mesura" column, replace it with the corresponding key.
    for unit, pattern in unit_patterns.items():
        mask = (df["clean_unit"].str.contains(pattern, na = False, flags = re.IGNORECASE, regex = True) & df['comentari_unitat'].isna()) # Filter dataframe to only include rows where the pattern is found.
        df.loc[mask, "clean_unit"] = unit # Replace the unit with the standardized unit.
        df.loc[mask, "comentari_unitat"] = "done" # Add a comment to the 'comentari_unitat' column.

    if report:
        n_units_standardized = len(df[df['comentari_unitat'] == "done"]) # Calculate the number of rows with standardized units.
        scale_records_percent = (n_units_standardized / total_n_records * 100) if total_n_records else np.nan # Calculate the percentage of total records.
        print(f"{n_units_standardized} rows with standardized units ({scale_records_percent:.2f}%).")

    return df

# -----------------------------------------
# ----- Step 5: Standardize test name for each code.
def standardize_name(df):
    """ The same lab test code can have multiple literals, we are going to keep only the most common one."""
    df['lab_prova'] = df.groupby('lab_prova_c')['lab_prova'].transform(lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0])

    return df