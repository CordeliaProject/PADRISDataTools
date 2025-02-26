################################################
# Patterns used to clean lab data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 24/01/2024
################################################
import pandas as pd

# Casts used to transform columns to the correct data type
casts = { 
    'codi_p': pd.Int64Dtype(),
    'any': pd.Int64Dtype(),
}

patterns_common_words = {
    'nc': [
        r"^(?:.*no.*)(?:calc(?:ulable)?|proce(?:deix|dent|sada)?|rebu(?:t|des)?|concloent|codi|valorable|realitza(?:da|t|r)?|possible|m[ue|o]stra).*",
        r".*mostra.*(?:coagulada|hem(?:oòó)(?:litzada|lisi)|rebutjada|insuficient|no.*[remesa|adient|estable|remitida]|contaminada|inade[quat|quada]|impedeix|vess?ada).*",
        r"^(?!.*\b(de|hipo)granulats?\b).*anu(?:lat|l·lat|lada|l·lada).*",
        r".*re(?:compte|cuento|sultat).*in(?:suficiente?|determinat|ferior).*",
        r".*--+.*",
    ],
    'positiu': [
        r".*pos(?:itiu|itiva).*",
    ],
    'negatiu': [
        r"(?!.*\bgram\b).*neg(?:atius?|ativa).*"
    ],
    'normal': [
        r".*\snormal\s.*"
        r"^(?:.*s[in|ense].*).*alteraci[oóóò]n.*$",	
    ],
    'baix': [
        r".*(?!.*\bno\b).*\b(?:ba(?:jo|ix))\b.*"
    ],
    'alt': [
        r".*(?!.*\bno\b).*\b(?:alt(?:o)?)\b.*"
    ],
    'microorganisme' : [
        r".*microorganisme\s?a[ïi]llat.*"
    ]
}

numeric_patterns = {
    'n1': r"-?([.,]?[0-9]+)+",  # General number pattern
    'n2': r"[<>]\s*(=?\s*)(([0-9]+([.,][0-9]+)?)|([0-9]*[.,][0-9]+))",  # Optional sign pattern and number, e.g., >100
    'n3': r"[0-9]{1,4}\s*[-]\s*[0-9]{1,4}",  # Range pattern, e.g., 100-200
    'n4': r"[<>]?\s*1[:/][0-9]{1,6}",  # Ratio type pattern, e.g., 1:1000
    'exponent': r"( ?[Xx*]{1} ?10(([Ee^][+-]?)|([+-]{1}))[0-9]{1,2})|([Ee][+-]?[0-9]{1,2})",  # Exponent handling
    'units': r"[a-zA-Z]{1,4}\s?\/\s?[a-zA-Z]{1,4}",  # Units pattern
}

# Dictionary to to identify wrongly written units and harmonize them
unit_patterns= {
    '%' : r'(?i)^(\d+([\.,]\d+))?\s*%\s*.*$',                                                                                                                        # %
    'ua' : r'(?i)^(u[\s\.\-]?\s*a(rb)?(?:itrary)?|a\.?u\.?)\s?[a-zA-Z\d]*$',                                                                                         # ua (unitats arbitraries)
    'ui' : r'(?i)^[\d\s,\.]*\s*(u[\s\.]?i(\.|nt\.?|\s)?|i(\.|nt\.?|\s)?u\.?)\s?[a-zA-Z\d]*$',                                                                        # ui (unitats internacionals)
    'uc' : r'(?i)^(?:uc|cu)\s?[a-zA-Z\d]*$',                                                                                                                         # uc (unitats corretgides)
    'ia' : r'(?i)^(?:ia|ai)\s?[a-zA-Z\d]*$',                                                                                                                         # ia (index aviditat)
    'µg/dl' : r'(?i)^(\d+([\.,]\d+)?\s*)?(µ|u|mc|micro)gr?\s?[\/7]\s*(dl|100\s?ml)\.?\s?[a-zA-Z\d]*$',                                                               # µg/dl
    'µg/ml' : r'(?i)^(\d+([\.,]\d+)?\s*)?(µ|u|mc|micro)gr?\s?[\/7]\s*ml\.?\s*\s?[a-zA-Z\d]*$',                                                                       # µg/ml 
    'µg/l' : r'(?i)^(\d+([\.,]\d+)?\s*)?(µ|u|mc|micro)gr?\s?[\/7]l\.?\s*\s?[a-zA-Z\d]*$',                                                                            # µg/l
    'mg/dl' : r'(?i)^(\d+([\.,]\d+)?\s*)?(m|mili)gr?\.?\s?[\/7](dL|100\s?mL)\.?\s?[a-zA-Z\d]*$',                                                                     # mg/dl
    'mg/ml' : r'(?i)^(\d+([\.,]\d+)?\s*)?(m|mili)gr?\s?[\/7]ml\s*\s?[a-zA-Z\d]*$',                                                                                   # mg/ml
    'mg/l' : r'(?i)^(\d+([\.,]\d+)?\s*)?(m|mili)gr?\s?[\/7]l\s*\s?[a-zA-Z\d]*$',                                                                                     # mg/l
    'ng/l' :r'(?i)^(\d+([\.,]\d+)?\s*)?(n|nano)gr?[a-zA-Z]*\s?[\/7]\s?l\s*[a-zA-Z\dóò]*$',                                                                           # ng/l
    'ng/dl' : r'(?i)^(\d+([\.,]\d+)?\s*)?(n|nano)gr?[a-zA-Z]*\s?[\/7]\s?(dl|100\s?mL)\.?\s*[a-zA-Z\dóò]*$',                                                          # ng/dl
    'ng/ml' : r'(?i)^(\d+([\.,]\d+)?\s*)?(n|nano)gr?[a-zA-Z]*\s?[\/7]\s?ml\.?[\s.]?[a-zA-Z\dóò]*$',                                                                  # ng/ml
    'pg/ml' : r'(?i)^(\d+([\.,]\d+)?\s*)?(p|pico)gr?\s?[\/7]\s?ml\.?[\s.]?[a-zA-Z\dóò]*$',                                                                           # pg/ml
    'mpl/ml' : r'(?i)^([a-zA-Z\d]+(?:,[a-zA-Z\d]+)*)?\s?\(?mpl.*\s?[\/7]\s?ml\.?\s?[a-zA-Z\d]*$',                                                                    # mpl/ml
    'g/dl' : r'(?i)^(\d+([\.,]\d+)?\s*)?gr?\s?[\/7]\s?(dl|100\s?ml)\.?[a-zA-Z\d]*$',                                                                                 # g/dl
    'g/ml' : r'(?i)^(\d+([\.,]\d+)?\s*)?gr?\s?[\/7]\s?ml\.?\s*[a-zA-Z\d]*$',                                                                                         # g/ml
    'g/l' : r'(?i)^(\d+([\.,]\d+)?\s*)?gr?\s?[\/7]\s?l\.?\s*[a-zA-Z\d]*$',                                                                                           # g/l
    'mmol/l' : r'(?i)^(?!.*(?:/mm?ol?|.*dl|.*ml))(\d+([\.,]\d+)?\s*)?(mm?ol?|mosmo?l)\s?[\/7]\s?[a-zA-Z\d]*l[a-zA-Z\d]*$',                                           # mmol/l
    'pmol/l' : r'(?i)^(?!.*(?:/mm?ol?|.*dl|.*ml))(\d+([\.,]\d+)?\s*)?(pm(ol)?)\s?[\/7]\s?[a-zA-Z\d]*l[a-zA-Z\d]*$',                                                  # pmol/l
    'mmol/dl' : r'(?i)^(?!.*(?:/mm?ol?))(\d+([\.,]\d+)?\s*)?(mm?ol?|mosmo?l)\s?[\/7]\s?[a-zA-Z\d]*dl[a-zA-Z\d]*',                                                    # mmol/dl
    'µmol/l' : r'^(\d+([\.,]\d+)?\s*)?[âá]?([âáuµ]|micro|mu)(m?ol?|mosmo?l)\s?[\/7]\s?[a-zA-Z\d]*dl[a-zA-Z\d]*',                                                     # µmol/l
    'ui/ml' : r'(?i)^(\d+([\.,]\d+)?\s*)?(u[\s\.]?i(\.|nt\.?|\s)?|i(\.|nt\.?|\s)?u\.?)\s?[\/7]\s?ml.*$',                                                             # ui/ml (unitats internacionals / ml)
    'ua/ml' : r'(?i)^(\d+([\.,]\d+)?\s*)?(u[\s\.\-]?\s*a(rb)?(?:itrary)?|a\.?u\.?)\s?[\/7]\s?ml.*$',                                                                 # ua/ml (unitats arbitraries / ml)
    'ui/l' : r'(?i)^(\d+([\.,]\d+)?\s*)?(u[\s\.]?i(\.|nt\.?|\s)?|i(\.|nt\.?|\s)?u\.?)\s?[\/7]\s?l.*$',                                                               # ui/l (unitats internacionals / l)
    'mui/l' : r'(?i)^(\d+([\.,]\d+)?\s*)?m(u[\s\.]?i(\.|nt\.?|\s)?|i(\.|nt\.?|\s)?u\.?)\s?[\/7]\s?l.*$',                                                             # mui/l (mili unitats internacionals / l)
    'ui/dl' : r'(?i)^(\d+([\.,]\d+)?\s*)?(u[\s\.]?i(\.|nt\.?|\s)?|i(\.|nt\.?|\s)?u\.?)\s?[\/7]\s?dl.*$',                                                             # ui/dl (unitats internacionals / dl)
    'kiu/l' : r'(?i)^(\d+([\.,]\d+)?\s*)?k(u[\s\.]?i(\.|nt\.?|\s)?|i(\.|nt\.?|\s)?u\.?)\s?[\/7]\s?l.*$',                                                             # kiu/l (kilo international units / l)
    'µui/ml' : r'(?i)^(\d+([\.,]\d+)?\s*)?[áâæ]?(µ|u|m(u|icro|c)?|[áâæ])\s*(i(nt|nternational)?\s?u\.?|u\.?(i(nt|nternational)?)?)\s?[\/7]\s?ml\s*[a-zA-Z]*$',       # µui/ml (micro-international units/ml)
    'eu/dl' : r'(?i)^(\d+([\.,]\d+)?\s*)?(e.?u.?|u.?e.?)\s?[\/7]\s?dl\s*[a-zA-Z]*$',                                                                                 # eu/dl (enzyme units/dl)
    'nmol/mmol' : r'(?i)^(\d+([\.,]\d+)?\s*)?nmol\s?[\/7]\s?(mmol?|mosmo?l)\s*[a-zA-Z]*',                                                                            # nmol/mmol
    'mmol/mol' : r'(?i)^(\d+([\.,]\d+)?\s*)?(m?mmol?|mosmo?l)\s?[\/7]\s?mol\s*[a-zA-Z]*',                                                                            # mmol/mol
    'mg/mmol' : r'(?i)^(\d+([\.,]\d+)?\s*)?mg\s?[\/7]\s?(m?mmol?|mosmo?l)\s*[a-zA-Z]*',                                                                              # mg/mmol
    'mol/mol' : r'(?i)^(\d+([\.,]\d+)?\s*)?mol\s?[\/7]\s?mol\s*[a-zA-Z]*',                                                                                           # mol/mmol
    'g/mol' : r'(?i)^(\d+([\.,]\d+)?\s*)?g\s?[\/7]\s?mol\s*[a-zA-Z]*',                                                                                               # g/mol
    '10^3/µl' : r'(?i)^x?\s?(10(\^|&|E|>)?[3³]|mil\.?|1000|k)(\s_)?u?\s?[\/7]\s?(µ|u|mc|micro)l\s*[a-zA-Z]*$',                                                       # 10^3/µl
    '10^3/mm3' : r'(?i)^x?\s?(10(\^|&|E|>)?[3³]|mil\.?|1000|k)(\s_)?u?\s?[\/7]\s?mm\s?.*$',                                                                          # 10^3/mm3
    '10^3/ml' : r'(?i)^x?\s?(10(\^|&|E|>)?[3³]|mil\.?|1000|k)(\s_)?u?\s?[\/7]\s?m(ili)?l\s*[a-zA-Z]*$',                                                              # 10^3/ml
    '10^3' : r'(?i)^x?\s?\s?(10(\^|&|E|>)?[3³]|mil\.?|1000|k)(\s_)?u?\s*[a-zA-Z]*$',                                                                                 # 10^3
    '10^6/µl' : r'(?i)^x?\s?(.*10.*6|mil(·li|i)[oó]|mill([oó]n)?).*[\/7]\s?(µ|u|mc|micro)l\s*[a-zA-Z]*$',                                                            # 10^6/µl
    '10^6/ml' : r'(?i)^x?\s?(.*10.*6|mil(·li|i)[oó]|mill([oó]n)?).*[\/7]\s?m(ili)?l\s*[a-zA-Z]*$',                                                                   # 10^6/ml
    '10^6/l' : r'(?i)^x?\s?(.*10.*6|mil(·li|i)[oó]|mill([oó]n)?).*[\/7]\s?l\s*[a-zA-Z]*$',                                                                           # 10^6/l
    '10^6/mm3' : r'(?i)^x?\s?(.*10.*6|mil(·li|i)[oó]|mill([oó]n)?).*[\/7]\s?mm\s?.*$',                                                                               # 10^6/mm3
    '10^6' : r'(?i)^x?\s?(.*10.*6|mil(·li|i)[oó]|mill([oó]n)?)$',                                                                                                    # 10^6
    '10^9/l' : r'(?i)^x?.*10?.*9.*/?l$',                                                                                                                             # 10^9/l
    '10^9' : r'(?i)^x?.*10.*9$',                                                                                                                                     # 10^9
    '10^12/l' : r'(?i)^x?.*10.*12.*/?l$',                                                                                                                            # 10^12/l
    'index' : r'(?i)\bã?[iíïãI][mn]dex\b|indice',                                                                                                                   # index
    'segons' : r'(?i)\b(s(?:eg(?:ond|ons?|undos?)?|g(?:u)?)|^s$)\b',                                                                                                 # segons
    'ratio' : r'(?i)^\[?(r(a[oöóò]|[aàá]tio?)|(in)?r)$',                                                                                                             # ratio
    'titol' :  r'(?i)^\[?(t[íìiï](tol|tulo))$',                                                                                                                      # titol
    'ph' : r'(?i)^.*?ph.*$',                                                                                                                                         # ph
    'mmol/24h' : r'(?i)mmol\s?[\/7]\s?\s?(24\s?h(or[ae]s)?|d(ia)?)$',                                                                                                # mmol/24h
    'µg/24h' : r'(?i)[â]?(u|mc|µ|mu)g\s?[\/7]\s?(24\s?h(or[ae]s)?|d(ia)?)$',                                                                                         # µg/24h
    'mg/24h' : r'(?i)mgr?\s?[\/7]\s?(24\s?h(or[ae]s)?|d(ia)?)$',                                                                                                     # mg/24h
    'ui/24h' : r'(?i)(u[\s\.]?i(\.|nt\.?|\s)?|i(\.|nt\.?|\s)?u\.?)\s?[\/7]\s?(24\s?h(or[ae]s)?|d(ia)?)$',                                                            # ui/24h
    'g/24h' : r'(?i)^gr?\s?[\/7]\s?(24\s?h(or[ae]s)?|d(ia)?)$',                                                                                                      # g/24h
    'g/12h' : r'(?i)gr?\s?[\/7]\s?12\s?h(or[ae]s)?$',                                                                                                                # g/12h
    'nmol/24h' : r'(?i)^nmol\s?[\/7]\s?(24\s?h(or[ae]s)?|d(ia)?)$',                                                                                                  # nmol/24h
    'meq/24h' : r'(?i)([\d]+(,[\d]+)*)?mequ?\s?[\/7]\s?(24\s?h(or[ae]s)?|d(ia)?)$',                                                                                  # meq/24h
    'ml/min/1.73m2' : r'(?i)^(ml|mil?)\s?(\/7)?\s?min\s?(\/7)?\s1[.,]73\s*m?[²2]$',                                                                                  # ml/min/1.73m2
    'ml/min' : r'(?i)^ml\s?[\/7]\s?m(i|in|n|inut)$',                                                                                                                 # ml/min
    'ng/ml/h' : r'(?i)^ng\s?[\/7]\s?ml\s?[\/7]\s?h(ora)?$',                                                                                                          # ng/ml/h
    'cel/mm3': r'(?i)^(\d+([\.,]\d+)?\s*)?(cel|c[iy]l|hem|er[yi]|leu).*[/7]\s?(mm\s?[3]?|c([uú]bic)?)?\.?$',                                                         # cel/mm3
    'cel/µl' : r'(?i)^(\d+([\.,]\d+)?\s*)?(cel|c[iy]l|hem|er[yi]|leu).*[/7]\s?â?(mc|micro|u|µ)\s?l\.?$',                                                             # cel/µl
    'cel/camp' : r'(?i)^(per\s?camp|x?\s?camp|(cel)?\s?[\/7]\s?camp)$',                                                                                              # cel/camp
    'copies/ml' : r'(?i)^.*c.?pies.*\s?[\/7]\s?(ml)[\s]?.*$',                                                                                                        # copies/ml
    'g' : r'(?i)^gr?$',                                                                                                                                              # g
    'mg' : r'(?i)^mgr?$',                                                                                                                                            # mg
    'µl' : r'(?i)^[â]?(micro|mc|[æáµu]|um|mu)l$',                                                                                                                    # µl
    'mm3' : r'(?i)^mm[\s]?(c|3|c[uú]bic|³)$',                                                                                                                        # mm3
    'pg' : r'(?i)^pgr?$',                                                                                                                                            # pg
    'µg/g' : r'(?i)^(?!.*µg/ghb)[áâ]?(mc|micro|u|µ)g.*\s?[\/7]\s?gr?$',                                                                                              # µg/g
    'g/g' : r'(?i)^g.*\s?[\/7]\s?gr?.*$',                                                                                                                            # g/g
    'mg/g' : r'(?i)^u?mg.*\s?[\/7]\s?gr?.*$',                                                                                                                        # mg/g
    'mg/mg' : r'(?i)^u?mg.*\s?[\/7]\s?mg?.*$',                                                                                                                       # mg/mg
    'mg/kg' : r'(?i)^u?mg.*\s?[\/7]\s?kg.*$',                                                                                                                        # mg/kg
    'µg/mg' : r'(?i)^(?!.*µg/ghb|umg/mg)â?(mc|micro|u|µ|mu)g.*\s?[\/7]\s?.*mgr?.*$',                                                                                 # µg/mg
    'mmol/kg' : r'(?i)^m(os)?m(ol)?\s?[\/7]\s?.*kgr?.*',                                                                                                             # mmol/kg
    'gpl/ml' : r'(?i)^(u\s?)?gpl.*\s?[\/7]\s?ml',                                                                                                                    # gpl/ml
    'µkat/l' : r'(?i)^[uµ]kat\s?[\/7]\s?l',                                                                                                                          # µkat/l
    'mu/10^9 eritrocits' : r'(?i)^mu\s?[\/7]\s?\s?(10?.*9.*|mil.*|1000\s?mil.*)',                                                                                    # mu/10^9 eritrocits
    'meq/l' : r'(?i)^([\d]+(,[\d]+)*)?mequ?\s?[\/7]\s?\s?l',                                                                                                         # meq/l
    'mmhg' : r'(?i)^mm\s?hg',                                                                                                                                        # mmHg
    'fl' : r'(?i)^fl(\.)?',                                                                                                                                          # fl 
}