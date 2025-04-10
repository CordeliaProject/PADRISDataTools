# Class for the Mesures tables from PADRIS
from source.classes.common import CommonData
from source.utils.mesures_info import unitats 
import pandas as pd

class Mesures(CommonData):
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

    def _check_if_mesures(self):
        """Check if the columns correspond to a Mesures file; if not, raise an error."""
        required_cols = {"Prova_data", "Prova_codi", "Prova_descripcio", "Prova_resultat"}
        if not required_cols.issubset(self.df.columns):
            raise ValueError("⚠️ The data does not correspond with a Mesures file or it does not have the corresponding columns.")

    def _filter_by_codes(self):
        """Keep only rows with codes of interest."""
        self.df = self.df[self.df['Prova_codi'].isin(self.codis.keys())]

    @staticmethod
    def _filter_by_range(row, ranges):
        """Check if a value falls within a valid range for its code."""
        codi = row['Prova_codi']
        value = row['Prova_resultat']
        valid_range = ranges.get(codi)

        try:
            if pd.isna(value):
                return False
            value = float(value)
            if valid_range:
                return valid_range[0] <= value <= valid_range[1]
        except (ValueError, TypeError):
            # You can log or print a warning here if needed
            return False

        return False

    def _apply_range_filter(self):
        """Filter rows where the measurement value is within allowed range."""
        self.df = self.df[self.df.apply(self._filter_by_range, axis=1, args=(self.ranges,))]

    def _add_unit(self, unitats_mesures):
        """ Add unit from the codis file to the dataframe"""
        self.df['unitat'] = self.df['Prova_codi'].map(unitats_mesures)
        return self.df

    def process(self):
        """Run full processing pipeline for Measures data."""
        self._check_if_mesures()
        self.df = self.unify_missing()
        self.df = self.cast_columns()
        self.df = self._filter_by_codes()
        self.df = self._apply_range_filter()
        self.df = self._add_unit(unitats)
        self.df.rename(columns={"Prova_data": "data", "Prova_resultat": "resultat", 
                                "Prova_codi": "codi_prova", "Prova_descripcio":"prova"}, inplace=True)

        return self.df