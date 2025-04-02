################################################
# Ranges to remove outliers from lab data and selected variables
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 02/04/2025
################################################

selected = {
    'Q13285' : 'Colesterol-Sèrum',
    'Q12785' : 'Colesterol HDL-Sèrum',
    'R12785' : 'Colesterol HDL-Sèrum',
    'Q12766' : 'Colesterol HDL-Sèrum',
    # 'Q12985' : 'LDL cholesterol',
    'Q53585' : 'Triglicèrid-Sèrum',
    'Q32685' : 'Glucosa-Sèrum',
    'Q32666' : 'Glucosa-Plasma',
    'Q15185' : 'Creatinini-Sèrum',
    'Q15166' : 'Creatinini-Plasma',
}

units = {
    'Q13285' : 'mg/dL', # Unit for colesterol
    'Q12785' : 'mg/dL', # Unit for HDL cholesterol
    'R12785' : 'mg/dL', # Unit for HDL cholesterol
    'Q12766' : 'mg/dL', # Unit for HDL cholesterol
    'Q12985' : 'mg/dL', # Unit for LDL cholesterol
    # 'Q53585' : 'mg/dL', # Unit for triglyceride
    'Q32685' : 'mg/dL', # Unit for glucose
    'Q32666' : 'mg/dL', # Unit for glucose
    'Q15185' : 'mg/dL', # Unit for creatinine
    'Q15166' : 'mg/dL', # Unit for creatinine
}

ranges = {
    'Q13285' : [100, 450], # Valid range for total cholesterol mg/dL
    'Q12785' : [20, 130], # valid range for HDL cholesterol mg/dL
    'R12785' : [20, 130], # valid range for HDL cholesterol mg/dL
    'Q12766' : [20, 130], # valid range for HDL cholesterol mg/dL
    'Q12985' : [20, 250], # Valid range for LDL cholesterol mg/dL -> ES CALCULA MANUALMENT
    # 'Q53585' : [30, 500], # Valid range for triglycerides mg/dL -> FALTA
    'Q32685' : [30, 350], # Valid range for glucose mg/dL
    'Q32666' : [30, 350], # Valid range for glucose mg/dL
    'Q15185' : [0.5, 10], # Valid range for creatinine mg/dL
    'Q15166' : [0.5, 10], # Valid range for creatinine mg/dL
}
