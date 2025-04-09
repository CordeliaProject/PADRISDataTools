
from source.classes.assegurats import Assegurats
from source.classes.cmbd import Episodis, DiagnosticsProcediments
from source.classes.lab import Lab
from source.classes.farmacia import Farmacia
from source.classes.primaria import Primaria
from source.classes.mesures import Mesures
from source.classes.mortalitat import Mortalitat
from source.utils.mesures_info import *

import pandas as pd

def generate_report(df, entity, report_path, preprocessing_df):
    def count_na(df):
        na_counts = df.isna().sum()
        total_rows = len(df)
        for col, na in na_counts.items():
            pct = (na / total_rows) * 100 if total_rows else 0
            f.write(f"  - {col}: {na} ({pct:.2f}%)\n\n")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Report for entity: {entity}\n")
        f.write("-"*50 + "\n")
        f.write(f"Rows before processing: {len(preprocessing_df)}\n")
        f.write(f"Rows after processing: {len(df)}\n\n")

        f.write("Missing values per column (before processing):\n")
        count_na(preprocessing_df)

        f.write("Missing values per column (after processing):\n")
        count_na(df)

        f.write("\nData types:\n")  # Now works with utf-8!
        for col, dtype in df.dtypes.items():
            f.write(f"  - {col}: {dtype}\n")

def process_dataframe(df, outpath, entity, column_casts, lab_option = None, lab_conversion = None, episodis = None, report = False):
    """
    Function to process a dataframe based on the entity type.
    
    Args:
        inpath (str): Path to the input file.
        outpath (str): Path to the output file.
        entity (str): Type of entity ('Assegurats', 'Episodis', 'Diagnostics', 'Procediments', 'Lab', 'Farmacia').
        column_casts (dict): Dictionary of columns and their target data types.
        episodis (str): Path to episodis file whn option is Diagnostics or Procediments.
        lab_option (str): Used only if entity == 'Laboratori'. If set to 'filter', applies filtering before processing.
        lab_conversion (str): Used only if entity == 'Laboratori'. If set to 'filter' add path to conversion file.
    """
    # In case of Diagnostics or Procediments, check if episodis exist.
    if entity in ['Diagnostics', 'Procediments'] and episodis is None:
        raise ValueError(f"Entity '{entity}' requires an episodis file.")

    # Process the dataframe based on the entity type
    if entity == 'Assegurats':
        data_processor = Assegurats(df, column_casts['Assegurats'])
    if entity == 'Mortalitat':
        data_processor = Mortalitat(df, column_casts['Mortalitat'])
    elif entity == 'Episodis':
        data_processor = Episodis(df, column_casts['Episodis'])
    elif entity == 'Diagnostics':
        episodis_small= pd.read_csv(episodis, sep = "|", usecols = ['codi_p', 'episodi_id', 'any_referencia'])
        data_processor = DiagnosticsProcediments(df, column_casts['Diagnostics'], entity, episodis_small)
    elif entity == 'Procediments':
        episodis_small= pd.read_csv(episodis, sep = "|", usecols = ['codi_p', 'episodi_id', 'any_referencia'])
        data_processor = DiagnosticsProcediments(df, column_casts['Procediments'], entity, episodis_small)
    elif entity == 'Laboratori':
        if lab_option == "filter":
            data_processor = Lab(df, column_casts['Filtered_laboratori'])
        else:
            data_processor = Lab(df, column_casts['Laboratori'])
    elif entity == 'Farmacia':
        data_processor = Farmacia(df, column_casts['Farmacia'])
    elif entity == 'Primaria':
        data_processor = Primaria(df, column_casts['Primaria'])
    elif entity == 'Mesures':
       data_processor = Mesures(df, column_casts['Mesures'], ranges, codi_mesures)

    # Check table before processing
    preprocessing_df = data_processor.df

    # Process the dataframe and save it to the output path
    if entity == 'Laboratori' and lab_option == 'filter':
        processed_df = data_processor.filter_lab(lab_conversion)
    else:
        processed_df = data_processor.process()

    if report: # If report option is true, print report file.
        report_path = outpath.replace(".csv", "_report.txt")
        generate_report(processed_df, entity, report_path, preprocessing_df)

    processed_df.to_csv(outpath, index=False, sep = "|")  # Save the processed dataframe to CSV
