# IMG_SIZE_ORIGINAL = {'width': 2260, 'height': 2304}
# IMG_SIZE_ROUNDED_TO_64 = {'width': 2304, 'height': 2304}
# IMAGE_PATH='data/2304'
import os

IMG_SIZE_ORIGINAL = {'width': 502, 'height': 512}
IMG_SIZE_ROUNDED_TO_64 = {'width': 512, 'height': 512}
IMAGE_PATH=os.path.join(os.getcwd(), "app", "nn_models", "cephalo", 'inputs')

IMG_TRANSFORM_PADDING = {'width': IMG_SIZE_ROUNDED_TO_64['width'] - IMG_SIZE_ORIGINAL['width'],
                        'height': IMG_SIZE_ROUNDED_TO_64['height']- IMG_SIZE_ORIGINAL['height']}

ISBI_TO_CEPHALO_MAPPING = {
"Columella"                : {'isbi': None, 'cephalo': 0},
"Subnasale"                : {'isbi': 14, 'cephalo': 1},
"Upper lip"                : {'isbi': 12, 'cephalo': 2},
"Soft Tissue Pogonion"     : {'isbi': 15, 'cephalo': 3},
"Nasion"                   : {'isbi': 1, 'cephalo': 4},
"Anterior nasal spine"     : {'isbi': 17, 'cephalo': 5},
"Subspinale"               : {'isbi': 4, 'cephalo': 6},
"Point B"                  : {'isbi': None, 'cephalo': 7},
"Pogonion"                 : {'isbi': 6, 'cephalo': 8},
"Gnathion"                 : {'isbi': 8, 'cephalo': 9},
"U1 root tip"              : {'isbi': None, 'cephalo': 10},
"U1 incisal edge"          : {'isbi': None, 'cephalo': 11},
"L1 incisal edge"          : {'isbi': None, 'cephalo': 12},
"L1 root tip"              : {'isbi': None, 'cephalo': 13},
"Sella"                    : {'isbi': 0, 'cephalo': 14},
"Articulare"               : {'isbi': 18, 'cephalo': 15},
"Basion"                   : {'isbi': None, 'cephalo': 16},
"Posterior nasal spine"    : {'isbi': 16, 'cephalo': 17},
"Gonion constructed"       : {'isbi': None, 'cephalo': 18},
"Tuberositas messenterica" : {'isbi': None, 'cephalo': 19},
"Orbitale"                 : {'isbi': 2, 'cephalo': None},
"Porion"                   : {'isbi': 3, 'cephalo': None},
"Supramentale"             : {'isbi': 5, 'cephalo': None},
"Menton"                   : {'isbi': 7, 'cephalo': None},
"Gonion"                   : {'isbi': 9, 'cephalo': None},
"Incision inferis"         : {'isbi': 10, 'cephalo': None},
"Incision superius"        : {'isbi': 11, 'cephalo': None},
"Lower lip"                : {'isbi': 13, 'cephalo': None}
}
TEXTBOOK_LANDMARKS = {
"S":    "Sella",
"Ba":   "Basion",
"N":    "Nasion",
"Sp":   "Spina nasalis anterior",
"A":    "Puntk A",
"Pm":   "Pterygomaxillare",
"Iss":  "Incision superius",
"Isa":  "Apex zęba siecznego szczęki",
"B":    "Punkt B",
"Pg":   "Pogonion",
"Gn":   "Gnathion",
"Iis":  "Incision inferius",
"Iia":  "Apex zęba siecznego żuchwy",
"Ar":   "Articulare",
"tgo":  "Gonion",
"Sp'":  "Spina'",
"WPg":  "Skórny punkt pogonion",
"UL":   "Punkt wargi górnej",
"Sn":   "Subnasale",
"ctg":  "Columella",
}

CEPHALO_TO_TEXTBOOK_MAPPING = [
    {'cephalo': 0, 'textbook': "ctg"},
    {'cephalo': 1, 'textbook': "Sn"},
    {'cephalo': 2, 'textbook': ""},
    {'cephalo': 3, 'textbook': "Pg"},
    {'cephalo': 4, 'textbook': "N"},
    {'cephalo': 5, 'textbook': ""},
    {'cephalo': 6, 'textbook': ""},
    {'cephalo': 7, 'textbook': "B"},
    {'cephalo': 8, 'textbook': ""},
    {'cephalo': 9, 'textbook': "Gn"},
    {'cephalo': 10, 'textbook': ""},
    {'cephalo': 11, 'textbook': ""},
    {'cephalo': 12, 'textbook': ""},
    {'cephalo': 13, 'textbook': ""},
    {'cephalo': 14, 'textbook': "S"},
    {'cephalo': 15, 'textbook': "Ar"},
    {'cephalo': 16, 'textbook': "Ba"},
    {'cephalo': 17, 'textbook': ""},
    {'cephalo': 18, 'textbook': ""},
    {'cephalo': 19, 'textbook': ""},
]

angles_list = [["S", "N", "A"], ["S", "N", "B"],
                ["A", "N", "B"], ["S", "N", "Pg"],
                ["ML", "NSL"], ["NL", "NSL"],
                ["ML", "NL"], ["Gn", "tgo", "Ar"],
                ["N", "S", "Ba"]]
distance_list = [["U1", "NA"], ["L1", "NB"]]

def cephalo_landamrk_from_textbook_acronym(acronym):
    for landmark in CEPHALO_TO_TEXTBOOK_MAPPING:
        if landmark["textbook"] == acronym :
            return landmark["cephalo"]
    return None

def filter_and_sort_isbi_to_cephalo_mapping():
    mapping_list = [(k, v["isbi"], v["cephalo"]) for k, v in ISBI_TO_CEPHALO_MAPPING.items()]
    valid_mapping_list = []

    # filter tuples with None values
    for points_tuple in mapping_list:
        if not any(map(lambda x: x is None, points_tuple)):
            valid_mapping_list.append(points_tuple)

    return sorted(valid_mapping_list, key=lambda x: x[1])

def cephalo_landmarks():
    mapping_list = [(k, v["cephalo"]) for k, v in ISBI_TO_CEPHALO_MAPPING.items()]
    valid_mapping_list = []

    # filter tuples with None values
    for points_tuple in mapping_list:
        if not any(map(lambda x: x is None, points_tuple)):
            valid_mapping_list.append(points_tuple)

    return sorted(valid_mapping_list, key=lambda x: x[1])
