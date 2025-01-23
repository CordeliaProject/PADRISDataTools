################################################
# Clean mesures data (PAD, PAS, Talla, Pes)
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 16/12/2024
################################################

from utils.casts import casts
from utils.functions import process_df, export
from utils.codi_mesures import codis
import argparse
from pathlib import Path
import pandas as pd

def main(measurement, inpath, casts, outpath):
    """
    Main function to clean and preprocess Measurement data.
    """
    # Statistics dictionary to track row counts at each step
    stats = {step: {} for step in ["initial", "processed"]}
    
    # Prepare output and statistics paths
    statistics_path = outpath.parent / "statistics"
    statistics_path.mkdir(exist_ok=True)

    print(f"Processing {measurement}...")

    # Step 1: Read the initial file
    df = pd.read_csv(inpath, sep="|")
    stats["initial"][measurement] = len(df)

    # Step 2: Process the file to correct data types
    for column, dtype in casts.items():
        if dtype == 'datetime64[ns]':
            # Convert to datetime using pd.to_datetime
            df[column] = pd.to_datetime(df[column], errors='coerce')
        else:
            # Apply other types
            df[column] = df[column].astype(dtype)

    # Step 3: Process dataframe to 
    df = process_df(df, codis)
    stats["processed"][measurement] = len(df)

    # Step 4: Generate clean file
    export(df, outpath)
    print(f"Exported {measurement} to {outpath}")

    # Step 3: Export statistics to Excel
    stats_df = pd.DataFrame(stats)
    stats_file = statistics_path / f"{measurement}_processing_statistics.xlsx"
    stats_df.to_excel(stats_file, index_label="Entity Name")
    print(f"Processing statistics saved to {stats_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess measurement data.")
    parser.add_argument("--measure", type=str, required=True, help="Measure you want to clean: Pes, Talla or PA.")
    parser.add_argument("--inpath", type=str, required=True, help="Input path for measurement files.")
    parser.add_argument("--outpath", type=str, required=True, help="Output path for cleaned files.")
    args = parser.parse_args()

    measurement = args.measure
    inpath = Path(args.inpath)
    outpath = Path(args.outpath)

    # Run main script
    main(measurement, inpath, casts, outpath)