import sys
import pandas as pd
import os
import time
from source.processing import process_dataframe
from source.utils.column_casts import column_casts
from source.utils.valid_entities import VALID_ENTITIES

def main():
    """Main function to prepare PADRIS data based on entity type."""
    args = sys.argv[1:]

    # Support an optional `--report` flag at the end
    report = '--report' in args
    if report:
        args.remove('--report')

    if len(args) not in [3, 4]:
        print("Usage: python3 main.py <inpath> <outpath> <entity> [lab_option] [--report]")
        sys.exit(1)

    inpath, outpath, entity = args[0], args[1], args[2]
    lab_option = args[3] if len(args) == 4 else None

    if not os.path.exists(inpath):
        print(f"❌ Input path '{inpath}' does not exist.")
        sys.exit(1)

    try:
        print("Reading input...")
        # Optional: validate file format early
        df = pd.read_csv(inpath, sep="|", low_memory=False)
    except Exception as e:
        raise ValueError("⚠️ Failed to read input file. Ensure it's a CSV with '|' separator.") from e

    # Optional: add some validation logic for the entity name here
    if entity not in VALID_ENTITIES:
        print(f"⚠️ '{entity}' is not a recognized entity.")
        sys.exit(1)

    ### DATAFRAME PROCESSING ###
    else:
        print("Processing dataframe...")
        if entity == 'Laboratori':
            process_dataframe(df, outpath, entity, column_casts, lab_option, report = report)
        else:
            process_dataframe(df, outpath, entity, column_casts, report = report)

    
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time:.2f} seconds ---")