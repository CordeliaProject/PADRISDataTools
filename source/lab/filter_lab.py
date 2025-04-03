################################################
# Filter and harmonize units for lab data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 10/12/2024
################################################

# Import libraries
import pandas as pd
from utils.test_ranges import *
from utils.factors import *
import time 
import argparse
from  pathlib import Path
import warnings

# -------------------
# Main
# -------------------
def main(inpath, conversion_file, outpath, report, result_type = "n1"):
    """ Main function to filter and harmonize lab data. """
    # Record start time
    start_time = time.time()
    warnings.filterwarnings("ignore")
    
    print("Reading input...")
    # Import dataframe
    df = pd.read_csv(inpath, sep = "|", low_memory=False)
    print(f"There are {df.shape[0]} rows.")

    # Rename columns to match the conversion file
    df.rename(columns = {'clean_unit': 'from_unit'}, inplace=True)

    # Import conversion file
    conversion_df = pd.read_csv(conversion_file, sep = "|", low_memory=False)

    # Step 1: Filter the data to keep only relevant variables
    # -----------------------------------------
    print("Step 1: Filter the data")
    filtered_df = df[df['codi_prova'].isin(list(conversion_df['codi_prova'].values))]

    print(f"After filtering, there are {filtered_df.shape[0]} rows.")

    # Step 2: Add a column with the reference unit for each test
    # -----------------------------------------
    print("Step 2: Add reference unit")
    test_df = conversion_df[['codi_prova', 'to_unit']].drop_duplicates()
    filtered_df.loc[:, 'to_unit'] = filtered_df['codi_prova'].map(test_df.set_index('codi_prova')['to_unit'])

    # Step 3: Convert the results to the reference unit
    # -----------------------------------------
    print("Step 3: Convert results to reference unit")

    # 1. Filter to keep only relevant results
    postfiltered_df = filtered_df.copy()  # Avoids modifying a slice
    postfiltered_df.loc[:, 'clean_result'] = pd.to_numeric(postfiltered_df['clean_result'], errors='coerce')

    if result_type == "n1":
        # 2. Transform the results to numeric
        postfiltered_df['clean_result'] = pd.to_numeric(postfiltered_df['clean_result'], errors='coerce')

        # 3. Merge the conversion factors with the filtered dataframe
        merged_df = postfiltered_df.merge(conversion_df, on=['codi_prova', 'from_unit', 'to_unit'], how='left')

        # 3.1. Add factor when to_unit and from_unit are the same
        merged_df.loc[merged_df['from_unit'] == merged_df['to_unit'], 'factor'] = 1

        # 3.2. Add factor when from_unit is not in the conversion file but base unit is the same
        merged_df.loc[merged_df['factor'].isna(), 'factor'] = merged_df.apply(
            lambda row: conversion_factors.get((row['from_unit'], row['to_unit']), 1), axis=1
        )

        # 4. Convert the results to the reference unit
        merged_df['converted_result'] = (merged_df['clean_result'] * merged_df['factor']).round(2)

        # Select relevant columns
        merged_df = merged_df[['codi_p', 'peticio_id', 'any', 'data', 'codi_prova', 'prova','clean_result', 'from_unit', 'converted_result', 'to_unit']]

        # If there is no unit, converted_result is empty
        merged_df.loc[merged_df['from_unit'].isna(),'converted_result'] = pd.NA
        
        #Rename columns
        merged_df.rename(columns = {'from_unit': 'unit', 'to_unit': 'converted_unit'}, inplace=True)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Conversion completed. It took {elapsed_time/60:.2f} seconds.")
        merged_df.to_csv(outpath, sep="|", index=False)
        print("File will be saved in: ", outpath)
    

    else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"No numeric results to convert. Results are filtered. It took {elapsed_time/60:.2f} seconds.")
        postfiltered_df.to_csv(outpath, sep="|", index=False)
        print("File will be saved in: ", outpath)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess lab data.")
    parser.add_argument("--inpath", type=str, required=True, help="Input path for lab file.")
    parser.add_argument("--conversion_file", type=str, required=True, help="Path to the conversion file.")
    parser.add_argument("--outpath", type=str, required=True, help="Output path for cleaned files.")
    parser.add_argument("--report", action="store_true", help="Enable report printing.")

    args = parser.parse_args()

    inpath = Path(args.inpath)
    conversion_file = Path(args.conversion_file)
    outpath = Path(args.outpath)
    report = args.report  # This will be True if --report is passed, otherwise False

    main(inpath, conversion_file, outpath, report)