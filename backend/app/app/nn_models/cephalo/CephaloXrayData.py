import os
import torch
from PIL import Image
from torch.utils.data import Dataset
import numpy as np
import torchvision.transforms as transforms
import pandas as pd
from app.nn_models.cephalo.cephaloConstants import IMG_SIZE_ORIGINAL, IMG_SIZE_ROUNDED_TO_64, IMG_TRANSFORM_PADDING, IMAGE_PATH

class HeadXrays(Dataset):

    def __init__(self, directory, junior=True):
        self.anno_dir = os.path.join(directory)
        self.anno_df = pd.read_csv(os.path.join(self.anno_dir, "cephalo_landmarks.csv"))

        img_dir = os.path.join(directory, "images")

        images = filter(lambda f: not f.startswith("."), os.listdir(img_dir))

        parse_id = lambda img: int(img.split(".jpg")[0])

        images = [(parse_id(img), img) for img in images]

        images.sort(key = lambda x: x[0])

        self.files = np.array([ (os.path.join(img_dir,img[1]),) + self.loadAnnotations(img[1]) for img in images ])

        print("File Shape:", self.files.shape)

    def loadAnnotations(self,id):
        anno = ()

        anno_row = self.anno_df[self.anno_df['filename'].str.match(id)]
        if (anno_row.shape[0] == 0):
            print("No annotation for this image: ", id)
            raise
        landmarks_list = anno_row.to_numpy()[0, :40].astype('float')
        anno = (np.reshape(landmarks_list, [-1, 2]),)

        return anno

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        path, doc_anno = self.files[idx]
        print(path)
        image = Image.open(path)

        return image, doc_anno


    def __len__(self):
        return len(self.files)


class HeadXrayAnnos(HeadXrays):
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        return self.files[idx]



class Transform(Dataset):
    def __init__(self, dataset, indices=None, tx=lambda x:x, ty=lambda x:x):
        self.dataset = dataset
        self.tx = tx
        self.ty = ty
        if indices is None:
            indices = np.arange(len(self.dataset))
        self.indices = indices

    def __getitem__(self, idx):
        x, doc_anno = self.dataset[self.indices[idx]]
        return self.tx(x), self.ty(doc_anno)

    def __len__(self):
        return len(self.indices)

class TransformedHeadXrayAnnos(Transform):
    def __init__(self, indices, landmarks):
        tx = lambda x: x

        middle = np.array([IMG_SIZE_ROUNDED_TO_64['width'], IMG_SIZE_ROUNDED_TO_64['height']]) / 2

        ty = lambda x: (x[landmarks] - middle) / float(IMG_SIZE_ROUNDED_TO_64['width']) * 2
        path = IMAGE_PATH
        # if 'SLURM_TMPDIR' in os.environ:
        #     path = os.path.join(os.environ['SLURM_TMPDIR'],'RawImage')
        super().__init__(HeadXrays(path),indices = indices,tx=tx,ty=ty)

class TransformedXrays(Transform):
    def __init__(self, indices, landmarks):
        tx = transforms.Compose([
            transforms.Pad((0, 0, IMG_TRANSFORM_PADDING['width'], IMG_TRANSFORM_PADDING['height'])),
            transforms.ToTensor(),
            lambda x: x[:, :, :IMG_SIZE_ROUNDED_TO_64['width']].sum(dim=0, keepdim=True),
            transforms.Normalize([1.4255656], [0.8835338])])

        middle = np.array([IMG_SIZE_ROUNDED_TO_64['width'], IMG_SIZE_ROUNDED_TO_64['height']]) / 2

        ty = lambda x: (x[landmarks] - middle) / float(IMG_SIZE_ROUNDED_TO_64['width']) * 2
        path = IMAGE_PATH
        # if 'SLURM_TMPDIR' in os.environ:
        #     path = os.path.join(os.environ['SLURM_TMPDIR'],'RawImage')
        super().__init__(HeadXrays(path),indices = indices,tx=tx,ty=ty)

def get_train_val(landmarks, trainset, valset):
    splits = ['train', 'val']

    ranges = {'train': trainset, 'val': valset}

    datasets = {x: TransformedXrays(indices=ranges[x], landmarks=landmarks) for x in splits}

    return splits, datasets

def get_folded(landmarks, fold, num_folds, fold_size, batchsize):
    folds = np.arange(num_folds * fold_size).reshape(num_folds, fold_size)
    val_fold = fold == np.arange(num_folds)
    val_set = folds[val_fold].flatten()
    train_set = folds[~val_fold].flatten()

    print("Trainset: ", train_set)
    print("ValSet", val_set)

    splits, datasets = get_train_val(landmarks, train_set, val_set)
    annos = TransformedHeadXrayAnnos(indices=train_set, landmarks=landmarks)
    dataloaders = {x: torch.utils.data.DataLoader(datasets[x],
                                                  batch_size=batchsize, shuffle=(x == 'train'), num_workers=2,
                                                  pin_memory=True)
                   for x in splits}

    return splits, datasets, dataloaders, annos

def get_shuffled(landmarks, seed):

    splits = ['train', 'val', 'test']

    train_val = np.arange(360)
    np.random.seed(seed)
    np.random.shuffle(train_val)
    train = train_val[:324]
    val = train_val[324:]

    ranges = {'train': train, 'val': val, 'test': np.arange(360, 400)}

    datasets = {x: TransformedXrays(indices=ranges[x], landmarks = landmarks) for x in splits}

    return splits, datasets

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    def show_landmarks(image, landmarks):
        """Show image with landmarks"""
        plt.imshow(image, cmap='gray')
        plt.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r')
        plt.pause(0.001)  # pause a bit so that plots are updated

    plt.figure()

    xrays = TransformedXrays(indices=[0], landmarks=[14])[0]
    middle = np.array([IMG_SIZE_ROUNDED_TO_64['width'], IMG_SIZE_ROUNDED_TO_64['height']]) / 2
    recreated_points = ((xrays[1]*IMG_SIZE_ROUNDED_TO_64['width'])/2) + middle
    show_landmarks(xrays[0].numpy().transpose((1, 2, 0)), recreated_points)

    plt.show()
