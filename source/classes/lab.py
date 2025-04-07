# Class for the Lab tables from PADRIS
from classes.common import CommonData


class Lab(CommonData):
    """
    This class will deal with the processes related to the lab table from PADRIS.
    """

    def __init__(self, df, column_casts):
        """ Constructor for the LAB class. """
        super().__init__(df, column_casts) 

    

    def process_df(self):
        """ Function to process Assegurats data."""
        self.df = self.unify_missing_values()

        #self.df = self.cast_columns()

        return self.df