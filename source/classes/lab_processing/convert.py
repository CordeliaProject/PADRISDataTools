# Dictionary to convert between different units of measurement for lab results.

conversion_factors = {
    ("g/L", "mg/dL"): 100,     # 1 g/L = 100 mg/dL
    ("mg/dL", "g/L"): 0.01,    # 1 mg/dL = 0.01 g/L
    ("mg/dL", "mg/L"): 10,     # 1 mg/dL = 10 mg/L
    ("mg/L", "mg/dL"): 0.1,    # 1 mg/L = 0.1 mg/dL
    ("g/L", "g/dL"): 0.1,      # 1 g/L = 0.1 g/dL
    ("g/dL", "g/L"): 10,       # 1 g/dL = 10 g/L
    ("g/L", "mg/mL"): 1,       # 1 g/L = 1 mg/mL
    ("mg/mL", "g/L"): 1,       # 1 mg/mL = 1 g/L
    ("mg/dL", "ug/mL"): 10,    # 1 mg/dL = 10 µg/mL
    ("ug/mL", "mg/dL"): 0.1, # 1 µg/mL = 0.1 mg/dL
    ("mg/L", "ug/dL"): 100,    # 1 mg/L = 100 µg/dL
    ("ug/dL", "mg/L"): 0.01,   # 1 µg/dL = 0.01 mg/L
}