################################################
# Clean LAB data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 10/12/2024
################################################

import argparse
import time
import os
from pathlib import Path
import pandas as pd
from collections import defaultdict
from utils.functions import preprocessing, add_commons, processing
from utils.factors import factor_dict, base_units

# -------------------
# Main
# -------------------
def main(inpath, outpath, chunksize):
    """ Main functino to clean and process lab data. """
    # Record start time
    start_time = time.time()
    label_counts = defaultdict(lambda: defaultdict(int))
    unit_counts = defaultdict(lambda: defaultdict(int))

    for i, chunk in enumerate(pd.read_csv(inpath, sep="|", chunksize=chunksize)):
         # Step 1: Go chunk by chunk and pre-clean formats, and units.
        print(f"Precleaning and cleaning chunk {i+1}...")
        chunk = preprocessing(chunk) # Process the chunk

        # Update label counts
        # Update both label_counts and unit_counts in one loop
        for prova, group in chunk.groupby('lab_prova_c'):
            label_counts[prova].update(group['lab_prova'].value_counts().to_dict())
            unit_counts[prova].update(group['unitat_mesura'].value_counts().to_dict())

        # Add common unit and label information to the chunk
        chunk = add_commons(chunk, label_counts, unit_counts)

        # Step 2: Convert units and labels to the most common one for each different lab prova
        # chunk = processing(chunk) # Process the chunk

        # Append preprocessed chunk to temporal file
        chunk.to_csv(outpath, sep="|", index=False, mode='a', header=False)

    end_time = time.time()
    print(f"Process done for all chunks, total time: {((end_time - start_time) / 60):.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess LAB data.")
    parser.add_argument("--inpath", type=str, required=True, help="Input path for LAB files.")
    parser.add_argument("--outpath", type=str, required=True, help="Output path for cleaned files.")
    parser.add_argument("--chunksize", type=int, default=1000000, help="Number of rows processed.")
    args = parser.parse_args()

    inpath = Path(args.inpath)
    outpath = Path(args.outpath)
    chunksize = int(args.chunksize)

    main(inpath, outpath, chunksize)