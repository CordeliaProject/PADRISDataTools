################################################
# Factors used to clean lab data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 10/12/2024
################################################

import pandas as pd
# This script is not used directly, in here you'll find the factors used to transform from one unit to another

# Dictionary to use known base units.
base_units = {"l",      # Volume
              "mm3",    # Volume
              "g",      # Mass
              "mol",    # Moles
              "m",      # Molarity
              "s",      # Time (seconds)
              "ui",     # Enzymatic activity
              "eq",     # Equivalents
              "osmol",  # Osmol
              "kat",    # Enzymatic activity
              "ph"      # pH
              }

# Dictionary to transform inside the same unit in different magnitudes
factor_dict = {
     "p": 1e-12,
     "n": 1e-9,
     "µ": 1e-6,
     "m": 1e-3,
     "d": 1e-1,
     "": 1,
     "k": 1e3,
}
