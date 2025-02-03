################################################
# Clean LAB data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 10/12/2024
################################################

import argparse
import time
import warnings
import os
from pathlib import Path
import pandas as pd
from utils.functions import *
from utils.patterns import *


# -------------------
# Main
# -------------------
def main(inpath, outpath, report):
    """ Main function to clean and process lab data. """
    # Record start time
    start_time = time.time()
    warnings.filterwarnings("ignore", category=UserWarning, message=".*match groups.*") # 

    print("Reading input...")
    # Import dataframe
    df = pd.read_csv(inpath, sep = "|")

    # Important: Transform empty values to nocalc
    df["lab_resultat"] = df["lab_resultat"].fillna("nocalc")

    # -----------------------------------------
    # ----- Step 1: Clear typos
    print("Step 1: Cleaning types")
    clear_df = clear_typos(df)

    # -----------------------------------------
    # ----- Step 2: Handle extra variables in the result
    print("Step 2: Handle extra variables")
    clean_df = handle_extra_variables(clear_df, patterns_common_words, numeric_patterns, report=True)

    # -----------------------------------------
    # ----- Step 3: Classify the numeric result
    print("Step 3: Handle numeric results")
    clean_df = classify_numeric_results(clean_df,  numeric_patterns)

    # -----------------------------------------
    # ----- Step 4: Standardize numeric results based in classification
    standardize_df = standardize_numeric_results(clean_df, report=True)

    # -----------------------------------------
    # ----- Step 5: Standardize unit.
    print("Step 4: Standardize units")
    standardize_df = standardize_unit(standardize_df, unit_patterns, report=True)

    # -----------------------------------------
    # ----- Step 6: Standardize test name for each code.
    print("Step 5: Standardize lab test name")
    standardize_df = standardize_name(standardize_df)
    
    # -----------------------------------------
    # ----- Extra: Change column name to facilitate management
    # Order the columns
    standardize_df = standardize_df[['codi_p','peticio_id','Any_prova','Data_prova','lab_prova_c','lab_prova','lab_resultat','unitat_mesura','ref_min','ref_max','clean_result','clean_unit','comentari','comentari_unitat','num_type']]
    standardize_df = standardize_df.rename(columns={"Any_prova": "any", "Prova_data": "data", "lab_resultat": "resultat", "lab_prova_c": "codi_prova", "lab_prova":"prova"})


    end_time = time.time()
    print(f"Process done, total time: {((end_time - start_time) / 60):.2f} min.")
    standardize_df.to_csv(outpath, sep = "|", index = False)
    print(f"Clean lab data in:")
    print(f"{outpath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess LAB data.")
    parser.add_argument("--inpath", type=str, required=True, help="Input path for lab file.")
    parser.add_argument("--outpath", type=str, required=True, help="Output path for cleaned files.")
    parser.add_argument("--report", action="store_true", help="Enable report printing.")

    args = parser.parse_args()

    inpath = Path(args.inpath)
    outpath = Path(args.outpath)
    report = args.report  # This will be True if --report is passed, otherwise False

    main(inpath, outpath, report)