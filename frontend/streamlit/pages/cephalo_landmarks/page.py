import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
import requests
from requests.auth import HTTPBasicAuth
import time
import tempfile
from . import cephaloConstants

CEPHALO_EXAMPLES = {
    "1000_1.jpg":"134",
    "1001_1.jpg":"135",
    "1002_1.jpg":"136",
    "1003_1.jpg":"137",
    "1004_1.jpg":"138",
    "1005_1.jpg":"139",
    "1006_1.jpg":"140",
    "1007_1.jpg":"141",
    "1008_1.jpg":"142",
    "1009_1.jpg":"143",
}

def get_measurements(cephalo_id):
    print(f"Getting measuemrents for {cephalo_id}")
    cephalo_response = requests.get("http://backend/api/v1/cephalo/measurements", params={'cephalo_id': str(cephalo_id)},)
    return cephalo_response.json()

def get_cephalo(cephalo_id):
    measurements_response = requests.get(f"http://backend/api/v1/cephalo/cephalo/{cephalo_id}")
    return measurements_response.json()

def get_image(cephalo_id):
    print(f"Getting cephalo for {cephalo_id}")
    image_response = requests.get(f"http://backend/api/v1/cephalo/images/{cephalo_id}")
    path='image.jpg'
    if image_response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in image_response:
                f.write(chunk)
    return Image.open(path)

def get_items_from_server():
    # request_auth = requests.post("http://backend/api/v1/login/access-token",
    # data={'username':"admin@cephalo-landmarks.com", 'password': "admincephalo"})
    # auth_access_token = return_string.json()["access_token"]
    auth_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTExNjUxMjAsInN1YiI6IjEifQ.d64k30hZiaGLwLKivxzKzIlIow0KURjBrWyWhX7DTKE"
    headers = {"Authorization": f"Bearer {auth_access_token}"}
    items_response = requests.get("http://backend/api/v1/items/?skip=0&limit=100", headers=headers)
    return items_response.json()

def get_landmarks(cephalo_id: int, progress_bar):
    landmarks_response = requests.get("http://backend/api/v1/cephalo/landmarks", params={'cephalo_id': str(cephalo_id)},)
    total_landmarks_count = 20
    with st.empty():
        while len(landmarks_response.json()) != total_landmarks_count:
            time.sleep(2)
            landmarks_response = requests.get("http://backend/api/v1/cephalo/landmarks", params={'cephalo_id': str(cephalo_id)},)
            st.write(f"Have {len(landmarks_response.json())} landmarks out of {total_landmarks_count}")
            progress_bar.progress(len(landmarks_response.json())/total_landmarks_count)

        st.write(f"{len(landmarks_response.json())} out of {total_landmarks_count} total landmarks")
        progress_bar.progress(len(landmarks_response.json())/total_landmarks_count)

    return landmarks_response.json()

def landmarks_json_to_np(cephalo_json):
    landmarks_arr = []
    start_time = time.now()
    for landmark in cephalo_json:
        landmarks_arr.append([landmark["landmark_x"], landmark["landmark_y"]])
        if (time.now() - start_time) > 60:
            break
    return landmarks_arr

def post_image(upload_image, px_to_cm_ratio):
    post_params = {'file': (upload_image.name, upload_image.read(), 'image/jpeg')}
    payload = {'px_per_cm': px_to_cm_ratio}
    r = requests.post("http://backend/api/v1/cephalo/predict", files=post_params, data=payload)
    return r.json()

def show_landmarks(image, landmarks, ax, ground_truth=None):
    """Show image with landmarks"""
    ax.imshow(image, cmap='gray')

    if landmarks is not None:
        ax.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r', label="Prediction")
        for index, landmark in enumerate(landmarks):
            ax.annotate(index, xy=(landmark[0], landmark[1]))
    if ground_truth is not None:
        ax.scatter(ground_truth[:, 0], ground_truth[:, 1], s=10, marker='.', c='b', label="Ground Truth")

    plt.pause(0.001)

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

def plot_landmarks_on_ax(xy_points, ax):
    if len(xy_points)==3:
        plot_ABC_angle_info(xy_points[0], xy_points[1], xy_points[2], ax, 'ro-')
    else:
        cephalo_angle  = cephaloConstants.angle_between_four_points(xy_points[0], xy_points[1], xy_points[2], xy_points[3])

        intersect_x, intersect_y = cephaloConstants.point_of_line_intersection(xy_points[0], xy_points[1], xy_points[2], xy_points[3])
        intersection = [intersect_x, intersect_y]

        segment1_point_closest_to_intersection, segment1_point_furthest_from_intersection = cephaloConstants.sort_points_from_intersection(xy_points[0], xy_points[1], intersection)
        segment2_point_closest_to_intersection, _ = cephaloConstants.sort_points_from_intersection(xy_points[2], xy_points[3], intersection)


        cephalo_intersect_angle  = cephaloConstants.angle_between_three_points(segment1_point_closest_to_intersection,intersection,segment2_point_closest_to_intersection)

        if round(cephalo_angle, 3) != round(cephalo_intersect_angle, 3):
            #draw arc for the obtuse angle
            print(f"4point angle and intersect angle do not match")
            print(f"cephalo_angle {cephalo_angle}, cephalo_intersect_angle {cephalo_intersect_angle}")
            temp = segment1_point_closest_to_intersection
            segment1_point_closest_to_intersection = segment1_point_furthest_from_intersection
            segment1_point_furthest_from_intersection = temp

        ax.plot(xy_points[:2, 0], xy_points[:2, 1], 'ro-')
        ax.plot(xy_points[2:, 0], xy_points[2:, 1], 'bo-')
        plot_ABC_angle_info(segment1_point_closest_to_intersection, intersection, segment2_point_closest_to_intersection, ax, 'go--')

def plot_distances_on_ax(xy_points, ax):
    if len(xy_points)==3:
        p1=xy_points[1]
        p2=xy_points[2]
        p3=xy_points[0]

        dx, dy = p2-p1
        det = dx*dx + dy*dy
        a = (dy*(p3[1]-p1[1])+dx*(p3[0]-p1[0]))/det
        p4 = [p1[0]+a*dx, p1[1]+a*dy]

        ax.scatter(xy_points[0][0], xy_points[0][1])
        ax.plot(xy_points[1:, 0], xy_points[1:, 1], 'bo-')
        plot_ABC_angle_info(p2, p4, p3, ax, 'go--')
    elif len(xy_points)==4:
        p1 = xy_points[0]
        p2 = xy_points[1]
        p3 = xy_points[2]
        p4 = xy_points[3]

        # import pdb; pdb.set_trace()
        ax.plot(xy_points[:2, 0], xy_points[:2, 1], 'o-')
        ax.plot(xy_points[2:, 0], xy_points[2:, 1], 'o-')


def format_multiselect_string(option_str):
    return "-".join(option_str)

def format_measurement_column(measuemrents_series):
    if measuemrents_series.unit == "deg":
        measuemrents_series.value = f"{measuemrents_series.value}°"
    elif measuemrents_series.unit == "cm":
        measuemrents_series.value = f"{measuemrents_series.value}cm"

    return measuemrents_series

@st.cache(allow_output_mutation=True)
def Cephalo_Id():
    return []

def run_cephalo_app():
    persist_cephalo_id = Cephalo_Id()

    st.title("Cephalometric Landmarks3")

    st.write("The model marks 20 landmarks on a cephalometric xray for orthodontists.")

    st.write("# Input")

    st.write("## Load example xray and predictions")
    cephalo_example = st.selectbox("Example Image", list(CEPHALO_EXAMPLES), index=0)
    get_example_button = st.button("Show Example Image")

    st.write("## Or upload own xray")

    uploaded_file = st.file_uploader("Upload a cephalometric image to the model", type=["jpg"])
    px_to_cm = st.number_input("Number of px per cm in the image, for calculations", min_value=1, value=13)
    get_landmarks_button = st.button("Get landmarks for image and px_to_cm ratio")

    st.write("# Output")

    if get_landmarks_button:
        if uploaded_file != None:
            post_response_json = post_image(uploaded_file, px_to_cm_ratio=px_to_cm)
            persist_cephalo_id.insert(0, post_response_json["id"])
        else:
            st.warning("No file uploaded")
            return

    if get_example_button or len(persist_cephalo_id) == 0:
        persist_cephalo_id.insert(0, CEPHALO_EXAMPLES[cephalo_example])

    cephalo_id = persist_cephalo_id[0]

    st.write(f"Landmarks for Cephalo Id {cephalo_id}")

    my_bar = st.progress(0)
    landmarks_pd = pd.DataFrame(get_landmarks(cephalo_id, my_bar), columns=['landmark_number', 'landmark_x', 'landmark_y'])

    measurements_df = pd.DataFrame(get_measurements(cephalo_id), columns=["measurement_name", "value", "unit"])
    uploaded_image = get_image(cephalo_id)
    st.write(f"Image size is {uploaded_image.size}, optimal size is (502, 512)")
    ## Show Image with landmarks


    fig = plt.figure(1)
    ax = fig.add_subplot(1, 1, 1)
    show_landmarks(uploaded_image, landmarks_pd[["landmark_x", "landmark_y"]].to_numpy(), ax)
    ax.legend()

    st.write(fig)
    st.write(landmarks_pd)

    ## Show Image with Angles
    st.write("Angles")
    possible_angles = []

    for angle in cephaloConstants.angles_list:
        if cephaloConstants.can_calculate_measurement(angle):
            possible_angles.append(angle)

    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.imshow(uploaded_image, cmap='gray')

    selected_angles = st.multiselect("Select Angles to be displayed", options=possible_angles, default=[possible_angles[0]], format_func=format_multiselect_string)

    for angle in selected_angles:
        landmark_ids  = []
        for x in angle:
            landmark_ids.extend(cephaloConstants.acronym_to_landmark_ids(x))
        landmarks_xy = []
        for landmark in landmark_ids:
            landmarks_np = landmarks_pd.loc[landmarks_pd['landmark_number']==landmark][["landmark_x", "landmark_y"]].to_numpy()[0]
            landmarks_xy.append(landmarks_np)
            ax2.annotate(cephaloConstants.acronym_from_landmark_id(landmark), tuple(landmarks_np))
        #plot it on ax2
        plot_landmarks_on_ax(np.array(landmarks_xy), ax2)

    st.pyplot(fig2)
    st.write(measurements_df[measurements_df["unit"]=="deg"].set_index("measurement_name").apply(format_measurement_column, axis=1)["value"])

    ## Show Image with Distances
    st.write("Distances")
    possible_distances = []

    for distance in cephaloConstants.distance_list:
        if cephaloConstants.can_calculate_measurement(distance):
            possible_distances.append(distance)

    fig3 = plt.figure(3)
    ax3 = fig3.add_subplot(1, 1, 1)
    ax3.imshow(uploaded_image, cmap='gray')

    selected_distances = st.multiselect("Select Distances to be displayed", options=possible_distances, default=[possible_distances[0]], format_func=format_multiselect_string)

    for distance in selected_distances:
        landmark_ids  = []
        for x in distance:
            landmark_ids.extend(cephaloConstants.acronym_to_landmark_ids(x))
        landmarks_xy = []
        for landmark in landmark_ids:
            landmarks_np = landmarks_pd.loc[landmarks_pd['landmark_number']==landmark][["landmark_x", "landmark_y"]].to_numpy()[0]
            landmarks_xy.append(landmarks_np)
            ax3.annotate(cephaloConstants.acronym_from_landmark_id(landmark), tuple(landmarks_np))
        #plot it on ax2
        plot_distances_on_ax(np.array(landmarks_xy), ax3)

    st.pyplot(fig3)
    cephalo_json = get_cephalo(cephalo_id)
    if 'px_per_cm' in cephalo_json:
        st.write(f"px per cm: {get_cephalo(cephalo_id)['px_per_cm']}")
    st.write("List of calculated measuemrents:")
    st.write(measurements_df[measurements_df["unit"]=="cm"].set_index("measurement_name").apply(format_measurement_column, axis=1)["value"])

if __name__ == "__main__":
    run_cephalo_app()
