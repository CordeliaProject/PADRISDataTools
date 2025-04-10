# Class for the mortalitat table from PADRIS
from source.classes.common import CommonData
import numpy as np

class Mortalitat(CommonData):
    """
    This class will deal with the processes related to the mortalitat table from PADRIS.
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

    def _modify_dx_columns(self):
        """ Function to change the columns in mortalitat to one dx col and one catalegcim_dx col."""
        self.df = self.df.assign(
        causa_defuncio_c=self.df['Causa_CIM10_codi'].fillna(self.df['Causa_CIM9_codi']),
        causa_defuncio=self.df['Causa_CIM10'].fillna(self.df['AS_Causa_CIM9']),
        catalegcim=np.where(self.df['Causa_CIM10_codi'].notna(), 'CIM10MC', np.where(self.df['Causa_CIM9_codi'].notna(), 'CIM9MC', None))
        )

        self.df = self.df.drop(columns=['Causa_CIM9_codi', 'AS_Causa_CIM9', 'Causa_CIM10_codi', 'Causa_CIM10'])

        return self.df

    def _harmonize_diagnostics(self):
        """Harmonize diagnostics by selecting the most frequent diagnosis for each group."""
        # Safely get the most frequent cause for each (causa_defuncio_c, catalegcim) combination
        most_common_causa = self.df.groupby(['causa_defuncio_c', 'catalegcim'])['causa_defuncio'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        # Map back to the original dataframe
        return self.df.set_index(['causa_defuncio_c', 'catalegcim']).index.map(most_common_causa.to_dict())

    def process(self):
        """ Function to process Assegurats data."""
        self.df = self.unify_missing()
        self.df = self.cast_columns()
        self.df = self._add_year_col('Data_defuncio')
        self.df = self._modify_dx_columns()
        self.df['causa_defuncio'] = self._harmonize_diagnostics()
        self.df.rename(columns={"Data_defuncio": "data_defuncio"}, inplace=True)
        return self.df