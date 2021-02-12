import pandas as pd
import cephaloConstants
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import patches
import os
import random

landmark_positions = {
    0:  [405.49937438964844, 272.74523162841797],
    1:  [387.60816955566406, 285.80562591552734],
    2:  [398.4422607421875, 321.87039947509766],
    3:  [374.4025192260742, 397.9781494140625],
    4:  [351.0680923461914, 170.67684173583984],
    5:  [365.7011260986328, 282.8748970031738],
    6:  [350.8236846923828, 299.27740478515625],
    7:  [338.3203353881836, 373.30709075927734],
    8:  [345.8814697265625, 400.583740234375],
    9:  [341.8031768798828, 413.2873840332031],
    10: [326.60467529296875, 291.38012313842773],
    11: [372.9366149902344, 340.0787124633789],
    12: [346.2404479980469, 327.7736053466797],
    13: [328.77274322509766, 380.07271575927734],
    14: [178.55220794677734, 202.44730377197266],
    15: [143.0613250732422, 275.24500465393066],
    16: [121.09426879882812, 298.36219024658203],
    17: [237.27423477172852, 292.23270416259766],
    18: [182.96990966796875, 372.99903106689453],
    19: [209.0761489868164, 377.26587677001953]
}

def cclockwise_angle_between_points(pointA, pointB, pointC):
    a = np.array(pointA)
    b = np.array(pointB)
    c = np.array(pointC)
    ba = a - b
    bc = c - b

    inner_angle = cephaloConstants.angle_between_vectors(ba, bc)
    det = np.linalg.det([ba, bc])

    if det>0:
        return inner_angle
    else:
        return 360-inner_angle

def point_of_line_intersection(pointA, pointB, pointC, pointD):
    slope1 = (pointB[1] - pointA[1]) / (pointB[0] - pointA[0])
    intercept1 = pointA[1] - (slope1*pointA[0])
    slope2 = (pointD[1] - pointC[1]) / (pointD[0] - pointC[0])
    intercept2 = pointC[1] - (slope2*pointC[0])

    x = (intercept2 - intercept1) / (slope1 - slope2)
    y = (slope1*x) + intercept1

    return [x, y]

def plot_landmarks_on_ax(landmark_xy, ax):
    plot_ABC_angle_info(landmark_xy[0], landmark_xy[1], landmark_xy[2], ax, 'ro-')

def plot_ABC_angle_info(pointA, pointB, pointC, ax, lineStyle='yo-'):
    angle = 0
    theta2 = 360

    r = min(40, max(np.linalg.norm(pointB-pointA), np.linalg.norm(pointB-pointC)))

    angle_deg = cephaloConstants.angle_between_three_points(pointA, pointB, pointC)

    plot_points = np.array([pointA, pointB, pointC])
    ax.plot(plot_points[:, 0], plot_points[:, 1], lineStyle)

    cclw_arc_a = cclockwise_angle_between_points((pointB + np.array([r, 0])), pointB, pointA)
    cclw_arc_c = cclockwise_angle_between_points((pointB + np.array([r, 0])), pointB, pointC)

    if (abs(cclw_arc_a-cclw_arc_c) > 180):
        # arc default starting point is inside angle
        angle = max(cclw_arc_a, cclw_arc_c)
        theta2 = min(cclw_arc_a, cclw_arc_c)
        mid_angel = np.deg2rad(((angle+theta2)%360)/2)
    else:
        # arc default starting point is outisde angle
        angle = min(cclw_arc_a, cclw_arc_c)
        theta2 = max(cclw_arc_a, cclw_arc_c)
        mid_angel = np.deg2rad(((angle+theta2))/2)

    e1 = patches.Arc(tuple(pointB), width=2*r, height=2*r, linewidth=2, fill=False, zorder=2, angle=angle, theta2=angle_deg)
    ax.add_patch(e1)


    # import pdb; pdb.set_trace()
    ax.annotate(f"{angle_deg:.1f}°", (r*np.cos(mid_angel)+pointB[0], r*np.sin(mid_angel)+pointB[1]))
    # ax.annotate(f"PointA", tuple(pointA))
    # ax.annotate(f"PointB", tuple(pointB))
    # ax.annotate(f"PointC", tuple(pointC))

def plot_four_landmarks_on_ax(landmark_xy, ax):
    intersect_x, intersect_y = point_of_line_intersection(landmark_xy[0], landmark_xy[1], landmark_xy[2], landmark_xy[3])
    intersection = [intersect_x, intersect_y]

    if (np.linalg.norm(intersection-landmark_xy[0]) < np.linalg.norm(intersection-landmark_xy[1])):
        segment1_point_closest_to_intersection = landmark_xy[0]
        segment1_point_furthest_from_intersection = landmark_xy[1]
    else:
        segment1_point_closest_to_intersection = landmark_xy[1]
        segment1_point_furthest_from_intersection = landmark_xy[0]

    if (np.linalg.norm(intersection-landmark_xy[2]) < np.linalg.norm(intersection-landmark_xy[3])):
        segment2_point_closest_to_intersection = landmark_xy[2]
        segment2_point_furthest_from_intersection = landmark_xy[3]
    else:
        segment2_point_closest_to_intersection = landmark_xy[3]
        segment2_point_furthest_from_intersection = landmark_xy[2]


    cephalo_angle  = cephaloConstants.angle_between_four_points(segment1_point_closest_to_intersection, segment1_point_furthest_from_intersection,
                                                                segment2_point_closest_to_intersection, segment2_point_furthest_from_intersection)

    cephalo_intersect_angle  = cephaloConstants.angle_between_three_points(segment1_point_closest_to_intersection,intersection,segment2_point_closest_to_intersection)

    print(cephalo_angle)

    if round(cephalo_angle, 3) != round(cephalo_intersect_angle, 3):
        #draw arc for the obtuse angle
        print(f"4point angle and intersect angle do not match")
        print(f"cephalo_angle {cephalo_angle}, cephalo_intersect_angle {cephalo_intersect_angle}")
        temp = segment1_point_closest_to_intersection
        segment1_point_closest_to_intersection = segment1_point_furthest_from_intersection
        segment1_point_furthest_from_intersection = temp

    ax.plot(landmark_xy[:2, 0], landmark_xy[:2, 1], 'ro-')
    ax.plot(landmark_xy[2:, 0], landmark_xy[2:, 1], 'bo-')
    plot_ABC_angle_info(segment1_point_closest_to_intersection, intersection, segment2_point_closest_to_intersection, ax, 'go--')


possible_angles = []

for measurement_points in cephaloConstants.angles_list:
    if cephaloConstants.can_calculate_measurement(measurement_points):
        possible_angles.append(measurement_points)

print(possible_angles)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.imshow(Image.open(os.path.join("inputs", "images", "1000_1.jpg")))

for pointAngle in possible_angles:
    landmark_xy = []
    for x in pointAngle:
        for id in cephaloConstants.acronym_to_landmark_ids(x):
            landmark_xy.append(landmark_positions[id])

    landmark_xy = np.array(landmark_xy)
    if (len(landmark_xy) == 4):
        plot_four_landmarks_on_ax(landmark_xy, ax)
    else:
        # plot_landmarks_on_ax(landmark_xy, ax)
        continue

plt.show()
