
from classes.assegurats import Assegurats
from classes.cmbd import Episodis, DiagnosticsProcediments
from classes.lab import Lab
from classes.farmacia import Farmacia
from classes.primaria import Primaria

import pandas as pd

def generate_report(df, entity, report_path):
    with open(report_path, "w") as f:
            f.write(f"📄 Report for entity: {entity}\n")
            f.write("-"*50 + "\n")
            f.write(f"Rows after processing: {len(df)}\n\n")

            f.write("🔍 Missing values per column (after processing):\n")
            na_counts = df.isna().sum()
            total_rows = len(df)
            for col, na in na_counts.items():
                pct = (na / total_rows) * 100 if total_rows else 0
                f.write(f"  - {col}: {na} ({pct:.2f}%)\n")

            f.write("\n🧪 Data types:\n")
            for col, dtype in df.dtypes.items():
                f.write(f"  - {col}: {dtype}\n")

def process_dataframe(df, outpath, entity, column_casts, lab_option = None, report = False):
    """
    Function to process a dataframe based on the entity type.
    
    Args:
        inpath (str): Path to the input file.
        outpath (str): Path to the output file.
        entity (str): Type of entity ('Assegurats', 'Episodis', 'Diagnostics', 'Procediments', 'Lab', 'Farmacia').
        column_casts (dict): Dictionary of columns and their target data types.
        lab_option (str): If entity = 'Laboratori', lab_option can be 'process' or 'filter'.
    """

    # Process the dataframe based on the entity type
    if entity == 'Assegurats':
        data_processor = Assegurats(df, column_casts['Assegurats'])
    elif entity == 'Episodis':
        data_processor = Episodis(df, column_casts['Episodis'])
    elif entity == 'Diagnostics':
        episodis_small= Episodis(df, column_casts).process_df()[['codi_p', 'episodi_id', 'any_referencia']]
        data_processor = DiagnosticsProcediments(df, column_casts['Diagnostics'], entity, episodis_small)
    elif entity == 'Procediments':
        episodis_small= Episodis(df, column_casts).process_df()[['codi_p', 'episodi_id', 'any_referencia']]
        data_processor = DiagnosticsProcediments(df, column_casts['Procediments'], entity, episodis_small)
    elif entity == 'Laboratori':
        data_processor = Lab(df, column_casts)
    elif entity == 'Farmacia':
        data_processor = Farmacia(df, column_casts['Farmacia'])
    elif entity == 'Primaria':
        data_processor = Primaria(df, column_casts['Primaria'])
    else:
        raise ValueError(f"Unknown entity type: {entity}")

    # Process the dataframe and save it to the output path
    if entity == 'Laboratori' and lab_option == 'filter':
        processed_df = data_processor.filter_lab()
    else:
        processed_df = data_processor.process()

    if report: # If report option is true, print report file.
        report_path = outpath.replace(".csv", "_report.txt")
        generate_report(processed_df, entity, report_path)

    processed_df.to_csv(outpath, index=False, sep = "|")  # Save the processed dataframe to CSV
