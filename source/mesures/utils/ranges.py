################################################
# Ranges to remove outliers from measurement data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 16/12/2024
################################################

ranges = {
    'TT101' : [110, 250], # Valid range for talla in cm
    'TT102' : [30, 250], # Valid range for pes in kg
    'EK201' : [60, 220], # Valid range for PAS in mmHg
    'EK202' : [40, 130] # Valid range for PAD in mmHg
}

unitats = {
    'TT101' : 'cm', # Unit for talla
    'TT102' : 'kg', # Unit for pes
    'EK201' : 'mmHg', # Unit for PAS
    'EK202' : 'mmHg' # Unit for PAD
}