# Common class to all data in the project

import pandas as pd
import numpy as np


class CommonData:
    """ This class will deal with the processes common among all PADRIS data."""
    
    def __init__(self, df, column_casts,):
        """ Constructor for the CommonData class. """
        self.df = df
        self.column_casts = column_casts

    def unify_missing(self):
        """ Replace various representations of missing values with a unified version."""
        self.df = self.df.replace([pd.NA, np.nan, 'nan', 'NaN', ''], pd.NA)
        return self.df
    
    def cast_columns(self):
        """Safely cast dataframe columns to specified types."""
        for col, dtype in self.column_casts.items():
            if col in self.df.columns:  # Check if column exists
                try:
                    if dtype == 'datetime64[ns]':  # Special case for dates
                        self.df[col] = pd.to_datetime(self.df[col], errors='coerce', dayfirst=False)
                        self.df[col] = self.df[col].dt.tz_localize(None)  # Remove timezone
                    elif dtype in ['float', 'float64']:
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    else:
                        self.df[col] = self.df[col].astype(dtype)
                except Exception as e:
                    print(f"Warning: Failed to convert column '{col}' to '{dtype}': {e}")
            else:
                print(f"Warning: Column '{col}' not found in the DataFrame.")
        return self.df
        
        
