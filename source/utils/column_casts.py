# Dictionary of data types to cast columns.
# This dictionary is used to specify the target data types for each column in the DataFrame.

import pandas as pd

column_casts = {
    'Assegurats': {
        'abs_c': pd.Int64Dtype(),
        'ss_c': pd.Int64Dtype(),
        'rs_c': pd.Int64Dtype(),
        'municipi_c': pd.Int64Dtype(),
        'comarca_c': pd.Int64Dtype(),
        'provincia_c': pd.Int64Dtype(),
        'data_defuncio': 'datetime64[ns]',
},
    'Episodis': {
        'episodi_id': pd.Int64Dtype(),
        'up_c': pd.Int64Dtype(),
        'any_referencia': pd.Int64Dtype(),
        'dies_estada_n': pd.Int64Dtype(),
        'circumstancia_ingres_c': pd.Int64Dtype(),
        'circumstancia_alta_c': pd.Int64Dtype(),
        'tipus_activitat_c': pd.Int64Dtype(),
        'data_ingres': 'datetime64[ns]',
        'data_alta': 'datetime64[ns]',
},
    'Diagnostics': {
        'episodi_id': pd.Int64Dtype(),
        'dx_posicio': pd.Int64Dtype(),
},
    'Procediments':{
        'episodi_id': pd.Int64Dtype(),
        'px_posicio': pd.Int64Dtype(),
},
    'Mesures': { 
        'Prova_resultat': 'float',
        'Prova_data': 'datetime64[ns]',
},
    'Primaria': { 
        'any_problema_salut': pd.Int64Dtype(),
        'data_problema_salut': 'datetime64[ns]',
        'data_problema_salut_baixa': 'datetime64[ns]',
},
    'Mortalitat': { 
        'Data_defuncio': 'datetime64[ns]',
    },
}