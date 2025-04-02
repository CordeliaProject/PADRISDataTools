################################################
# Factors used to clean lab data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 10/12/2024
################################################

import pandas as pd

# Dictionary to transform from one unit to another in different measurements
conversion_dict = {
    'Q13285' : {'unit': 'mmol/l', 'factor': 38.66}, # Total cholesterol
    'Q12785' : {'unit': 'mmol/l', 'factor': 38.66}, # HDL cholesterol
    'Q53585' : {'unit': 'g/l', 'factor': 100}, # Triglyceride
    'Q53585' : {'unit': 'mmol/l', 'factor': 88.5}, # Triglyceride
    'Q32685' : {'unit': 'mmol/l', 'factor': 18}, # Glucose
    'Q32666' : {'unit': 'mmol/l', 'factor': 18}, # Glucose
    'Q15185' : {'unit': 'umol/l', 'factor': 88.42}, # Creatinine
    'Q15166' : {'unit': 'umol/l', 'factor': 88.42}, # Creatinine
    }