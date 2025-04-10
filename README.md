# PADRISDataTools

**IMPORTANT**: The individual id column **MUST** be the first column. If not, the tool will not detect it. Also, columns MUST be named as PADRIS names them.

PADRISDataTools is a collection of Python scripts designed to clean, preprocess, and manage data from PADRIS. This toolset supports the following PADRIS datasets:

- Ensurance data – Assegurats

- Mortality data – Mortalitat

- CMBD data – Episodis, Diagnostics, Procediments

- Measurements data – Mesures (e.g., height, weight, blood pressure)

- Laboratory data – Laboratori

## Objective
The main goal of PADRISDataTools is to standardize and prepare PADRIS data for analysis. It applies two common preprocessing steps across all datasets:

- Unification of missing values

- Conversion to more analysis-friendly data types

Each data type may then undergo additional custom processing steps to ensure usability. The scripts return the original DataFrame with new or modified columns and data types, making the data ready for further work.

### Special Case: Laboratory Data
For the Laboratori dataset, two processing modes are available:

- Base processing – Cleans and standardizes the lab data.

- Filtered processing – Requires an external conversion file.

This mode filters the lab data based on the conversion file and transforms the values into the desired units.


## Installation

To install PADRISDataTools, follow the following steps:

1. Clone this repository to your local machine:

```
git clone https://github.com/CordeliaProject/PADRISDataTools.git
```

2. Install the required dependencies, taking into account that  `python --version == 3.11.9`:
```
pip install -r requirements.txt
```

## Usage

PADRISDataTools should be as easy to use as possible. The arguments you should take into account are:

**IMPORTANT**: The individual id column **MUST** be the first column. If not, the tool will not detect it. Also, columns MUST be named as PADRIS names them.

```
    inpath (str): Path to the input file
    outpath (str): Path to the output file
    entity (str): Type of entity. Options: 'Assegurats', 'Episodis', 'Diagnostics', 'Procediments', 'Mortalitat', 'Laboratori'
    episodis (str): [Optional] Required only for 'Diagnostics' or 'Procediments'.
                       Path to the raw 'Episodis' file.
    lab_option (str): [Optional] Used only when entity is 'Laboratori'.
                       If set to 'filter', enables lab test filtering and unit conversion.
    lab_conversion (str): [Optional] Required if lab_option is 'filter'.
                       Path to the conversion file.
```

The general usage will be:

```
python3 main.py <inpath> <outpath> <entity>
```

### Special cases

#### Laboratorti `filter` mode
If you're working with Laboratori data and want to use the `filter` mode, you'll need to provide the path to a **conversion file**, which is an excel file with just one sheet.

```
python3 main.py <inpath> <outpath> <entity> 'filter' <lab_conversion>
```

The conversion file must include the following columns:

```
    codi_prova (str): Test code (must match PADRIS lab codes)
    from_unit (str): Original unit of the measurement
    factor (float): Multiplication factor to convert to the desired unit
    to_unit (str): Target unit for conversion
    group (str): [optional] Classification label to group tests
```

You must add at least one row per test you wish to filter. You don't need to repeat entries for unit conversions that share the same base if a matching line already exists.

[Example conversion file](https://docs.google.com/spreadsheets/d/1psceKUL4BeNs7xuVsmPr4IceuKPLsgO_/edit?usp=sharing&ouid=113699313160507628266&rtpof=true&sd=true).


#### Diagnostics or Procediments
For Diagnostics or Procediments, the tool requires access to the raw Episodis data to check for inconsistencies.

```
python3 main.py <inpath> <outpath> <entity> <episodis>
```

Make sure the <episodis> argument points to the path of the unprocessed Episodis dataframe


## About PADRIS
The PADRIS program (Programa d'Analítica de Dades per a la Recerca i la Innovació en Salut) aims to make health data accessible for research purposes, aligning with legal and ethical frameworks while maintaining transparency towards the citizens of Catalonia.