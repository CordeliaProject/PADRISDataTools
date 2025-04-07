# Class for the assegurats table from PADRIS
from classes.common import CommonData

class Assegurats(CommonData):
    """
    This class will deal with the processes related to the assegurats table from PADRIS.
    """

    def __init__(self, df, column_casts):
        """ Constructor for the Assegurats class. """
        super().__init__(df, column_casts) 


    def _add_year_col(self, date_col):
        """ Add a year column from a date column."""
        if date_col in self.df.columns:  # Ensure column exists
            self.df['any_defuncio'] = self.df[date_col].dt.year
            self.df['any_defuncio'] = self.df['any_defuncio'].astype('Int64')  # Use nullable integer type

            return self.df
        
        else:
            raise ValueError(f"Column '{date_col}' not found in the DataFrame.")

    def process_df(self):
        """ Function to process Assegurats data."""
        self.df = self.unify_missing_values()
        self.df = self.cast_columns()
        self.df = self._add_year_col('data_defuncio')
        
        return self.df