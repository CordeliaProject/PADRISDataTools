################################################
# Casts (data types) for Assegurats
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 09/12/2024
################################################
import pandas as pd

casts = { 
'Assegurats': {
    'abs_c': pd.Int64Dtype(),
    'ss_c': pd.Int64Dtype(),
    'rs_c': pd.Int64Dtype(),
    'municipi_c': pd.Int64Dtype(),
    'comarca_c': pd.Int64Dtype(),
    'provincia_c': pd.Int64Dtype(),
}
}