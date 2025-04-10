# PADRISDataTools

PADRISDataTools is a collection of Python scripts designed to clean, preprocess, and manage data from PADRIS. This toolset supports the following PADRIS datasets:

- Ensurance data – Assegurats

- Mortality data – Mortalitat

- CMBD data – Episodis, Diagnostics, Procediments

- Measurements data – Mesures (e.g., height, weight, blood pressure)

- Laboratory data – Laboratori

### Objective
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

```
    inpath (str): Path to the input file.
    outpath (str): Path to the output file.
    entity (str): Type of entity ('Assegurats', 'Episodis', 'Diagnostics', 'Procediments', 'Mortalitat', 'Laboratori').
    episodis (str) - OPT: Path to episodis file whn option is Diagnostics or Procediments.
    lab_option (str) - OPT: Used only if entity == 'Laboratori'. If set to 'filter', applies filtering before processing.
    lab_conversion (str) - OPT: Used only if entity == 'Laboratori'. If set to 'filter' add path to conversion file.
```

The general usage will be:

```
python3 main.py <inpath> <outpath> <entity>
```

### Special cases

1- If you are working with 'Laboratori' data from PADRIS, and you want to use the 'filter' option. You will need to add the path to a [conversion file](https://drive.google.com/file/d/1z6AZO_aRNcDSPrr4iIxXQJRlPYDJPU9W/view?usp=sharing).

```
python3 main.py <inpath> <outpath> <entity> 'filter' <lab_conversion>
```

The conversion file should look like ## TO DO

2- If you are working with 'Diagnostics' or 'Procediments' ## TO DO

## About PADRIS
The PADRIS program (Programa d'Analítica de Dades per a la Recerca i la Innovació en Salut) aims to make health data accessible for research purposes, aligning with legal and ethical frameworks while maintaining transparency towards the citizens of Catalonia.