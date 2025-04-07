# Class for the Mesures tables from PADRIS
from source.classes.common import CommonData
import pandas as pd

class Measures(CommonData):
    """
    Processes measurement-related data from the PADRIS dataset.
    Includes filtering by relevant codes and acceptable value ranges.
    """

    def __init__(self, df, column_casts, ranges, codis):
        """
        Initialize Measures class.
        
        Args:
            df (pd.DataFrame): Raw input data.
            column_casts (dict): Dictionary of column type mappings.
            ranges (dict): Valid value ranges for each code.
            codis (dict): Dictionary of relevant measurement codes.
        """
        super().__init__(df, column_casts)
        self.ranges = ranges
        self.codis = codis

    def _filter_by_codes(self):
        """Keep only rows with codes of interest."""
        self.df = self.df[self.df['Prova_codi'].isin(self.codis.keys())]

    @staticmethod
    def _filter_by_range(row, ranges):
        """Check if a value falls within a valid range for its code."""
        codi = row['Prova_codi']
        value = row['Prova_resultat']
        valid_range = ranges.get(codi)
        if pd.isna(value):  # Safety check for NaNs
            return False
        if valid_range:
            return valid_range[0] <= value <= valid_range[1]
        return False

    def _apply_range_filter(self):
        """Filter rows where the measurement value is within allowed range."""
        self.df = self.df[self.df.apply(self._filter_by_range, axis=1, args=(self.ranges,))]

    def process(self):
        """Run full processing pipeline for Measures data."""
        self.df = self.unify_missing()
        self.df = self.cast_columns()
        self._filter_by_codes()
        self._apply_range_filter()
        self.df.rename(columns={"Prova_data": "data", "Prova_resultat": "resultat", 
                                "Prova_codi": "codi_prova", "Prova_descripcio":"prova"}, inplace=True)

        return self.df