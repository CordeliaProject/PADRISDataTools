# Class for the Primaria tables from PADRIS
from source.classes.common import CommonData

class Primaria(CommonData):
    """
    Processes Primaria data from the PADRIS dataset.
    """
    def __init__(self, df, column_casts):
        """ Constructor for the Assegurats class. """
        super().__init__(df, column_casts)  # Pass outpath to parent constructor

    def _rename_columns(self):
        """ Rename columns from the dataframe to get same variables as in CMBD"""
        self.df = self.df.rename(columns=
                                 {'any_problema_salut':'any_referencia',
                                  'data_problema_salut': 'data_ingres',
                                  'data_problema_salut_baixa': 'data_alta',
                                  'catalegcim_problema_salut_c': 'catalegcim_dx',
                                  'problema_salut_c': 'dx_c',
                                  'problema_salut': 'dx'})

        return self.df
    
    def _correct_cim_values(self):
        """ Replace values in the 'catalegcim' column """
        self.df['catalegcim_dx'] = self.df['catalegcim_dx'].replace({
            'CIM-10-MC': 'CIM10MC'})
        
        return self.df

    def process(self):
        """ Function to process Primaria data."""
        self.df = self.unify_missing()
        self.df = self.cast_columns()
        self.df = self._rename_columns()
        self.df = self._correct_cim_values()

        return self.df