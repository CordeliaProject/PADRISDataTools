################################################
# Functions to clean lab data

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
    if re.match(r'^[,\.]\d+', value):
        value = '0' + value.replace(',', '.')

    # Step 2: Transform commas to dots for decimal numbers (e.g., '1,23' -> '1.23')
    value = re.sub(r',', '.', value)

    # Step 3: Remove leading zeros unless it's a decimal (e.g., '01.23' -> '1.23')
    value = re.sub(r'^0+(\.\d+)', r'0\1', value)  # Ensure '0.x' is kept
    value = re.sub(r'^0+(\d)', r'\1', value)  # Remove leading zeros before digits

    # Step 4: Transform to numeric and round to 4 decimal places
    try:
        value = round(float(value), 4)
    except ValueError:
        pass  # If conversion fails, keep the original value

    return str(value)

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
def handle_extra_variables(df, patterns_common_words, numeric_patterns):
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
    # extracted = df.loc[mask_exponent, 'clean_result'].str.extract(exponent_pattern)
    # Apply standardization to the base number (n1)
    # df.loc[mask_exponent, 'clean_result'] = extracted[0].apply(standardize_number) + extracted[2] # Clean the number and add the exponent
    
    # Clean up stray characters from exponents
    #df['clean_result'] = df['clean_result'].str.replace(r"[\*\^]", "", regex=True)

    return df

# -----------------------------------------
# ----- Step 3: Classify the numeric result
def classify_numeric_results(df,  numeric_patterns):
    """ Classifies numeric results into n1, n2, n3, and n4 scales based on patterns."""
    # Ensure 'comentari' column exists:
    if 'num_type' not in df.columns:
        df['num_type'] = pd.NA

    for num_type in ['n1', 'n2', 'n3', 'n4', 'other']:
        # Assign the scale type based on the numeric patterns
        df['num_type'] = df['num_type'].where(
            ~df['clean_result'].astype(str).str.match(f"^{numeric_patterns[num_type]}$"), num_type
        )

    return df

# -----------------------------------------
# ----- Step 4: Standardize numeric results based in classification
def standardize_numeric_results(df):
    """ Standardizes the lab data by cleaning the result values and assigning scale types."""

    # Step 1: Harmonize n1 results.
    mask_n1 = (df['num_type'] == 'n1') # Create a mask for the conditions
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

    return df


# -----------------------------------------
# ----- Step 5: Standardize unit.
def standardize_unit(df, unit_patterns):
    """ Standardizes the format of units in the lab data."""
    df = df.copy()

    # Ensure "clean_unit" column exists.
    if "clean_unit" not in df.columns:
        df["clean_unit"] = df["unitat_mesura"]
        df['comentari_unitat'] = pd.NA
    
    # For each unit in the unit_patterns dictionary, if it is found in the "unitat_mesura" column, replace it with the corresponding key.
    for unit, pattern in unit_patterns.items():
        mask = (df["clean_unit"].str.contains(pattern, na = False, flags = re.IGNORECASE, regex = True) & df['comentari_unitat'].isna()) # Filter dataframe to only include rows where the pattern is found.
        df.loc[mask, "clean_unit"] = unit # Replace the unit with the standardized unit.
        df.loc[mask, "comentari_unitat"] = "done" # Add a comment to the 'comentari_unitat' column.

    return df

# -----------------------------------------
# ----- Step 5: Standardize test name for each code.
def standardize_name(df):
    """ The same lab test code can have multiple literals, we are going to keep only the most common one."""
    df['lab_prova'] = df.groupby('lab_prova_c')['lab_prova'].transform(lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0])

    return df

# -----------------------------------------
# ----- Step 6: Reference values
def standardize_reference_values(df):
    """ Standardizes the reference values in the lab data."""
    df = df.copy()
    mask_min = df['ref_min'].notna() # Create a mask for the conditions
    mask_max = df['ref_max'].notna() # Create a mask for the conditions
    
    df.loc[mask_min, 'ref_min'] = df.loc[mask_min, 'ref_min'].apply(standardize_number) # Apply transformation using the mask (vectorized)
    df.loc[mask_max, 'ref_max'] = df.loc[mask_max, 'ref_max'].apply(standardize_number) # Apply transformation using the mask (vectorized)


    return df

# -----------------------------------------
# ----- Step 7: Standardize peticio_id
def standardize_peticio_id(df):
    """ Standardizes the peticio_id in the lab data."""
    df = df.copy()
    # Remove hypens from "peticio_id"
    df["peticio_id"] = df["peticio_id"].str.replace(r"-", "")
    df["peticio_id"] = df["peticio_id"].str.replace(r"\.0", "", regex = True)

    return df