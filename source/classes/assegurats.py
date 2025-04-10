# Class for the assegurats table from PADRIS
from source.classes.common import CommonData

class Assegurats(CommonData):
    """
    This class will deal with the processes related to the assegurats table from PADRIS.
    """

    def __init__(self, df, column_casts):
        """ Constructor for the Assegurats class. """
        super().__init__(df, column_casts) 

    def _check_if_assegurats(self):
        """Check if the columns correspond to a Assegurats file; if not, raise an error."""
        required_cols = {'codi_p', 'situacio_assegurat_c', 'sexe', 'abs_c', 'abs', 'ss_c', 'ss',
       'rs_c', 'rs', 'municipi_c', 'municipi', 'comarca_c', 'comarca',
       'provincia_c', 'provincia', 'data_defuncio'}
        if not required_cols.issubset(self.df.columns):
            raise ValueError("⚠️ The data does not correspond with a Assegurats file or it does not have the corresponding columns.")

    def _add_year_col(self, date_col):
        """ Add a year column from a date column."""
        if date_col in self.df.columns:  # Ensure column exists
            self.df['any_defuncio'] = self.df[date_col].dt.year
            self.df['any_defuncio'] = self.df['any_defuncio'].astype('Int64')  # Use nullable integer type

            return self.df
        
        else:
            raise ValueError(f"Column '{date_col}' not found in the DataFrame.")

    def process(self):
        """ Function to process Assegurats data."""
        self.df = self.unify_missing()
        self.df = self.cast_columns()
        self.df = self._add_year_col('data_defuncio')
        
        return self.df