from typing import Tuple
import os
from PIL import Image
import torchvision.transforms.functional as TF
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as transforms

from app.nn_models.cephalo import model as m
from app.nn_models.cephalo import pyramid
from app.nn_models.cephalo import cephaloConstants
from app.nn_models.cephalo import CephaloXrayData

def rescale_point_to_original_size(point):
    middle = np.array([cephaloConstants.IMG_SIZE_ROUNDED_TO_64['width'], cephaloConstants.IMG_SIZE_ROUNDED_TO_64['height']]) / 2
    return ((point*cephaloConstants.IMG_SIZE_ROUNDED_TO_64['width'])/2) + middle

def show_landmarks(image, landmarks, ground_truth=None):
    """Show image with landmarks"""
    plt.imshow(image, cmap='gray')
    plt.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r', label="Prediction")
    if ground_truth is not None:
        plt.scatter(ground_truth[:, 0], ground_truth[:, 1], s=10, marker='.', c='b', label="Ground Truth")
    # plt.figlegend('', ('Red', 'Blue'), 'center left')
    plt.pause(0.001)  # pause a bit so that plots are updated


def get_prediction(img_path: str, landmark: int) -> Tuple[float, float]:
    levels = 6
    path = os.path.join(os.getcwd(), "app", "nn_models/cephalo/models/big_cephalo_0_0")
    setting = {"loadpath": path}
    device = 'cpu'
    model = m.load_model(levels=levels, name=setting["loadpath"], device=device, load=True)
    model.eval()

    phase = 'val'
    inputs = Image.open(img_path)

    tx = transforms.Compose([
        transforms.Pad((0, 0, cephaloConstants.IMG_TRANSFORM_PADDING['width'], cephaloConstants.IMG_TRANSFORM_PADDING['height'])),
        transforms.ToTensor(),
        lambda x: x[:, :, :cephaloConstants.IMG_SIZE_ROUNDED_TO_64['width']].sum(dim=0, keepdim=True),
        transforms.Normalize([1.4255656], [0.8835338])])

    x = tx(inputs)
    x.unsqueeze_(0)
    inputs_tensor = x.to(device)

    annos = CephaloXrayData.TransformedHeadXrayAnnos(indices=None, landmarks=[landmark])

    pnts = np.stack(list(map(lambda x: x[1], annos)))
    means = torch.tensor(pnts.mean(0, keepdims=True), device=device, dtype=torch.float32)

    pym = pyramid.pyramid(inputs_tensor, levels)
    guess = 0
    with torch.set_grad_enabled(False):
        guess = means
        for j in range(10):
            outputs = guess + model(pym, guess,
                                    phase == 'train')  # ,j==2 and i==0 and phase=='val' and False,rando)
            guess = outputs.detach()

    recreated_points = rescale_point_to_original_size(guess[0][0].numpy())

    return (recreated_points[0], recreated_points[1])

if __name__=="__main__":
    landmark = 0
    example_input = 0
    dataset = CephaloXrayData.HeadXrays(cephaloConstants.IMAGE_PATH);
    img_path = dataset[example_input][0].filename
    landmarks_gt = [dataset[example_input][1][landmark]]

    image_path = os.path.join(img_path)
    landmark_x, landmark_y = get_prediction(image_path, landmark=landmark)

    ax = plt.subplot(1, 1, 1)
    plt.tight_layout()
    plot_dict = {
    'image': Image.open(image_path).convert('L'),
    'landmarks': np.array([[landmark_x, landmark_y]]),
    'ground_truth': np.array(landmarks_gt)
    }

    plt.legend()
    show_landmarks(**plot_dict)
    plt.show()
