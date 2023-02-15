import cv2
import sys
import numpy as np
from scipy import ndimage

def loadImgs(image_1_path, mask_1_path, image_2_path, mask_2_path):
    img1 = cv2.imread(image_1_path)
    mask1 = cv2.imread(mask_1_path)
    img2 = cv2.imread(image_2_path)
    mask2 = cv2.imread(mask_2_path)

    # Show images
    scx, scy = 5, 10
    cv2.imshow('images', np.concatenate((cv2.resize(np.concatenate((img1,img2), axis=1), (img1.shape[1]//scx, img1.shape[0]//scy)), cv2.resize(np.concatenate((mask1,mask2), axis=1), (img1.shape[1]//scx, img1.shape[0]//scy))), axis=0))
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    return (img1, mask1, img2, mask2)

def compute_center(mask):
    # Let's take only one layer of the mask
    layer1 = mask[:,:,0]
    layer1[layer1 > 1] = 1

    center_coordinates = (int(ndimage.center_of_mass(layer1)[0]), int(ndimage.center_of_mass(layer1)[1]))
  
    # Show image
    show_center_coordinates = (center_coordinates[0]//5, center_coordinates[1]//5)
    radius = 20
    color = (255, 0, 0)
    thickness = 2
    scl = 5
    image = cv2.circle(cv2.resize(mask, (mask.shape[0]//scl, mask.shape[0]//scl)), show_center_coordinates, radius, color, thickness)
    # Displaying the image 
    cv2.imshow("center", image)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    print(center_coordinates)

    return center_coordinates

if __name__ == "__main__":

    image_1_path = sys.argv[1]
    mask_1_path = sys.argv[2]
    image_2_path = sys.argv[3]
    mask_2_path = sys.argv[4]

    print("Loading images from sources\n   (1)", image_1_path, "\n   (2)", mask_1_path, "\n   (3)", image_2_path, "\n   (4)", mask_2_path)

    img1, mask1, img2, mask2 = loadImgs(image_1_path, mask_1_path, image_2_path, mask_2_path)

    center_m1 = compute_center(mask1)
    center_m2 = compute_center(mask2)

