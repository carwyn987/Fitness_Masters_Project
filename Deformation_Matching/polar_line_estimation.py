import cv2
import sys
import math
import time
from tqdm import tqdm
import numpy as np
from scipy import ndimage

def dist(t1, t2):
    return ((t1[0] - t2[0])**2 + (t1[1] - t2[1])**2)**0.5

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
    img1 = cv2.resize(img1, (img1.shape[1]//scl, img1.shape[0]//scl))
    mask1 = cv2.resize(mask1, (mask1.shape[1]//scl, mask1.shape[0]//scl))
    img2 = cv2.resize(img2, (img2.shape[1]//scl, img2.shape[0]//scl))
    mask2 = cv2.resize(mask2, (mask2.shape[1]//scl, mask2.shape[0]//scl))

    return (img1, mask1, img2, mask2)

def compute_center(mask, saveFile, showprocess=False, save=True):
    # Let's take only one layer of the mask
    layer1 = mask[:,:,0].copy()
    layer1[layer1 > 1] = 1

    center_coordinates = (int(ndimage.center_of_mass(layer1)[0]), int(ndimage.center_of_mass(layer1)[1]))

    # put circle on image
    scl = 1
    image = cv2.circle(cv2.resize(mask, (mask.shape[0]//scl, mask.shape[0]//scl)), (center_coordinates[0]//scl, center_coordinates[1]//scl), 20, (255, 0, 0), 2)


    if showprocess:    
        cv2.imshow("center", image)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    
    if save:
        cv2.imwrite(saveFile, image)

    print(center_coordinates)
    return center_coordinates


def compute_polar_line(mask, center, saveFile, showprocess=False, save=True):

    print("Starting edge search for image: ", saveFile)
    start = time.perf_counter()

    # set masks
    show_mask = mask.copy()
    singled_mask = mask[:,:,0].squeeze().copy()

    # Test 360 "rays" for each mask
    numrays = 2000 # [1,360)
    moveby = 1

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
        while search_pnt[0] < singled_mask.shape[0] and search_pnt[0] > 0 and search_pnt[1] < singled_mask.shape[1] and search_pnt[1] > 0:
            
            cur_pnt = True if singled_mask[search_pnt[0], search_pnt[1]] > 0 else False
            
            if cur_pnt == False and last_pnt == True:
                leaving_points.append((search_pnt[0], search_pnt[1], angle))
                if save:
                    # Modifying the show point breaks the code???
                    cv2.drawMarker(show_mask, (search_pnt[1], search_pnt[0]),(255,0,0), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
            else:
                if showprocess:
                    cv2.drawMarker(show_mask, (search_pnt[1], search_pnt[0]),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
                pass

            if showprocess:
                # Show image
                cv2.imshow("center", show_mask)
                cv2.waitKey(100)
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
            outline.append((search_pnt[0], search_pnt[1], angle))
            pass

        angle += 360.0/numrays
        # print("Angle: ", angle)
    
    print("Total time to process image points = ", time.perf_counter() - start)

    # Print Image
    if showprocess:
        print("Visualizing points:")
        start = time.perf_counter()
        for item in outline:
            if len(outline) > 1:
                for item2 in outline:
                    cv2.drawMarker(show_mask, tuple(item2),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
            else:
                cv2.drawMarker(show_mask, tuple(item),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
        
        cv2.imshow("center", show_mask)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        print("Total time to visualizeimage points = ", time.perf_counter() - start)

    if save:
        cv2.imwrite(saveFile, show_mask)

    # print(len(outline))
    return outline

def visualize_pairs(img1, m1_edge_pts, img2, m2_edge_pts):

    img1_cp = img1.copy()
    img2_cp = img2.copy()

    for i in range(len(m1_edge_pts)):
        if i%25 == 0:
            cv2.drawMarker(img1_cp, (m1_edge_pts[i][1], m1_edge_pts[i][0]),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
            cv2.drawMarker(img2_cp, (m2_edge_pts[i][1], m2_edge_pts[i][0]),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=20, thickness=3, line_type=cv2.LINE_AA)
            # show concat
            cv2.imshow("center", np.concatenate((img1_cp, img2_cp), axis=1))
            cv2.waitKey(150)
            cv2.destroyAllWindows()

# Need to add thermal image
def deform_image(img2, center, m1_edge_pts, m2_edge_pts, fileName):
    
    print("Starting Image Deformation")
    start = time.perf_counter()
    new_img2 = img2.copy()

    stepsize = 25
    kernel_width = 10

    # Iterate over all angle copies saved
    assert len(m1_edge_pts) == len(m2_edge_pts)
    for i in tqdm(range(len(m1_edge_pts))):
        # compute ratio:
        # print("dist: ", m1_edge_pts[i], ", ", center)
        m1_center_dist = dist(m1_edge_pts[i], center)
        m2_center_dist = dist(m2_edge_pts[i], center)
        ratio = m2_center_dist/m1_center_dist

        # print("x: ", (m2_edge_pts[i][0] - m1_edge_pts[i][0]), ", y: ", (m2_edge_pts[i][1] - m1_edge_pts[i][1]))
        # angle = math.radians(math.atan(float((m2_edge_pts[i][0] - m1_edge_pts[i][0]))/(m2_edge_pts[i][1] - m1_edge_pts[i][1])))
        # print("Angle: ", math.degrees(angle))
        angle = math.radians(m1_edge_pts[i][2])
        # print("Angle: ", angle)

        movedby = 0

        # Iterate over original image between center and edge, and recompute pixel placement in copied image
        search_pnt = np.array(center)
        while dist(tuple(search_pnt), center) <= dist(center, m1_edge_pts[i]):

            # print(movedby, dist(tuple(search_pnt), center))
            search_pnt[0] = center[0] + movedby*math.sin(angle)
            search_pnt[1] = center[1] + movedby*math.cos(angle)

            scaled_pnt_y = int(center[0] + movedby*math.sin(angle)*ratio)
            scaled_pnt_x = int(center[1] + movedby*math.cos(angle)*ratio)

            # Update transformed image
            try:
                new_img2[scaled_pnt_y, scaled_pnt_x] = img2[search_pnt[0], search_pnt[1]]
                # Do kernel operation
                new_img2[scaled_pnt_y-(kernel_width//2):scaled_pnt_y+(kernel_width//2), scaled_pnt_x-(kernel_width//2):scaled_pnt_x+(kernel_width//2)] = img2[search_pnt[0]-(kernel_width//2):search_pnt[0]+(kernel_width//2), search_pnt[1]-(kernel_width//2):search_pnt[1]+(kernel_width//2)]
            except:
                break


            # cv2.drawMarker(new_img2, (search_pnt[1], search_pnt[0]),(0,0,255), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=2, thickness=3, line_type=cv2.LINE_AA)
            # cv2.imshow("center", new_img2)
            # cv2.waitKey(30)
            # cv2.destroyAllWindows()

            # print("Point: (", scaled_pnt_y, ", ", scaled_pnt_x, ") moved to position ", search_pnt)

            # Update point location
            movedby += stepsize

    cv2.imwrite(fileName, new_img2)
    print("Total time to deform = ", time.perf_counter() - start)
    pass

if __name__ == "__main__":

    image_1_path = sys.argv[1]
    mask_1_path = sys.argv[2]
    image_2_path = sys.argv[3]
    mask_2_path = sys.argv[4]

    print("Loading images from sources\n   (1)", image_1_path, "\n   (2)", mask_1_path, "\n   (3)", image_2_path, "\n   (4)", mask_2_path)

    img1, mask1, img2, mask2 = loadImgs(image_1_path, mask_1_path, image_2_path, mask_2_path)
    img1, mask1, img2, mask2 = resizeImgs(img1, mask1, img2, mask2)
    assert img1.shape == mask1.shape
    assert img2.shape == mask2.shape

    center_m1 = compute_center(mask1, "computed_images/m1_center.png")
    center_m2 = compute_center(mask2, "computed_images/m2_center.png")

    x1 = (center_m1[0] + center_m2[0])//2
    x2 = (center_m1[1] + center_m2[1])//2
    center = (x1,x2)

    m1_edge_pts = compute_polar_line(mask1, center, "computed_images/m1_edges.png")
    m2_edge_pts = compute_polar_line(mask2, center, "computed_images/m2_edges.png")

    # visualize_pairs(img1, m1_edge_pts, img2, m2_edge_pts)

    # Now we have the centers, edges, and the lines that connect them. We simply have to "extend" the lines of pixels in one image to the other image.
    deform_image(img1, center, m1_edge_pts, m2_edge_pts, "computed_images/deformed_" + sys.argv[1].split('/')[-1])