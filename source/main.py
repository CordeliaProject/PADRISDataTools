import sys
import pandas as pd
import os
from processing import process_dataframe
from utils.column_casts import column_casts
from utils.valid_entities import VALID_ENTITIES

def main():
    """Main function to prepare PADRIS data based on entity type."""
    args = sys.argv[1:]

    if len(args) not in [3, 4]:
        print("Usage: python3 main.py <inpath> <outpath> <entity> [lab_option]")
        sys.exit(1)

    inpath, outpath, entity = args[0], args[1], args[2]
    lab_option = args[3] if len(args) == 4 else None

    if not os.path.exists(inpath):
        print(f"❌ Input path '{inpath}' does not exist.")
        sys.exit(1)

    try:
        # Optional: validate file format early
        df = pd.read_csv(inpath, sep="|", low_memory=False)
    except Exception as e:
        raise ValueError("⚠️ Failed to read input file. Ensure it's a CSV with '|' separator.") from e

    # Optional: add some validation logic for the entity name here
    if entity not in VALID_ENTITIES:
        print(f"⚠️ '{entity}' is not a recognized entity.")
        sys.exit(1)

    else:
        if entity == 'Laboratori':
            process_dataframe(df, outpath, entity, column_casts, lab_option)
        else:
            process_dataframe(df, outpath, entity, column_casts)