import matplotlib.pyplot as plt
import numpy as np
import cv2

def plot_loss(y, title, xlabel, ylabel, filename=None):
    fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    ax.plot(np.arange(len(y)), y)
    fig.suptitle(title, fontsize='large')
    ax.set_xlabel(xlabel, fontsize='medium')
    ax.set_ylabel(ylabel, fontsize='medium')

    if filename:
        fig.savefig(filename)   # save the figure to file

def save_prediction(img, segmented, filename):

    # The segmented image will be 2d ... augment it to have 3 dimensions
    segmented = np.repeat(segmented[:, :, np.newaxis], 3, axis=2)

    # The image will be normalized, put back to 0-255 range
    segmented = cv2.normalize(segmented, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F).astype(np.uint8)
    img = cv2.normalize(img, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F).astype(np.uint8)

    # Concatenate img and segmented
    img_concat = np.concatenate((img,segmented), axis=1)

    # Save image
    cv2.imwrite(filename, img_concat)