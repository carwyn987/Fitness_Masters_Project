import os, os.path
import cv2
import torch
from tqdm import tqdm
import numpy as np
import sys
import time

def load_and_split(folder):
    data, labels = load(folder)

    # Just as a thought experiment
    print(f'image data in memory is of size: {data.nbytes}, labels in memory is of size: {labels.nbytes}')
    print(f'this equates to approximately {(100*(data.nbytes + labels.nbytes)/(64157.8 * 1049000)):8.6f}% of main memory on my machine (was ~30% before downsampling)')

    return split(data, labels)
    
'''
Given a relative path to a data folder with the following structure, load images into a data tensor.

relative_folder/
    images/
        img1_filename.jpg
        ...
    masks/
        mask1_filename.png
        ...

One notable design decision in the load() function is that we assume that the images are all the same size, and the width and height can be swapped (landscape and portrait are both supported).
'''
def load(folder):
    img_data_folder = os.path.join(folder, "images")
    mask_data_folder = os.path.join(folder, "masks")

    # Create tensor to hold data
    img_names = [os.path.join(img_data_folder, name) for name in os.listdir(img_data_folder) if os.path.isfile(os.path.join(img_data_folder, name))]
    num_images = len(img_names)
    print(f'Loading {num_images} observations.')

    scaleFactor = 32
    h,w,c = cv2.imread(img_names[0], cv2.IMREAD_COLOR).shape
    print(f'Each image has width: {w}, height: {h}, channels: {c}')

    data = np.zeros([num_images,c,h//scaleFactor,w//scaleFactor], dtype=float)
    print(f'New data size is (width, height): {(data.shape[3], data.shape[2])}')

    print("Loading images")
    for i in tqdm(range(num_images)):
        img = cv2.normalize(cv2.resize(cv2.imread(img_names[i], cv2.IMREAD_COLOR), (data.shape[3], data.shape[2]), interpolation = cv2.INTER_AREA), None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        try:
            data[i] = np.moveaxis(img, 2,0)
        except ValueError:
            try:
                data[i] = np.swapaxes(np.moveaxis(img, 2,0), 1,2)
            except:
                raise RuntimeError('Input image size is ambiguous and is not universal.')
    
    # Create tensor to hold labels
    mask_names = [os.path.join(mask_data_folder, name.rsplit('/', 1)[-1].rsplit('.', 1)[0] + ".png") for name in img_names]
    labels = np.zeros([num_images,c,h//scaleFactor,w//scaleFactor], dtype=float)
    print("Loading labels")
    for i in tqdm(range(num_images)):
        img = cv2.normalize(cv2.resize(cv2.imread(mask_names[i], cv2.IMREAD_COLOR), (data.shape[3], data.shape[2]), interpolation = cv2.INTER_AREA), None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        try:
            labels[i] = np.moveaxis(img, 2,0)
        except ValueError:
            try:
                labels[i] = np.swapaxes(np.moveaxis(img, 2,0), 1,2)
            except:
                raise RuntimeError('Input mask size is ambiguous and is not universal.')

    return data, labels

'''
validation - whether or not we want a validation set

returns (train_imgs, train_labels), (val_imgs, val_labels), (test_imgs, test_labels)
'''
def split(data, labels, validation=False):
    num_samples = data.shape[0]
    if validation:
        # to be implemented
        raise NotImplementedError
    else:
        train_size = (num_samples * 4) // 5
        test_size = (num_samples) // 5

    # training_set = np.choose()

    return (data[0:(num_samples * 4)//5, :, :, :], labels[0:(num_samples * 4)//5, :, :, :]), \
            None, \
            (data[(num_samples * 4)//5::, :, :, :], labels[(num_samples * 4)//5::, :, :, :])