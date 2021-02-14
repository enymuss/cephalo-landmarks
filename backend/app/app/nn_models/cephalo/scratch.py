import pandas as pd
import cephaloConstants
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import patches
import os
import random

landmark_positions = {
    0: [406.1053 , 259.7082 ],
    1: [385.68787, 273.8496 ],
    2: [380.97614, 307.29517],
    3: [375.81567, 366.55444],
    4: [350.91086, 158.92255],
    5: [365.49478, 268.01346],
    6: [353.82767, 279.01233],
    7: [345.52606, 350.39282],
    8: [356.74442, 387.20538],
    9: [350.2378 , 394.83728],
    10: [335.33304, 270.37036],
    11: [361.42194, 326.55368],
    12: [346.92737, 314.68927],
    13: [333.48203, 363.7037 ],
    14: [183.37036, 189.1253 ],
    15: [165.4823 , 255.     ],
    16: [132.71904, 278.05554],
    17: [236.56195, 278.8889 ],
    18: [186.58408, 349.44446],
    19: [209.90709, 354.72223]
}



def plot_landmarks_on_ax(landmark_xy, ax):
    plot_ABC_angle_info(landmark_xy[0], landmark_xy[1], landmark_xy[2], ax, 'ro-')

def plot_ABC_angle_info(pointA, pointB, pointC, ax, lineStyle='yo-'):
    angle = 0
    theta2 = 360

    r = min(40, max(np.linalg.norm(pointB-pointA), np.linalg.norm(pointB-pointC)))

    angle_deg = cephaloConstants.angle_between_three_points(pointA, pointB, pointC)
    print("Cephalo Angle:", angle_deg)

    plot_points = np.array([pointA, pointB, pointC])
    ax.plot(plot_points[:, 0], plot_points[:, 1], lineStyle)

    cclw_arc_a = cephaloConstants.cclockwise_angle_between_points((pointB + np.array([r, 0])), pointB, pointA)
    cclw_arc_c = cephaloConstants.cclockwise_angle_between_points((pointB + np.array([r, 0])), pointB, pointC)

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
    cephalo_angle  = cephaloConstants.angle_between_four_points(landmark_xy[0], landmark_xy[1], landmark_xy[2], landmark_xy[3])

    intersect_x, intersect_y = cephaloConstants.point_of_line_intersection(pointA, pointB, pointC, pointD)
    intersection = [intersect_x, intersect_y]

    segment1_point_closest_to_intersection, _ = cephaloConstants.sort_points_from_intersection(landmark_xy[0], landmark_xy[1], intersection)
    segment2_point_closest_to_intersection, _ = cephaloConstants.sort_points_from_intersection(landmark_xy[2], landmark_xy[3], intersection)


    cephalo_intersect_angle  = cephaloConstants.angle_between_three_points(segment1_point_closest_to_intersection,intersection,segment2_point_closest_to_intersection)

    # print("Cephalo Angle:", cephalo_angle)

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
    print("-".join(pointAngle))
    if (len(landmark_xy) == 4):
        plot_four_landmarks_on_ax(landmark_xy, ax)
    else:
        plot_landmarks_on_ax(landmark_xy, ax)
        # continue

possible_distances = []

for measurement_points in cephaloConstants.distance_list:
    if cephaloConstants.can_calculate_measurement(measurement_points):
        possible_distances.append(measurement_points)

print(possible_distances)

px_per_cm = 27

for line in possible_distances:
    landmark_xy = []
    for x in line:
        for id in cephaloConstants.acronym_to_landmark_ids(x):
            landmark_xy.append(landmark_positions[id])

    landmark_xy = np.array(landmark_xy)
    print(landmark_xy)
    if (len(landmark_xy) == 3):
        # plot_landmarks_on_ax(landmark_xy, ax)
        continue
        ax.scatter(landmark_xy[0][0], landmark_xy[0][1])
        ax.plot(landmark_xy[1:, 0], landmark_xy[1:, 1], 'bo-')
        p1=landmark_xy[1]
        p2=landmark_xy[2]
        p3=landmark_xy[0]
        distance = cephaloConstants.calculate_distance(px_per_cm, p1, p2, p3)

        print(f"Distance: {distance} cm")

        dx, dy = p2-p1
        det = dx*dx + dy*dy
        a = (dy*(p3[1]-p1[1])+dx*(p3[0]-p1[0]))/det
        p4 = [p1[0]+a*dx, p1[1]+a*dy]

        plot_ABC_angle_info(p2, p4, p3, ax, 'go--')

        # plot_four_landmarks_on_ax(landmark_xy, ax)
    elif (len(landmark_xy) == 4):
        p1 = landmark_xy[0]
        p2 = landmark_xy[1]
        p3 = landmark_xy[2]
        p4 = landmark_xy[3]

        distance = cephaloConstants.calculate_distance(px_per_cm, p1, p2, p3, p4)

        print(f"Distance: {distance} cm")
        # import pdb; pdb.set_trace()
        ax.plot(landmark_xy[:2, 0], landmark_xy[:2, 1], 'o-')
        ax.plot(landmark_xy[2:, 0], landmark_xy[2:, 1], 'o-')
    #     continue

# plt.show()
