# IMG_SIZE_ORIGINAL = {'width': 2260, 'height': 2304}
# IMG_SIZE_ROUNDED_TO_64 = {'width': 2304, 'height': 2304}
# IMAGE_PATH='data/2304'
import os
import numpy as np

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
    {'cephalo': 2, 'textbook': "UL"},
    {'cephalo': 3, 'textbook': "WPg"},
    {'cephalo': 4, 'textbook': "N"},
    {'cephalo': 5, 'textbook': "Sp"},
    {'cephalo': 6, 'textbook': ""},
    {'cephalo': 7, 'textbook': "B"},
    {'cephalo': 8, 'textbook': "Pg"},
    {'cephalo': 9, 'textbook': "Gn"},
    {'cephalo': 10, 'textbook': "Isa"},
    {'cephalo': 11, 'textbook': "Iss"},
    {'cephalo': 12, 'textbook': "Iis"},
    {'cephalo': 13, 'textbook': "Iia"},
    {'cephalo': 14, 'textbook': "S"},
    {'cephalo': 15, 'textbook': "Ar"},
    {'cephalo': 16, 'textbook': "Ba"},
    {'cephalo': 17, 'textbook': ""},
    {'cephalo': 18, 'textbook': "tgo"},
    {'cephalo': 19, 'textbook': ""},
]

angles_list = [["S", "N", "A"], ["S", "N", "B"],
                ["A", "N", "B"], ["S", "N", "Pg"],
                ["ML", "NSL"], ["NL", "NSL"],
                ["ML", "NL"], ["Gn", "tgo", "Ar"],
                ["N", "S", "Ba"],
                ["U1", "NA"],
                ["L1", "NB"],
                ["U1", "L1"]]
angle_keys  = {
    "ML": ["tgo", "Gn"],
    "NSL" : ["N", "S"],
    "NL": ["Sp", "Pg"],
    "U1": ["Isa", "Iss"],
    "L1": ["Iis", "Iia"],
    "NB" : ["N", "B"],
    "NA" : ["N", "A"]
}
distance_list = [["U1", "NA"], ["L1", "NB"], ["Pg", "NB"]]

def cephalo_landamrk_from_textbook_acronym(acronym):
    for landmark in CEPHALO_TO_TEXTBOOK_MAPPING:
        if landmark["textbook"] == acronym:
            return landmark["cephalo"]
    return None

def acronym_from_landmark_id(landmark_id):
    for landmark in CEPHALO_TO_TEXTBOOK_MAPPING:
        if landmark["cephalo"] == landmark_id:
            return landmark["textbook"]
    return landmark_id

def acronym_to_landmark_ids(acronym):
    landmark_ids = []

    if acronym in angle_keys:
        for aacronym in angle_keys[acronym]:
            landmark_ids.append(cephalo_landamrk_from_textbook_acronym(aacronym))
    else:
        landmark_ids.append(cephalo_landamrk_from_textbook_acronym(acronym))

    return landmark_ids


def can_calculate_measurement(measurement_item):
    for acronym in measurement_item:
        if acronym in angle_keys:
            for aacronym in angle_keys[acronym]:
                if cephalo_landamrk_from_textbook_acronym(aacronym) is None:
                    return False
        elif (cephalo_landamrk_from_textbook_acronym(acronym) is None):
            return False
    return True

def calculate_distance(px_per_cm, pointA, pointB, pointC, pointD=None):
    distance = 0


    if pointD is None:
        p1 = np.array(pointA)
        p2 = (pointB)
        p3 = (pointC)
        distance=np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)

    else:
        p1 = np.array(pointA)
        p2 = np.array(pointB)
        p3 = np.array(pointC)
        p4 = np.array(pointD)

        distance=np.cross(p2-p1,p4-p3)/np.linalg.norm(p2-p1)

    distance = abs(distance) * 1/px_per_cm
    return distance

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

def angle_between_three_points(pointA, pointB, pointC):
    a = np.array(pointA)
    b = np.array(pointB)
    c = np.array(pointC)
    ba = a - b
    bc = c - b
    return angle_between_vectors(ba, bc)

def angle_between_vectors(vectorA, vectorB):
    cosine_angle = np.dot(vectorA, vectorB) / (np.linalg.norm(vectorA) * np.linalg.norm(vectorB))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def point_of_line_intersection(pointA, pointB, pointC, pointD):
    slope1 = (pointB[1] - pointA[1]) / (pointB[0] - pointA[0])
    intercept1 = pointA[1] - (slope1*pointA[0])
    slope2 = (pointD[1] - pointC[1]) / (pointD[0] - pointC[0])
    intercept2 = pointC[1] - (slope2*pointC[0])

    x = (intercept2 - intercept1) / (slope1 - slope2)
    y = (slope1*x) + intercept1

    return [x, y]

def sort_points_from_intersection(pointA, pointB, intersection):
    if (np.linalg.norm(intersection-pointA) < np.linalg.norm(intersection-pointB)):
        point_closest_to_intersection = pointA
        point_furthest_from_intersection = pointB
    else:
        point_closest_to_intersection = pointB
        point_furthest_from_intersection = pointA

    return point_closest_to_intersection, point_furthest_from_intersection

def angle_between_four_points(pointA, pointB, pointC, pointD):
    pointA = np.array(pointA)
    pointB = np.array(pointB)
    pointC = np.array(pointC)
    pointD = np.array(pointD)

    intersect_x, intersect_y = point_of_line_intersection(pointA, pointB, pointC, pointD)
    intersection = [intersect_x, intersect_y]

    segment1_point_closest_to_intersection, segment1_point_furthest_from_intersection = sort_points_from_intersection(pointA, pointB, intersection)
    segment2_point_closest_to_intersection, segment2_point_furthest_from_intersection = sort_points_from_intersection(pointC, pointD, intersection)

    a, b = segment1_point_closest_to_intersection, segment1_point_furthest_from_intersection
    c, d = segment2_point_closest_to_intersection, segment2_point_furthest_from_intersection
    ba = a - b
    dc = c - d
    return angle_between_vectors(ba, dc)

def cclockwise_angle_between_points(pointA, pointB, pointC):
    a = np.array(pointA)
    b = np.array(pointB)
    c = np.array(pointC)
    ba = a - b
    bc = c - b

    inner_angle = angle_between_vectors(ba, bc)
    det = np.linalg.det([ba, bc])

    if det>0:
        return inner_angle
    else:
        return 360-inner_angle
