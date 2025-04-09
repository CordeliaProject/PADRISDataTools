# Main function to use to remove date and diagnostic outliers in Primaria - PADRIS
import pandas as pd
from source.utils.outliers_primaria.functions import *
import sys

def main():
    """ Main function to remove primaria outliers."""
    args = sys.argv[1:]

    if len(args) != 3:
        print("Usage: python3 main.py <inpath primaria> <inpath mortalitat> <oupath>")
        sys.exit(1)

    primaria, mortalitat, outpath = args[0], args[1], args[2]
    
    # Read the reference for CIM10 and CIM9
    cie10_df = pd.read_excel(r".\cie_reference\Diagnosticos_ES2024_TablaReferencia_30_06_2023.xlsx", sheet_name='ES2024 Finales', usecols=['Código'])
    cie9_df = pd.read_excel(r".\cie_reference\CIE9MC_9_2014_REF_20210601_2362183957514564327.xls", sheet_name='cie9mc2014', usecols=['Tab.D'])
    # From https://www.eciemaps.sanidad.gob.es/documentation at 09/04/2025 -> Tablas de Referencia

    # Remove non coherent cie codes
    primaria_first_filt = remove_non_coherent_cie(primaria, cie9_df, cie10_df)

    # Remove non coherent dates
    primaria_filt = remove_date_outliers(primaria_first_filt, mortalitat)

    # Output file
    primaria_filt.to_csv(outpath, sep = "|", index = False)