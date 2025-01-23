################################################
# Factors used to clean lab data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 10/12/2024
################################################

# This script is not used directly, in here you'll find the factors used to transform from one unit to another

# Dictionary to use known base units.
base_units = {"l",      # Volume
              "mm3",    # Volume
              "g",      # Mass
              "mol",    # Moles
              "m",      # Molarity
              "s",      # Time (seconds)
              "ui",     # Enzymatic activity
              "eq",     # Equivalents
              "osmol",  # Osmol
              "kat",    # Enzymatic activity
              "ph"      # pH
              }

# Dictionary to transform inside the same unit in different magnitudes
factor_dict = {
     "p": 1e-12,
     "n": 1e-9,
     "µ": 1e-6,
     "m": 1e-3,
     "d": 1e-1,
     "": 1,
     "k": 1e3,
}

# Dictionary to to identify wrongly written units and harmonize them
patterns_unitats = {
    r'^(([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?%.*|fracci[oó])$': '%',                                                       # %
    r'^(u\.?a|a\.?u|u[\.\s]?arb.*)$': 'ua',                                                                             # ua (unitats arbitraries)
    r'^([\d]+(,[\d]+)*)?[\s]?(u\.?i|i\.?u)$': 'ui',                                                                     # ui (unitats internacionals)
    r'^(uc|cu)$': 'uc',                                                                                                 # uc (unitats corretgides)
    r'^(ia|ai)$': 'ia',                                                                                                 # ia (index aviditat)
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?[â]?(micro|mc|[æáµu]|um|mu)g[/7\s]?(dl\s?[a-zA-Z\d\(]*|100\s?ml)$': 'µg/dl', # µg/dl
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?[â]?(micro|mc|[æáµu]|um|mu)g[/7\s]?ml\s?[a-zA-Z\d\(]*$': 'µg/ml',           # µg/ml 
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?[â]?(micro|mc|[æáµu]|um|mu)g[/7\s]?l\s?[a-zA-Z\d\(]*$': 'µg/l',             # µg/l
    r'^([a-zA-Z\d]+([,-][a-zA-Z\d]+)*)?[\s]?\(?mq?gr?[/7\s]?(dl\s?[a-zA-Z\d]*|100\s?ml)$':'mg/dl',                      # mg/dl
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?mgr?[/7\s]?ml\s?[a-zA-Z\d]*$':'mg/ml',                                      # mg/ml
    r'^mgr?[\.\,]?[/7\s]?l\s?[a-zA-Z\d]*$':'mg/l',                                                                      # mg/l
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?(n|nano)gr?.*[/7\s]l\s?[a-zA-Z\d]*$':'ng/l',                                # ng/l
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?(n|nano)gr?.*[/7\s](dl\s?[a-zA-Z\d]*|100\s?ml)\s?[a-zA-Z\d]*$':'ng/dl',     # ng/dl
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?(n|nano)gr?.*[/7\s]?ml\s?[a-zA-Z\dóò]*$':'ng/ml',                           # ng/ml
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?(p|pico)gr?.*[/7\s]?ml\s?[a-zA-Z\d]*$':'pg/ml',                             # pg/ml
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?mpl.*[/7\s]?ml\s?[a-zA-Z\d]*$':'mpl/ml',                                    # mpl/ml
    r'^([\d]+(,[\d]+)*)?[\s]?gr?[/7\s]?(dl|100\s?ml)$':'g/dl',                                                          # g/dl
    r'^([\d]+(,[\d]+)*)?[\s]?gr?[/7\s]?ml$':'g/ml',                                                                     # g/ml
    r'^([\d]+(,[\d]+)*)?[\s]?gr?[/7\s]?l$':'g/l',                                                                       # g/l
    r'^(?!.*/mm?ol?|.*dl)m{1,2}(os)?m(ol?)?[/7].*l.*':'mmol/l',                                                         # mmol/l
    r'^pm(ol?)?\.?[/7].*l.*':'pmol/l',                                                                                  # pmol/l
    r'^(?!.*/mm?ol?)m(os)?m(ol?)?[/7].*dl.*':'mmol/dl',                                                                 # mmol/dl
    r'^([\d]+(,[\d]+)*)?(u(i|\.?int\.?)|iu)[/7]m\,?l.*$':'ui/ml',                                                       # ui/ml (unitats internacionals / ml)
    r'^([\d]+(,[\d]+)*)?(u(a|\.?int\.?)|au)[/7]ml.*$':'ua/ml',                                                          # ua/ml (unitats arbitraries / ml)
    r'^([\d]+(,[\d]+)*)?\s?(ui?|\.?int\.?u|u\.?int\.?|iu)[/7]l.*$':'ui/l',                                              # ui/l (unitats internacionals / l)
    r'^m(ui?|\.?int\.?u\.?|\.?u\.?int\.?|iu)[/7]l.*$':'mui/l',                                                          # mui/l (mili unitats internacionals / l)
    r'^([\d]+(,[\d]+)*)?\s?(ui?|\.?int\.?u\.?|u\.?int\.?|iu)[/7]dl.*$':'ui/dl',                                         # ui/dl (unitats internacionals / dl)
    r'^k(int\.?u\.?|iu|u(?:\.?i\.?)?)?[7/]l{1,2}':'kiu/l',                                                              # kiu/l (kilo international units / l)
    r'^\(?[áâæ]?(mc?|micro\s?|u|µ|[áâæ])(ui?|iu)[/7\s]?ml$':'µui/ml',                                                   # µui/ml (micro-international units/ml)
    r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?e.?u.?[/7\s]?dl$':'eu/dl',                                                  # eu/dl (enzyme units/dl)
    r'^[âá]?([âáuµ]|micro|mu)mol/l$':'µmol/l',                                                                          # µmol/l
    r'^nmol/*mmol\s?.*':'nmol/mmol',                                                                                    # nmol/mmol
    r'^m?mmol/*mol\s?.*':'mmol/mol',                                                                                    # mmol/mol
    r'^mg/mmol\s?(cre)?.*':'mg/mmol',                                                                                   # mg/mmol
    r'^mol/mol.*':'mol/mol',                                                                                            # mol/mmol
    r'^g/mol\s?(cre)?.*':'g/mol',                                                                                       # g/mol
    r'^x?.*(10.*[3³]|mil|1000|^m|^k[/7]).*/*[áâ]*([µuá]l|mcl)$':'10^3/µl',                                              # 10^3/µl
    r'^x?.*(10.*[3³]|mil|1000|^m[/7]|^k[/7]).*/*mm[\s]?.*$':'10^3/mm3',                                                 # 10^3/mm3
    r'^x?.*(10.*[3³]|mil|1000|^m[/7]|^k[/7]).*/*(ml|microl)[\s]?.*$':'10^3/ml',                                         # 10^3/ml
    r'^x?.*(10[^xe]?[3³]|mil|1000)$':'10^3',                                                                            # 10^3
    r'^x?.*10.*6.*/*[áâ]*([µuá]l|mcl)$': '10^6/µl',                                                                     # 10^6/µl
    r'^x?.*10.*6.*/*ml$': '10^6/ml',                                                                                    # 10^6/ml
    r'^x?.*10.*6.*/?l$': '10^6/l',                                                                                      # 10^6/l
    r'^x?.*10.*6.*/*mm[\s]?.*$':'10^6/mm3',                                                                             # 10^6/mm3
    r'^x?.*10.*6$': '10^6',                                                                                             # 10^6
    r'^x?.*10?.*9.*/?l$': '10^9/l',                                                                                     # 10^9/l
    r'^x?.*10.*9$': '10^9',                                                                                             # 10^9
    r'^x?.*10.*12.*/?l$': '10^12/l',                                                                                    # 10^12/l
    r'\bã?[iíïãI][mn]dex\b|indice': 'index',                                                                           # index
    r'\b(s(?:eg(?:ond|ons?|undos?)?|g(?:u)?)|^s$)\b':'segons',                                                          # segons
    r'\b^[Nn]e?g(atiu)?s?\b$':'negatiu',                                                                                # negatiu
    r'^\[?(r(a[oöóò]|[aàá]tio?)|(in)?r)$':'ratio',                                                                      # ratio
    r'^.*?ph.*$':'ph',                                                                                                  # ph
    r'mmol/\s?(24\s?h(or[ae]s)?|d(ia)?).*': 'mmol/24h',                                                                 # mmol/24h
    r'[â]?(u|mc|µ|mu)g/\s?(24\s?h(or[ae]s)?|d(ia)?).*': 'µg/24h',                                                       # µg/24h
    r'mgr?/\s?(24\s?h(or[ae]s)?.*|d(ia)?)': 'mg/24h',                                                                   # mg/24h
    r'(u\.?i|i\.?u)/\s?(24\s?h(or[ae]s)?.*|d(ia)?)':'ui/24h',                                                           # ui/24h
    r'gr?/\s?(24\s?h(or[ae]s)?.*|d(ia)?)':'g/24h',                                                                      # g/24h
    r'gr?/\s?12\s?h(or[ae]s)?.*':'g/12h',                                                                               # g/12h
    r'nmol/\s?(24\s?h(or[ae]s)?.*|d(ia)?)':'nmol/24h',                                                                  # nmol/24h
    r'([\d]+(,[\d]+)*)?mequ?[/7](24\s?h(or[ae]s)?.*|d(ia)?)':'meq/24h',                                                 # meq/24h
    r'\b(ml|mil?)(?:[i]*|il)?[7/\(]*m(?:i?n?)?[\)*]?/?1[.,\']7[23]m?(?:\^?2|[m²&2e2]*)?.*\b': 'ml/min/1.73m2',          # ml/min/1.73m2
    r'^ml[/7]m(i|in|n|inut)': 'ml/min',                                                                                 # ml/min
    r'^ng[/7]ml[7/]h(ora)?$': 'ng/ml/h',                                                                                # ng/ml/h
    r'^1?(x\s?)?[/7]mm[\s]?(c|3|c[uú]bic|³)':'cel/mm3',                                                                 # cel/mm3
    r'^1?u?[/7]â?(mc|micro|u|µ)[\s]?l':'cel/µl',                                                                        # cel/µl
    r'^.*(hem:*|c[eièé]l).*[/7]mm.*':'cel/mm3',                                                                         # cel/mm3
    r'^.*(hem:*|c[eièé]l).*[/7]â?(mc|micro|u|µ)[\s]?l':'cel/µl',                                                        # cel/µl
    r'^.*er[iy][/7][áâ]?(mc|micro|u|µ)[\s]?l':'cel/µl',                                                                 # cel/µl
    r'^.*leu.*[/7][áâ]?(mc|micro|u|µ)[\s]?l':'cel/µl',                                                                  # cel/µl
    r'^(per\s?camp|x?\s?camp|(cel)?\/\s?camp)$':'cel/camp',                                                             # cel/camp
    r'^.*c..?pies.*[/7](ml)[\s]?.*':'copies/ml',                                                                        # copies/ml
    r'^gr?$':'g',                                                                                                       # g
    r'^[â]?(micro|mc|[æáµu]|um|mu)l$':'µl',                                                                             # µl
    r'^mm[\s]?(c|3|c[uú]bic|³)$':'mm3',                                                                                 # mm3
    r'^pgr?$':'pg',                                                                                                     # pg
    r'^gr?/100\s?ml$':'g/100ml',                                                                                        # g/100ml
    r'^(?!.*µg/ghb)[áâ]?(mc|micro|u|µ)g.*[/7]gr?':'µg/g',                                                               # µg/g
    r'^g.*[/7]gr?.*':'g/g',                                                                                             # g/g
    r'^u?mg.*[/7]gr?.*':'mg/g',                                                                                         # mg/g
    r'^u?mg.*[/7]mg?.*':'mg/mg',                                                                                        # mg/mg
    r'^u?mg.*[/7]kg.*':'mg/kg',                                                                                         # mg/kg
    r'^(?!.*µg/ghb|umg/mg)â?(mc|micro|u|µ|mu)g.*[/7].*mgr?.*':'µg/mg',                                                  # µg/mg
    r'^m(os)?m(ol)?[/7].*kgr?.*':'mmol/kg',                                                                             # mmol/kg
    r'^(u\s?)?gpl.*[/7]ml':'gpl/ml',                                                                                    # gpl/ml
    r'^[uµ]kat[/7]l':'µkat/l',                                                                                          # µkat/l
    r'^mu[/7]\s?(10?.*9.*|mil.*|1000\s?mil.*)':'mu/10^9 eritrocits',                                                    # mu/10^9 eritrocits
    r'^([\d]+(,[\d]+)*)?mequ?[/7]\s?l':'meq/l',                                                                         # meq/l
    r'^mm\s?hg':'mmhg',                                                                                                 # mmHg
    r'^fl(\.)?':'fl',                                                                                                  # fl
    
}