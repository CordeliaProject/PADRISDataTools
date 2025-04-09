# PADRISDataTools

PADRISDataTools is a collection of scripts designed to clean, preprocess, and manage data from PADRIS.

## About PADRIS
The PADRIS program (El Programa d'Analítica de Dades per a la Recerca i la Innovació en Salut) aims to make health data accessible for research purposes, aligning with legal and ethical frameworks while maintaining transparency towards the citizens of Catalonia.

## Installation

To install PADRISDataTools, follow the followingg steps:

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

Then, there are two special cases:

1- If you are working with 'Laboratori' data from PADRIS, and you want to use the 'filter' option. You will need to add the path to a conversion file.

```
python3 main.py <inpath> <outpath> <entity> 'filter' <lab_conversion>
```

The conversion file should look like ## TO DO

2- If you are working with 'Diagnostics' or 'Procediments' ## TO DO