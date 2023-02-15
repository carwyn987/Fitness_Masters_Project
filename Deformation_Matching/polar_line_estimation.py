import cv2
import sys
import math
import time
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

def resizeImgs(img1, mask1, img2, mask2):
    scl = 5
    img1 = cv2.resize(img1, (img1.shape[0]//scl, img1.shape[0]//scl))
    mask1 = cv2.resize(mask1, (mask1.shape[0]//scl, mask1.shape[0]//scl))
    img2 = cv2.resize(img2, (img2.shape[0]//scl, img2.shape[0]//scl))
    mask2 = cv2.resize(mask2, (mask2.shape[0]//scl, mask2.shape[0]//scl))

    return (img1, mask1, img2, mask2)

def compute_center(mask, saveFile):
    # Let's take only one layer of the mask
    layer1 = mask[:,:,0]
    layer1[layer1 > 1] = 1

    center_coordinates = (int(ndimage.center_of_mass(layer1)[0]), int(ndimage.center_of_mass(layer1)[1]))

    # Show image
    scl = 1
    image = cv2.circle(cv2.resize(mask, (mask.shape[0]//scl, mask.shape[0]//scl)), (center_coordinates[0]//scl, center_coordinates[1]//scl), 20, (255, 0, 0), 2)
    cv2.imshow("center", image)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    cv2.imwrite(saveFile, image)

    print(center_coordinates)
    return center_coordinates


def compute_polar_line(mask, center, saveFile, showprocess=False):

    start = time.perf_counter()

    # set masks
    show_mask = mask
    mask = mask[:,:,0].squeeze()

    # Test 360 "rays" for each mask
    numrays = 80 # [1,360)
    moveby = 2

    outline = []

    angle = 0
    while angle < 360:
        # Compute the first non-segmented pixel location
        # Compute the last segmented pixel location
        # Compute a point that "represents" the outermost point we need to keep
        # Keep in mind the previous ray's points (no huge jumps)

        # Search from center along angled line:
        leaving_points = []
        search_pnt = np.array(center)
        last_pnt = True # true represents in the segmented area
        cur_pnt = True # These two statements are assumptions
        movedby = 0
        while search_pnt[0] < mask.shape[0] and search_pnt[0] > 0 and search_pnt[1] < mask.shape[1] and search_pnt[1] > 0:
            
            cur_pnt = True if mask[search_pnt[1], search_pnt[0]] > 0 else False
            
            if cur_pnt == False and last_pnt == True:
                leaving_points.append((search_pnt[0], search_pnt[1]))
                if showprocess:
                    cv2.drawMarker(show_mask, tuple(search_pnt),(255,0,0), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
            else:
                if showprocess:
                    cv2.drawMarker(show_mask, tuple(search_pnt),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
                pass

            if showprocess:
                # Show image
                cv2.imshow("center", show_mask)
                cv2.waitKey(50)
                cv2.destroyAllWindows()

            # Update point location
            movedby += moveby
            search_pnt[0] = center[0] + movedby*math.sin(math.radians(angle))
            search_pnt[1] = center[1] + movedby*math.cos(math.radians(angle))

            last_pnt = cur_pnt
        
        # Add one leave point (or other estimate) to the outline
        try:
            outline.append(leaving_points[0])
        except:
            pass

        angle += 360/numrays
    
    print("Total time to process image points = ", time.perf_counter() - start)
    print("Visualizing points:")
    start = time.perf_counter()

    # Print Image
    for item in outline:
        if len(outline) > 1:
            for item2 in outline:
                cv2.drawMarker(show_mask, tuple(item2),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
        else:
            cv2.drawMarker(show_mask, tuple(item),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)

    print("Total time to visualizeimage points = ", time.perf_counter() - start)
    
    cv2.imshow("center", show_mask)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    cv2.imwrite(saveFile, show_mask)

    print(len(outline))

if __name__ == "__main__":

    image_1_path = sys.argv[1]
    mask_1_path = sys.argv[2]
    image_2_path = sys.argv[3]
    mask_2_path = sys.argv[4]

    print("Loading images from sources\n   (1)", image_1_path, "\n   (2)", mask_1_path, "\n   (3)", image_2_path, "\n   (4)", mask_2_path)

    img1, mask1, img2, mask2 = loadImgs(image_1_path, mask_1_path, image_2_path, mask_2_path)
    img1, mask1, img2, mask2 = resizeImgs(img1, mask1, img2, mask2)

    center_m1 = compute_center(mask1, "computed_images/m1_center.png")
    center_m2 = compute_center(mask2, "computed_images/m2_center.png")

    m1_edges = compute_polar_line(mask1, center_m1, "computed_images/m1_edges.png")
    m2_edges = compute_polar_line(mask2, center_m2, "computed_images/m2_edges.png")

    # Now we have the centers, edges, and the lines that connect them. We simply have to "extend" the lines of pixels in one image to the other image.

