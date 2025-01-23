################################################
# Clean Problemes de salut a primaria
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 16/01/2024
################################################

import argparse
from pathlib import Path
from utils.functions import unify_missing_values, process_df, remove_outliers, export
import pandas as pd


# -------------------
# Main
# -------------------
def main(inpath, outpath):
    """
    Main function to clean and preprocess Measurement data.
    """
    # Statistics dictionary to track row counts at each step
    stats = {step: {} for step in ["initial", "processed", "remove_outliers"]}
    
    # Prepare output and statistics paths
    statistics_path = outpath.parent / "statistics"
    statistics_path.mkdir(exist_ok=True)

    print(f"Processing AP_Problemes_Salut...")

    # Step 1: Read the initial file
    df = pd.read_csv(inpath, sep="|")
    stats["initial"]["AP_Problemes_Salut"] = len(df)

    # Step 2: Unify missing values
    df = unify_missing_values(df)

    # Step 3: Process dataframe
    df = process_df(df)
    stats["processed"]["AP_Problemes_Salut"] = len(df)
    
    print(f"Removing outliers...")
    # Step 4: Remove outliers
    filtered_df = remove_outliers(df)
    stats["remove_outliers"]["AP_Problemes_Salut"] = len(filtered_df)

    # Step 4: Generate clean file
    export(filtered_df, outpath)
    print(f"Exported AP_Problemes_Salut to {outpath}")

    # Step 3: Export statistics to Excel
    stats_df = pd.DataFrame(stats)
    stats_file = statistics_path / f"AP_Problemes_Salut_processing_statistics.xlsx"
    stats_df.to_excel(stats_file, index_label="Entity Name")
    print(f"Processing statistics saved to {stats_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess measurement data.")
    parser.add_argument("--inpath", type=str, required=True, help="Input path for measurement files.")
    parser.add_argument("--outpath", type=str, required=True, help="Output path for cleaned files.")
    args = parser.parse_args()

    inpath = Path(args.inpath)
    outpath = Path(args.outpath)

    # Run main script
    main(inpath, outpath)