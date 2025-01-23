################################################
# Casts (data types) for CMBD data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 09/12/2024
################################################
import pandas as pd

# Column types for casting
casts = { 
'episodis': {
    'episodi_id': pd.Int64Dtype(),
    'up_c': pd.Int64Dtype(),
    'any_referencia': pd.Int64Dtype(),
    'dies_estada_n': pd.Int64Dtype(),
    'circumstancia_ingres_c': pd.Int64Dtype(),
    'circumstancia_alta_c': pd.Int64Dtype(),
    'tipus_activitat_c': pd.Int64Dtype()
},
'diagnostics': {
    'episodi_id': pd.Int64Dtype(),
    'dx_posicio': pd.Int64Dtype()
},
'procediments':{
    'episodi_id': pd.Int64Dtype(),
    'px_posicio': pd.Int64Dtype()
}
}
