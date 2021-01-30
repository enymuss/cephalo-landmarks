import pandas as pd
import cephaloConstants
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

def angle_between_points(pointA, pointB, pointC):
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

def xy_for_landmark(landmarks_list):
    point_list = []
    for point in landmarks_list:
        cephalo_landmark_id = cephaloConstants.cephalo_landamrk_from_textbook_acronym(point)
        point_x = one_file_series[cephalo_landmark_id*2]
        point_y = one_file_series[(cephalo_landmark_id*2)+1]
        point_list.append([point_x, point_y])
    return point_list

landmarks_pd = pd.read_csv('./inputs/cephalo_landmarks.csv')
one_file_series = landmarks_pd.loc[0, :]
pointAngle = ["S" , "N", "B"]
landamrk_xy = xy_for_landmark(pointAngle)

print(angle_between_points(landamrk_xy[0],landamrk_xy[1],landamrk_xy[2]))
landamrk_xy = np.array(landamrk_xy)
plt.imshow(Image.open(os.path.join("inputs", "images", one_file_series[-1])), cmap='gray')
plt.plot(landamrk_xy[:, 0], landamrk_xy[:, 1], 'ro-')
plt.show()
