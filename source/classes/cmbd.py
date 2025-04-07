# Class for the CMBD tables from PADRIS
from source.classes.common import CommonData
import pandas as pd

class Episodis(CommonData):
    """
    This class will deal with the processes related to the Episodis table from PADRIS.
    """

    def __init__(self, df, column_casts):
        """ Constructor for the Assegurats class. """
        super().__init__(df, column_casts)  # Pass outpath to parent constructor

    def _fix_inconsistencies(self):
        """ 
        Detect inconsistencies in episodi identifiers.
        Fix episodi identifiers before 2018 to a positive value.
        """
        if 'any_referencia' in self.df.columns and 'episodi_id' in self.df.columns:
            self.df.loc[
            (self.df['any_referencia'] >= 2018),
            'episodi_id'] = self.df['episodi_id'].abs()

        return self.df

    def process(self):
        """ Function to process Episodis data."""
        self.df = self.unify_missing_values()
        self.df = self.cast_columns()

        if 'data_alta' in self.df.columns:
            self.df['any_referencia'] = pd.to_numeric(self.df['data_alta'].dt.year, errors='coerce')

        self.df = self._fix_inconsistencies()

        return self.df


class DiagnosticsProcediments(CommonData):
    """
    This class will deal with the processes related to the Diagnostics table from PADRIS.
    """

    def __init__(self, df, column_casts, entity_name, episodis_df):
        """
        Constructor for the DiagnosticsProcediments class. 
        
        Args:
            df (pd.DataFrame): DataFrame to be processed.
            column_casts (dict): Dictionary of columns and their target data types.
            entity_name (str): Name of the entity, either "Diagnostics" or "Procediments".
            episodis_df (pd.DataFrame): DataFrame containing episodis data.
        """
        super().__init__(df, column_casts)
        self.episodis = episodis_df
        self.entity_name = entity_name

    def _get_catalog_mapping(self):
        """ Return the catalog mapping for Diagnostics or Procediments. """
        return {
            "Diagnostics": {"post_2018": "CIM10MC", "pre_2018": "CIM9MC"},
            "Procediments": {"post_2018": "CIM10SCP", "pre_2018": "CIM9MC"}
        }.get(self.entity_name, {})

    def _get_label_column(self):
        """ Return the label column ('dx' or 'px') based on entity_name. """
        return 'dx' if self.entity_name == "Diagnostics" else 'px'

    def _get_most_frequent(self, group):
        """ Get the most frequent value in a group. """
        return group.mode().iloc[0] if not group.mode().empty else None

    def _fix_inconsistencies(self):
        """ 
        Detect inconsistencies in episodis identifiers (diagnostics or procedures).
        Fix inconsistencies for episodis identifiers before 2018 to ensure correct mappings.
        """
        label_col = self._get_label_column()
        catalogs = self._get_catalog_mapping()

        # Merge the episodis dataframe with the main df
        merged = pd.merge(self.episodis, self.df, on="episodi_id", how="right")

        # Remove incorrect mappings based on year and catalog
        remove_condition = (
            (merged['any_referencia'] >= 2018) & (merged[f'catalegcim_{label_col}'] == catalogs["pre_2018"]) |
            (merged['any_referencia'] < 2018) & (merged[f'catalegcim_{label_col}'] == catalogs["post_2018"])
        )
        fixed_merged = merged[~remove_condition].copy()

        # Update episodis_id for post-2018 records
        update_condition = (fixed_merged['any_referencia'] >= 2018) & (fixed_merged[f'catalegcim_{label_col}'] == catalogs["post_2018"])
        fixed_merged.loc[update_condition, 'episodi_id'] = fixed_merged['episodi_id'].abs()

        # Drop unnecessary columns
        columns_to_drop = ["codi_p", "any_referencia"]
        fixed_merged.drop(columns=[col for col in columns_to_drop if col in fixed_merged.columns], inplace=True)

        # Group by label columns and find the most common label
        group_cols = [f"{label_col}_c", f"catalegcim_{label_col}"]
        if all(col in fixed_merged.columns for col in group_cols):
            most_common_label = self.df.groupby(group_cols)[label_col].agg(self._get_most_frequent)
            fixed_merged[label_col] = fixed_merged.set_index(group_cols).index.map(most_common_label.to_dict())

        # Remove duplicates
        fixed_merged.drop_duplicates(inplace=True)
        
        return fixed_merged

    def process(self):
        """ Process Diagnostics or Procediments data. """
        self.df = self.unify_missing()
        self.df = self._fix_inconsistencies()
        self.df = self.cast_columns()
        
        return self.df