################################################
# Clean CMBD data (episodis, diagnostics, procediments)
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 09/12/2024
################################################

import argparse
from pathlib import Path
from utils.casts import casts
from utils.functions import preprocess_file, process_df, fix_inconsistencies
from pathlib import Path
import pandas as pd


# -------------------
# Main
# -------------------
def main(files, casts, outpath):
    """ Main function to clean and preprocess CMBD data. """
    # Statistics dictionary to track row counts at each step
    stats = {step: {} for step in ["initial", "preprocessed", "processed", "fixed_inconsistencies"]}
    
    # Prepare output and statistics paths
    statistics_path = outpath / "statistics"
    statistics_path.mkdir(exist_ok=True)

    results = {}
    for entity_name, file_path in files.items():
        print(f"Processing {entity_name}...")

        # Step 1: Read the initial file
        df = pd.read_csv(file_path, sep="|")
        stats["initial"][entity_name] = len(df)

        # Step 2: Preprocess the file to correct data types
        column_casts = casts.get(entity_name, {})
        df = preprocess_file(file_path, column_casts, entity_name)
        stats["preprocessed"][entity_name] = len(df)

        # Skip entities with empty data
        if df.empty:
            print(f"Skipping {entity_name} due to errors.")
            continue

        # Step 3: Process the dataframe to unify dates and labels
        df = process_df(df, entity_name)
        # Save statistics
        stats["processed"][entity_name] = len(df)

        results[entity_name] = df
    
    # Step 4: Solve inconsistencies in Diagnostics and Procediments
    for entity_name, df in results.items():
        if entity_name != "Episodis":
            df = fix_inconsistencies(results['Episodis'], df, entity_name)
        # Save statistics
        stats["fixed_inconsistencies"][entity_name] = len(df)
    
    # Step 5: Handle Episodis-specific inconsistencies
    results['Episodis'].loc[
        (results['Episodis']['any_referencia'] >= 2018),
        'episodi_id'
    ] = results['Episodis']['episodi_id'].abs()
    # Save statistics
    stats["fixed_inconsistencies"]["Episodis"] = len(results['Episodis'])

    # Step 6: Export results
    for entity_name, df in results.items():
        output_file = outpath / f"AH_{entity_name}.csv"
        df.to_csv(output_file, sep="|", index=False)
        print(f"Exported {entity_name} to {output_file}")

    # Step 7: Export statistics to Excel
    stats_df = pd.DataFrame(stats)
    stats_file = statistics_path / "cmbd_processing_statistics.xlsx"
    stats_df.to_excel(stats_file, index_label="Entity Name")
    print(f"Processing statistics saved to {stats_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess CMBD data.")
    parser.add_argument("--inpath", type=str, required=True, help="Input path for CMBD files.")
    parser.add_argument("--outpath", type=str, required=True, help="Output path for cleaned files.")
    args = parser.parse_args()

    inpath = Path(args.inpath)
    outpath = Path(args.outpath)

    # Define file paths
    files = {
        "Episodis": inpath / "AH_Episodis.csv",
        "Diagnostics": inpath / "AH_Diagnostics.csv",
        "Procediments": inpath / "AH_Procediments.csv",
    }

    main(files, casts, outpath)
