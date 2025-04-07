# Class for the Lab tables from PADRIS
from classes.common import CommonData
from lab_processing.clean_lab import *
from lab_processing.patterns import *


class Lab(CommonData):
    """
    This class will deal with the processes related to the lab table from PADRIS.
    """

    def __init__(self, df, column_casts):
        """ Constructor for the LAB class. """
        super().__init__(df, column_casts)

    def _fill_missing(self):
        """ Fill missing values in the lab_resultat with nocalc. """
        self.df["lab_resultat"] = self.df["lab_resultat"].fillna("nocalc")

        return self.df

    def _prepare_lab_data(self):
        """ Prepare the lab data for processing. """
        self.df = self.df[['codi_p','peticio_id','Any_prova','Data_prova','lab_prova_c','lab_prova','lab_resultat','unitat_mesura','ref_min','ref_max','clean_result','clean_unit','comentari','comentari_unitat','num_type']]
        self.df = self.df.rename(columns={"Any_prova": "any", "Data_prova": "data", "lab_resultat": "resultat", "lab_prova_c": "codi_prova", "lab_prova":"prova"})

        return self.df

    def process(self):
        """ Function to process Assegurats data."""
        self.df = self.unify_missing() # Unify missing values to be pd.NA
        self.df = self._fill_missing() # Fill missing values in the lab_resultat col with nocalc

        # Process the lab data
        self.df = clear_typos(self.df) # Clear typos in the lab data
        self.df = handle_extra_variables(self.df, patterns_common_words, numeric_patterns)
        self.df = classify_numeric_results(self.df, numeric_patterns) # Classify numeric results
        self.df = standardize_numeric_results(self.df) # Standardize numeric results
        self.df = standardize_unit(self.df, unit_patterns) # Standardize units
        self.df = standardize_name(self.df) # Standardize names
        self.df = standardize_reference_values(self.df) # Standardize reference values
        self.df = standardize_peticio_id(self.df) # Standardize peticio_id
        self.df = self._prepare_lab_data()
        self.df = self.cast_columns()

        return self.df