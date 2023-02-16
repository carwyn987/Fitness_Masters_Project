import cv2
import argparse
import numpy as np

def load(thermal1_path, thermal2_path):
    print("Loading (1) ", thermal1_path, ", (2) ", thermal2_path)
    thermal1 = cv2.imread(thermal1_path)
    thermal2 = cv2.imread(thermal2_path)
    assert thermal1.shape == thermal2.shape

    return (thermal1, thermal2)

def computeDifference(thermal1, thermal2, out):
    compare = np.concatenate((thermal1, np.zeros((thermal1.shape[0],40,3)), thermal2), axis=1)
    difImg = thermal2 - thermal1
    
    cv2.imshow("Compare Images", compare)
    cv2.waitKey(1500)
    cv2.destroyAllWindows()

    cv2.imshow("Difference Image", difImg)
    cv2.waitKey(1500)
    cv2.destroyAllWindows()

    cv2.imwrite(out + "comparison.png", compare)
    cv2.imwrite(out + "output.png", difImg)

    return difImg

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Segmentation Masks.')
    parser.add_argument('-thermal1')
    parser.add_argument('-thermal2')
    parser.add_argument('-out')

    args = parser.parse_args()

    thermal1, thermal2 = load(args.thermal1, args.thermal2)
    difImg = computeDifference(thermal1, thermal2, args.out)