################################################
# Clean Assegurats table
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 09/12/2024
################################################

from utils.casts import casts
from utils.functions import process_df, export
import argparse
from pathlib import Path
import pandas as pd

def main(inpath, casts, outpath):
    """
    Main function to clean and preprocess Assegurats data.
    """
    # Statistics dictionary to track row counts at each step
    stats = {step: {} for step in ["initial", "processed"]}
    
    # Prepare output and statistics paths
    statistics_path = outpath.parent / "statistics"
    statistics_path.mkdir(exist_ok=True)

    print(f"Processing Assegurats...")

    # Step 1: Read the initial file
    df = pd.read_csv(inpath, sep="|")
    stats["initial"]["Assegurats"] = len(df)

    # Step 2: Process the file to correct data types
    casts = casts.get("Assegurats", {})
    df = process_df(df, casts)
    stats["processed"]["Assegurats"] = len(df)

    # Step 4: Generate clean file
    export(df, outpath)
    print(f"Exported Assegurats to {outpath}")

    # Step 3: Export statistics to Excel
    stats_df = pd.DataFrame(stats)
    stats_file = statistics_path / "assegurats_processing_statistics.xlsx"
    stats_df.to_excel(stats_file, index_label="Entity Name")
    print(f"Processing statistics saved to {stats_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess Assegurats data.")
    parser.add_argument("--inpath", type=str, required=True, help="Input path for Assegurats files.")
    parser.add_argument("--outpath", type=str, required=True, help="Output path for cleaned files.")
    args = parser.parse_args()

    inpath = Path(args.inpath)
    outpath = Path(args.outpath)

    # Run main script
    main(inpath, casts, outpath)
