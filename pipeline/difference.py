import cv2
import argparse
import numpy as np

def load(thermal1_path, thermal2_path):
    print("Loading (1) ", thermal1_path, ", (2) ", thermal2_path)
    thermal1 = cv2.imread(thermal1_path)
    thermal2 = cv2.imread(thermal2_path)
    assert thermal1.shape == thermal2.shape

    return (thermal1, thermal2)

def scale(thermal1, thermal2):
    others = 126
    thermal1[:,:,2] = thermal1[:,:,0] + thermal1[:,:,1] + thermal1[:,:,2] // 3
    thermal1[:,:,1] = others
    thermal1[:,:,0] = others
    thermal2[:,:,2] = thermal2[:,:,0] + thermal2[:,:,1] + thermal2[:,:,2] // 3
    thermal2[:,:,1] = others
    thermal2[:,:,0] = others

def computeDif(thermal1, thermal2):
    # scale from [-255,255] to [0,255]
    t1 = thermal1[:,:,0] + thermal1[:,:,1] + thermal1[:,:,2] // 3
    t2 = thermal2[:,:,0] + thermal2[:,:,1] + thermal2[:,:,2] // 3

    scaleup = 1.25
    scaledown = 0.75

    dif = (t2 - t1).astype(np.float64)
    difb = dif.copy().astype(np.float64)
    difr = dif.copy().astype(np.float64)
    difb[difb < 0] *= scaledown
    difr[difr > 0] *= scaleup

    # rerange
    dif = dif//2 + (255//2)
    difr = difr//2 + (255//2)
    difb = difb//2 + (255//2)

    res = np.stack((dif, dif, dif), axis=2).astype(np.uint8)

    return res

def computeDifference(thermal1, thermal2, out):
    compare = np.concatenate((thermal1, np.zeros((thermal1.shape[0],40,3)), thermal2), axis=1)
    difImg = thermal1 - thermal2
    # difImg = computeDif(thermal1, thermal2)
    
    cv2.imshow("Compare Images", compare)
    cv2.waitKey(1500)
    cv2.destroyAllWindows()

    cv2.imshow("Difference Image", difImg)
    cv2.waitKey(15000)
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
    # scale(thermal1, thermal2)
    difImg = computeDifference(thermal1, thermal2, args.out)