################################################
# Patterns used to clean lab data
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 24/01/2024
################################################

patterns_common_words = {
    'nc': [
        r"^(?:.*no.*)(?:calc(?:ulable)?|proce(?:deix|dent|sada)?|rebu(?:t|des)?|concloent|codi|valorable|realitza(?:da|t|r)?|possible|m[ue|o]stra).*",
        r".*mostra.*(?:coagulada|hem(?:oòó)(?:litzada|lisi)|rebutjada|insuficient|no.*[remesa|adient|estable|remitida]|contaminada|inade[quat|quada]|impedeix|vess?ada).*",
        r"^(?!.*\b(de|hipo)granulats?\b).*anu(?:lat|l·lat|lada|l·lada).*",
        r".*re(?:compte|cuento|sultat).*in(?:suficiente?|determinat|ferior).*"
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
    '%' : r'^(([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?%.*|fracci[oó])$',                                                        # %
    'ua' : r'^(u\.?a|a\.?u|u[\.\s]?arb.*)$',                                                                              # ua (unitats arbitraries)
    'ui' : r'^([\d]+(,[\d]+)*)?[\s]?(u\.?i|i\.?u)$',                                                                      # ui (unitats internacionals)
    'uc' : r'^(uc|cu)$',                                                                                                  # uc (unitats corretgides)
    'ia' : r'^(ia|ai)$',                                                                                                  # ia (index aviditat)
    'µg/dl' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?[â]?(micro|mc|[æáµu]|um|mu)g[/7\s]?(dl\s?[a-zA-Z\d\(]*|100\s?ml)$', # µg/dl
    'µg/ml' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?[â]?(micro|mc|[æáµu]|um|mu)g[/7\s]?ml\s?[a-zA-Z\d\(]*$',            # µg/ml 
    'µg/l' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?[â]?(micro|mc|[æáµu]|um|mu)g[/7\s]?l\s?[a-zA-Z\d\(]*$',              # µg/l
    'mg/dl' : r'^([a-zA-Z\d]+([,-][a-zA-Z\d]+)*)?[\s]?\(?mq?gr?[/7\s]?(dl\s?[a-zA-Z\d]*|100\s?ml)$',                      # mg/dl
    'mg/ml' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?mgr?[/7\s]?ml\s?[a-zA-Z\d]*$',                                      # mg/ml
    'mg/l' : r'^mgr?[\.\,]?[/7\s]?l\s?[a-zA-Z\d]*$',                                                                      # mg/l
    'ng/l' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?(n|nano)gr?.*[/7\s]l\s?[a-zA-Z\d]*$',                                # ng/l
    'ng/dl' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?(n|nano)gr?.*[/7\s](dl\s?[a-zA-Z\d]*|100\s?ml)\s?[a-zA-Z\d]*$',     # ng/dl
    'ng/ml' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?(n|nano)gr?.*[/7\s]?ml\s?[a-zA-Z\dóò]*$',                           # ng/ml
    'pg/ml' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?(p|pico)gr?.*[/7\s]?ml\s?[a-zA-Z\d]*$',                             # pg/ml
    'mpl/ml' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?mpl.*[/7\s]?ml\s?[a-zA-Z\d]*$',                                    # mpl/ml
    'g/dl' : r'^([\d]+(,[\d]+)*)?[\s]?gr?[/7\s]?(dl|100\s?ml)$',                                                          # g/dl
    'g/ml' : r'^([\d]+(,[\d]+)*)?[\s]?gr?[/7\s]?ml$',                                                                     # g/ml
    'g/l' : r'^([\d]+(,[\d]+)*)?[\s]?gr?[/7\s]?l$',                                                                       # g/l
    'mmol/l' : r'^(?!.*/mm?ol?|.*dl)m{1,2}(os)?m(ol?)?[/7].*l.*',                                                         # mmol/l
    'pmol/l' : r'^pm(ol?)?\.?[/7].*l.*',                                                                                  # pmol/l
    'mmol/dl' : r'^(?!.*/mm?ol?)m(os)?m(ol?)?[/7].*dl.*',                                                                 # mmol/dl
    'ui/ml' : r'^([\d]+(,[\d]+)*)?(u(i|\.?int\.?)|iu)[/7]m\,?l.*$',                                                       # ui/ml (unitats internacionals / ml)
    'ua/ml' : r'^([\d]+(,[\d]+)*)?(u(a|\.?int\.?)|au)[/7]ml.*$',                                                          # ua/ml (unitats arbitraries / ml)
    'ui/l' : r'^([\d]+(,[\d]+)*)?\s?(ui?|\.?int\.?u|u\.?int\.?|iu)[/7]l.*$',                                              # ui/l (unitats internacionals / l)
    'mui/l' : r'^m(ui?|\.?int\.?u\.?|\.?u\.?int\.?|iu)[/7]l.*$',                                                          # mui/l (mili unitats internacionals / l)
    'ui/dl' : r'^([\d]+(,[\d]+)*)?\s?(ui?|\.?int\.?u\.?|u\.?int\.?|iu)[/7]dl.*$',                                         # ui/dl (unitats internacionals / dl)
    'kiu/l' : r'^k(int\.?u\.?|iu|u(?:\.?i\.?)?)?[7/]l{1,2}',                                                              # kiu/l (kilo international units / l)
    'µui/ml' : r'^\(?[áâæ]?(mc?|micro\s?|u|µ|[áâæ])(ui?|iu)[/7\s]?ml$',                                                   # µui/ml (micro-international units/ml)
    'eu/dl' : r'^([a-zA-Z\d]+(,[a-zA-Z\d]+)*)?[\s]?\(?e.?u.?[/7\s]?dl$',                                                  # eu/dl (enzyme units/dl)
    'µmol/l' : r'^[âá]?([âáuµ]|micro|mu)mol/l$',                                                                          # µmol/l
    'nmol/mmol' : r'^nmol/*mmol\s?.*',                                                                                    # nmol/mmol
    'mmol/mol' : r'^m?mmol/*mol\s?.*',                                                                                    # mmol/mol
    'mg/mmol' : r'^mg/mmol\s?(cre)?.*',                                                                                   # mg/mmol
    'mol/mol' : r'^mol/mol.*',                                                                                            # mol/mmol
    'g/mol' : r'^g/mol\s?(cre)?.*',                                                                                       # g/mol
    '10^3/µl' : r'^x?.*(10.*[3³]|mil|1000|^m|^k[/7]).*/*[áâ]*([µuá]l|mcl)$',                                              # 10^3/µl
    '10^3/mm3' : r'^x?.*(10.*[3³]|mil|1000|^m[/7]|^k[/7]).*/*mm[\s]?.*$',                                                 # 10^3/mm3
    '10^3/ml' : r'^x?.*(10.*[3³]|mil|1000|^m[/7]|^k[/7]).*/*(ml|microl)[\s]?.*$',                                         # 10^3/ml
    '10^3' : r'^x?.*(10[^xe]?[3³]|mil|1000)$',                                                                            # 10^3
    '10^6/µl' : r'^x?.*10.*6.*/*[áâ]*([µuá]l|mcl)$',                                                                      # 10^6/µl
    '10^6/ml' : r'^x?.*10.*6.*/*ml$',                                                                                     # 10^6/ml
    '10^6/l' : r'^x?.*10.*6.*/?l$',                                                                                       # 10^6/l
    '10^6/mm3' : r'^x?.*10.*6.*/*mm[\s]?.*$',                                                                             # 10^6/mm3
    '10^6' : r'^x?.*10.*6$',                                                                                              # 10^6
    '10^9/l' : r'^x?.*10?.*9.*/?l$',                                                                                      # 10^9/l
    '10^9' : r'^x?.*10.*9$',                                                                                              # 10^9
    '10^12/l' : r'^x?.*10.*12.*/?l$',                                                                                     # 10^12/l
    'index' : r'\bã?[iíïãI][mn]dex\b|indice',                                                                            # index
    'segons' : r'\b(s(?:eg(?:ond|ons?|undos?)?|g(?:u)?)|^s$)\b',                                                          # segons
    'ratio' : r'^\[?(r(a[oöóò]|[aàá]tio?)|(in)?r)$',                                                                      # ratio
    'ph' : r'^.*?ph.*$',                                                                                                  # ph
    'mmol/24h' : r'mmol/\s?(24\s?h(or[ae]s)?|d(ia)?).*',                                                                  # mmol/24h
    'µg/24h' : r'[â]?(u|mc|µ|mu)g/\s?(24\s?h(or[ae]s)?|d(ia)?).*',                                                        # µg/24h
    'mg/24h' : r'mgr?/\s?(24\s?h(or[ae]s)?.*|d(ia)?)',                                                                    # mg/24h
    'ui/24h' : r'(u\.?i|i\.?u)/\s?(24\s?h(or[ae]s)?.*|d(ia)?)',                                                           # ui/24h
    'g/24h' : r'gr?/\s?(24\s?h(or[ae]s)?.*|d(ia)?)',                                                                      # g/24h
    'g/12h' : r'gr?/\s?12\s?h(or[ae]s)?.*',                                                                               # g/12h
    'nmol/24h' : r'nmol/\s?(24\s?h(or[ae]s)?.*|d(ia)?)',                                                                  # nmol/24h
    'meq/24h' : r'([\d]+(,[\d]+)*)?mequ?[/7](24\s?h(or[ae]s)?.*|d(ia)?)',                                                 # meq/24h
    'ml/min/1.73m2' : r'\b(ml|mil?)(?:[i]*|il)?[7/\(]*m(?:i?n?)?[\)*]?/?1[.,\']7[23]m?(?:\^?2|[m²&2e2]*)?.*\b',           # ml/min/1.73m2
    'ml/min' : r'^ml[/7]m(i|in|n|inut)',                                                                                  # ml/min
    'ng/ml/h' : r'^ng[/7]ml[7/]h(ora)?$',                                                                                 # ng/ml/h
    'cel/mm3' : r'^1?(x\s?)?[/7]mm[\s]?(c|3|c[uú]bic|³)',                                                                 # cel/mm3
    'cel/µl' : r'^1?u?[/7]â?(mc|micro|u|µ)[\s]?l',                                                                        # cel/µl
    'cel/mm3' : r'^.*(hem:*|c[eièé]l).*[/7]mm.*',                                                                         # cel/mm3
    'cel/µl' : r'^.*(hem:*|c[eièé]l).*[/7]â?(mc|micro|u|µ)[\s]?l',                                                        # cel/µl
    'cel/µl' : r'^.*er[iy][/7][áâ]?(mc|micro|u|µ)[\s]?l',                                                                 # cel/µl
    'cel/µl' : r'^.*leu.*[/7][áâ]?(mc|micro|u|µ)[\s]?l',                                                                  # cel/µl
    'cel/camp' : r'^(per\s?camp|x?\s?camp|(cel)?\/\s?camp)$',                                                             # cel/camp
    'copies/ml' : r'^.*c..?pies.*[/7](ml)[\s]?.*',                                                                        # copies/ml
    'g' : r'^gr?$',                                                                                                       # g
    'µl' : r'^[â]?(micro|mc|[æáµu]|um|mu)l$',                                                                             # µl
    'mm3' : r'^mm[\s]?(c|3|c[uú]bic|³)$',                                                                                 # mm3
    'pg' : r'^pgr?$',                                                                                                     # pg
    'g/dl' : r'^gr?/100\s?ml$',                                                                                           # g/dl
    'µg/g' : r'^(?!.*µg/ghb)[áâ]?(mc|micro|u|µ)g.*[/7]gr?',                                                               # µg/g
    'g/g' : r'^g.*[/7]gr?.*',                                                                                             # g/g
    'mg/g' : r'^u?mg.*[/7]gr?.*',                                                                                         # mg/g
    'mg/mg' : r'^u?mg.*[/7]mg?.*',                                                                                        # mg/mg
    'mg/kg' : r'^u?mg.*[/7]kg.*',                                                                                         # mg/kg
    'µg/mg' : r'^(?!.*µg/ghb|umg/mg)â?(mc|micro|u|µ|mu)g.*[/7].*mgr?.*',                                                  # µg/mg
    'mmol/kg' : r'^m(os)?m(ol)?[/7].*kgr?.*',                                                                             # mmol/kg
    'gpl/ml' : r'^(u\s?)?gpl.*[/7]ml',                                                                                    # gpl/ml
    'µkat/l' : r'^[uµ]kat[/7]l',                                                                                          # µkat/l
    'mu/10^9 eritrocits' : r'^mu[/7]\s?(10?.*9.*|mil.*|1000\s?mil.*)',                                                    # mu/10^9 eritrocits
    'meq/l' : r'^([\d]+(,[\d]+)*)?mequ?[/7]\s?l',                                                                         # meq/l
    'mmhg' : r'^mm\s?hg',                                                                                                 # mmHg
    'fl' : r'^fl(\.)?',                                                                                                  # fl 
}
