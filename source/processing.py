from classes.common import CommonData
from classes.assegurats import Assegurats
from classes.cmbd import Episodis, DiagnosticsProcediments
from classes.lab import Lab
from classes.farmacia import Farmacia
from classes.primaria import Primaria

import pandas as pd

def process_dataframe(inpath, outpath, entity, column_casts):
    """
    Function to process a dataframe based on the entity type.
    
    Args:
        inpath (str): Path to the input file.
        outpath (str): Path to the output file.
        entity (str): Type of entity ('Assegurats', 'Episodis', 'Diagnostics', 'Procediments', 'Lab', 'Farmacia').
        column_casts (dict): Dictionary of columns and their target data types.
    """

    # Read the input file
    df = pd.read_csv(inpath, low_memory=False)

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
    elif entity == 'Lab':
        data_processor = Lab(df, column_casts)
    elif entity == 'Farmacia':
        data_processor = Farmacia(df, column_casts['Farmacia'])
    elif entity == 'Primaria':
        data_processor = Primaria(df, column_casts['Primaria'])
    else:
        raise ValueError(f"Unknown entity type: {entity}")

    # Process the dataframe and save it to the output path
    processed_df = data_processor.process_df()
    processed_df.to_csv(outpath, index=False, sep = "|")  # Save the processed dataframe to CSV
