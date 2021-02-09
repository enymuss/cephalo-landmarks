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

    inner_angle = angle_between_vectors(ba, bc)
    det = np.linalg.det([ba, bc])

    if det>0:
        return inner_angle
    else:
        return 360-inner_angle

def xy_for_landmark(landmarks_list):
    point_list = []
    for point in landmarks_list:
        cephalo_landmark_id = cephaloConstants.cephalo_landamrk_from_textbook_acronym(point)
        if cephalo_landmark_id is None:
            raise ValueError(f"Did not find matching Cephalo Id for acronym {point}")
        point_x = one_file_series[cephalo_landmark_id*2]
        point_y = one_file_series[(cephalo_landmark_id*2)+1]
        point_list.append([point_x, point_y])
    return point_list


def plot_landmarks_on_ax(landmark_xy, ax):
    r = 40
    angle = 0
    theta2 = 360

    cephalo_angle  = cephaloConstants.angle_between_three_points(landmark_xy[0],landmark_xy[1],landmark_xy[2])

    cclw_arc_a = cclockwise_angle_between_points((landmark_xy[1] + [r, 0]), landmark_xy[1], landmark_xy[0])
    cclw_arc_c = cclockwise_angle_between_points((landmark_xy[1] + [r, 0]), landmark_xy[1], landmark_xy[2])

    ax.plot(landmark_xy[:, 0], landmark_xy[:, 1], 'ro-')

    if (abs(cclw_arc_a-cclw_arc_c) > 180):
        # arc default starting point is inside angle
        angle = max(cclw_arc_a, cclw_arc_c)
        theta2 = min(cclw_arc_a, cclw_arc_c)
    else:
        # arc default starting point is outisde angle
        angle = min(cclw_arc_a, cclw_arc_c)
        theta2 = max(cclw_arc_a, cclw_arc_c)

    e1 = patches.Arc(tuple(landmark_xy[1]), width=2*r, height=2*r, linewidth=2, fill=False, zorder=2, angle=angle, theta2=cephalo_angle)
    ax.add_patch(e1)

    mid_angel = np.deg2rad((angle+theta2)/2)
    ax.annotate(f"{cephalo_angle:.1f}°", (r*np.cos(mid_angel)+landmark_xy[1][0], r*np.sin(mid_angel)+landmark_xy[1][1]))


def plot_four_landmarks_on_ax(landmark_xy, ax):
    r = 40
    angle = 0
    theta2 = 360

    cephalo_angle  = cephaloConstants.angle_between_four_points(landmark_xy[0],landmark_xy[1],landmark_xy[2], landmark_xy[3])

    print(cephalo_angle)

    # cclw_arc_a = cclockwise_angle_between_points((landmark_xy[1] + [r, 0]), landmark_xy[1], landmark_xy[0])
    # cclw_arc_c = cclockwise_angle_between_points((landmark_xy[1] + [r, 0]), landmark_xy[1], landmark_xy[2])

    ax.plot(landmark_xy[:2, 0], landmark_xy[:2, 1], 'ro-')
    ax.plot(landmark_xy[2:, 0], landmark_xy[2:, 1], 'bo-')

    slope1 = (landmark_xy[1][1] - landmark_xy[0][1]) / (landmark_xy[1][0] - landmark_xy[0][0])
    intercept1 = landmark_xy[0][1] - (slope1*landmark_xy[0][0])
    slope2 = (landmark_xy[3][1] - landmark_xy[2][1]) / (landmark_xy[3][0] - landmark_xy[2][0])
    intercept2 = landmark_xy[2][1] - (slope2*landmark_xy[2][0])

    intersect_x = (intercept2 - intercept1) / (slope1 - slope2)
    intersect_y = (slope1*intersect_x) + intercept1

    # import pdb; pdb.set_trace()

    intersection = [intersect_x, intersect_y]

    ax.scatter(intersect_x, intersect_y)


    if (np.linalg.norm(intersection-landmark_xy[0]) < np.linalg.norm(intersection-landmark_xy[1])):
        ax.plot([intersect_x, landmark_xy[0][0]], [intersect_y, landmark_xy[0][1]], 'go--')
    else:
        ax.plot([intersect_x, landmark_xy[1][0]], [intersect_y, landmark_xy[1][1]], 'go--')

    if (np.linalg.norm(intersection-landmark_xy[2]) < np.linalg.norm(intersection-landmark_xy[3])):
        ax.plot([intersect_x, landmark_xy[2][0]], [intersect_y, landmark_xy[2][1]], 'go--')
    else:
        ax.plot([intersect_x, landmark_xy[3][0]], [intersect_y, landmark_xy[3][1]], 'go--')


    # if (abs(cclw_arc_a-cclw_arc_c) > 180):
    #     # arc default starting point is inside angle
    #     angle = max(cclw_arc_a, cclw_arc_c)
    #     theta2 = min(cclw_arc_a, cclw_arc_c)
    # else:
    #     # arc default starting point is outisde angle
    #     angle = min(cclw_arc_a, cclw_arc_c)
    #     theta2 = max(cclw_arc_a, cclw_arc_c)

    # e1 = patches.Arc(tuple(landmark_xy[1]), width=2*r, height=2*r, linewidth=2, fill=False, zorder=2, angle=angle, theta2=cephalo_angle)
    # ax.add_patch(e1)

    # mid_angel = np.deg2rad((angle+theta2)/2)
    # ax.annotate(f"{cephalo_angle:.1f}°", (r*np.cos(mid_angel)+landmark_xy[1][0], r*np.sin(mid_angel)+landmark_xy[1][1]))

# landmarks_pd = pd.read_csv('./inputs/cephalo_landmarks.csv')
# one_file_series = landmarks_pd.loc[0, :]
#
possible_angles = []

for measurement_points in cephaloConstants.angles_list:
    if cephaloConstants.can_calculate_measurement(measurement_points) and len(measurement_points)==2:
        possible_angles.append(measurement_points)
#
# for angle in cephaloConstants.angles_list:
#     try:
#         xy_for_landmark(angle)
#     except ValueError as err:
#         print(err)
#         print(f"Cannot calculate angle {angle}")
#         print()
#         continue
#     possible_angles.append(angle)
#
print(possible_angles)
#
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.imshow(Image.open(os.path.join("inputs", "images", "1000_1.jpg")))

for pointAngle in possible_angles:
    print(pointAngle)
    landmark_xy = []
    for x in pointAngle:
        # print(x, cephaloConstants.acronym_to_landmark_ids(x))
        for id in cephaloConstants.acronym_to_landmark_ids(x):
            landmark_xy.append(landmark_positions[id])
    print(landmark_xy)
    # landmark_xy = np.array(xy_for_landmark(pointAngle))

    # plot_landmarks_on_ax(np.array(landmark_xy), ax)
    if (len(landmark_xy) == 4):
        plot_four_landmarks_on_ax(np.array(landmark_xy), ax)
plt.show()
