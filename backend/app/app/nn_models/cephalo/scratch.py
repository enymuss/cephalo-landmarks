import pandas as pd
import cephaloConstants
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import patches
import os
import random

def angle_between_points(pointA, pointB, pointC):
    a = np.array(pointA)
    b = np.array(pointB)
    c = np.array(pointC)
    ba = a - b
    bc = c - b
    return angle_between_vectors(ba, bc)

def clockwise_angle_between_points(pointA, pointB, pointC):
    a = np.array(pointA)
    b = np.array(pointB)
    c = np.array(pointC)
    ba = a - b
    bc = c - b

    inner_angle = angle_between_vectors(ba, bc)
    det = np.linalg.det([ba, bc])

    if det<0:
        return inner_angle
    else:
        return 360-inner_angle

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

def angle_between_vectors(vectorA, vectorB):
    cosine_angle = np.dot(vectorA, vectorB) / (np.linalg.norm(vectorA) * np.linalg.norm(vectorB))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

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

    cephalo_angle  = angle_between_points(landmark_xy[0],landmark_xy[1],landmark_xy[2])
    angle_arc_A = angle_between_points((landmark_xy[1] + [r, 0]), landmark_xy[1], landmark_xy[0])
    angle_arc_C = angle_between_points((landmark_xy[1] + [r, 0]), landmark_xy[1], landmark_xy[2])

    cclw_arc_a = cclockwise_angle_between_points((landmark_xy[1] + [r, 0]), landmark_xy[1], landmark_xy[0])
    cclw_arc_c = cclockwise_angle_between_points((landmark_xy[1] + [r, 0]), landmark_xy[1], landmark_xy[2])

    ax.plot(landmark_xy[:, 0], landmark_xy[:, 1], 'ro-')

    if (angle_arc_A < cephalo_angle and angle_arc_C < cephalo_angle):
        angle = max(cclw_arc_a, cclw_arc_c)
        theta2 = min(cclw_arc_a, cclw_arc_c)
    else:
        angle = min(cclw_arc_a, cclw_arc_c)
        theta2 = max(cclw_arc_a, cclw_arc_c)

    e1 = patches.Arc(tuple(landmark_xy[1]), width=2*r, height=2*r, linewidth=2, fill=False, zorder=2, angle=angle, theta2=cephalo_angle)
    ax.add_patch(e1)

    mid_angel = np.deg2rad((angle+theta2)/2)
    ax.annotate(f"{cephalo_angle:.1f}°", (r*np.cos(mid_angel)+landmark_xy[1][0], r*np.sin(mid_angel)+landmark_xy[1][1]))


landmarks_pd = pd.read_csv('./inputs/cephalo_landmarks.csv')
one_file_series = landmarks_pd.loc[0, :]

possible_angles = []

for angle in cephaloConstants.angles_list:
    try:
        xy_for_landmark(angle)
    except ValueError as err:
        print(err)
        print(f"Cannot calculate angle {angle}")
        print()
        continue
    possible_angles.append(angle)

print(possible_angles)
# pointAngle = possible_angles[0]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.imshow(Image.open(os.path.join("inputs", "images", one_file_series[-1])))

for pointAngle in possible_angles:
    landmark_xy = np.array(xy_for_landmark(pointAngle))

    plot_landmarks_on_ax(landmark_xy, ax)

plt.show()
