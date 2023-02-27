import cv2
import sys
import math
import time
import argparse
from tqdm import tqdm
import numpy as np
from scipy import ndimage

def dist(t1, t2):
    return ((t1[0] - t2[0])**2 + (t1[1] - t2[1])**2)**0.5

def loadImgs(image_1_path, mask_1_path, thermal_1_path, image_2_path, mask_2_path, thermal_2_path):
    img1 = cv2.imread(image_1_path)
    mask1 = cv2.imread(mask_1_path)
    thermal1 = cv2.imread(thermal_1_path)
    img2 = cv2.imread(image_2_path)
    mask2 = cv2.imread(mask_2_path)
    thermal2 = cv2.imread(thermal_2_path)

    print("shapes: ", img1.shape, mask1.shape, thermal1.shape)

    # Show images
    scx, scy = 3, 6
    concat_img = np.concatenate(( cv2.resize(np.concatenate((img1,img2), axis=1), (img1.shape[1]//scx, img1.shape[0]//scy)), 
                                          cv2.resize(np.concatenate((mask1,mask2), axis=1), (img1.shape[1]//scx, img1.shape[0]//scy)), 
                                          cv2.resize(np.concatenate((thermal1,thermal2), axis=1), (img1.shape[1]//scx, img1.shape[0]//scy))
                                        ), axis=0)

    cv2.imshow('images', concat_img)
    cv2.waitKey(1500)
    cv2.destroyAllWindows()
    cv2.imwrite(out + "loaded_images.png", concat_img)

    return (img1, mask1, thermal1, img2, mask2, thermal2)

def resizeImgs(img1, mask1, thermal1, img2, mask2, thermal2, out):
    scl = 2
    img1 = cv2.resize(img1, (img1.shape[1]//scl, img1.shape[0]//scl))
    mask1 = cv2.resize(mask1, (mask1.shape[1]//scl, mask1.shape[0]//scl))
    thermal1 = cv2.resize(thermal1, (thermal1.shape[1]//scl, thermal1.shape[0]//scl))
    img2 = cv2.resize(img2, (img2.shape[1]//scl, img2.shape[0]//scl))
    mask2 = cv2.resize(mask2, (mask2.shape[1]//scl, mask2.shape[0]//scl))
    thermal2 = cv2.resize(thermal2, (thermal2.shape[1]//scl, thermal2.shape[0]//scl))

    cv2.imwrite(out + "thermal1.png", thermal1)
    cv2.imwrite(out + "thermal2.png", thermal2)

    return (img1, mask1, thermal1, img2, mask2, thermal2)

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
    numrays = 5000 # [1,360)
    moveby = 0.5

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
def deform_image(img2, center, m1_edge_pts, m2_edge_pts, thermal2, fileName, fileNameThermal):
    
    print("Starting Image Deformation")
    start = time.perf_counter()
    new_img2 = img2.copy()
    new_thermal = thermal2.copy()

    stepsize = 0.7
    kernel_width = 1

    # Iterate over all angle copies saved
    assert len(m1_edge_pts) == len(m2_edge_pts)
    for i in tqdm(range(len(m1_edge_pts))):
        # compute ratio:
        # print("dist: ", m1_edge_pts[i], ", ", center)
        m1_center_dist = dist(m1_edge_pts[i], center)
        m2_center_dist = dist(m2_edge_pts[i], center)
        ratio = m2_center_dist/m1_center_dist
        angle = math.radians(m1_edge_pts[i][2])

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
                new_thermal[scaled_pnt_y, scaled_pnt_x] = new_thermal[search_pnt[0], search_pnt[1]]
                # Do kernel operation
                new_img2[scaled_pnt_y-(kernel_width//2):scaled_pnt_y+(kernel_width//2), scaled_pnt_x-(kernel_width//2):scaled_pnt_x+(kernel_width//2)] = img2[search_pnt[0]-(kernel_width//2):search_pnt[0]+(kernel_width//2), search_pnt[1]-(kernel_width//2):search_pnt[1]+(kernel_width//2)]
                new_thermal[scaled_pnt_y-(kernel_width//2):scaled_pnt_y+(kernel_width//2), scaled_pnt_x-(kernel_width//2):scaled_pnt_x+(kernel_width//2)] = new_thermal[search_pnt[0]-(kernel_width//2):search_pnt[0]+(kernel_width//2), search_pnt[1]-(kernel_width//2):search_pnt[1]+(kernel_width//2)]
            except:
                break

            # Update point location
            movedby += stepsize

    cv2.imwrite(fileName, new_img2)
    cv2.imwrite(fileNameThermal, new_thermal)
    print("Total time to deform = ", time.perf_counter() - start)
    pass

def meshDeform():
    warped = cv2.remap(thermal2_dst,src,dst,cv2.INTER_LINEAR)

# Non-affine transformation
def cv2Deform(img2, center, m1_edge_pts, m2_edge_pts, thermal2, fileName, fileNameThermal):

    pts_src = m1_edge_pts
    pts_dst = m2_edge_pts

    print("ex: shape: ", pts_src[0], ", len: ", len(pts_src))

    unzipped_src = list(zip(*pts_src))
    unzipped_dst = list(zip(*pts_dst))
    print("unzipped_shape: ", unzipped_src[0], ", len: ", len(unzipped_src))

    reformatted_src = list(zip(unzipped_src[0], unzipped_src[1]))
    reformatted_dst = list(zip(unzipped_dst[0], unzipped_dst[1]))

    print("reformatted_src shape: ", reformatted_src[0], ", len: ", len(reformatted_src))

    src = np.array(reformatted_src)
    dst = np.array(reformatted_dst)

    print("srcshape: ", src.shape)
    
    h, status = cv2.findHomography(src, dst) # h = transformation matrix

    print("transformation matrix: ", h)

    im_dst = cv2.warpPerspective(img2, h, img2.shape[1::-1])
    thermal2_dst = cv2.warpPerspective(thermal2, h, img2.shape[1::-1])

    cv2.imshow("center", im_dst)
    cv2.waitKey(3000)
    cv2.imshow("center", thermal2_dst)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate Segmentation Masks.')
    parser.add_argument('-img1')
    parser.add_argument('-mask1')
    parser.add_argument('-img2')
    parser.add_argument('-mask2')
    parser.add_argument('-out')
    parser.add_argument('-thermal1')
    parser.add_argument('-thermal2')

    args = parser.parse_args()

    image_1_path = args.img1
    mask_1_path = args.mask1
    image_2_path = args.img2
    mask_2_path = args.mask2
    thermal_1_path = args.thermal1
    thermal_2_path = args.thermal2
    out = args.out

    print("Loading images from sources\n   (1)", image_1_path, "\n   (2)", mask_1_path, "\n   (3)", image_2_path, "\n   (4)", mask_2_path, "\n   (5)", thermal_1_path, "\n   (6)", thermal_2_path)
    print("Out folder: ", out)

    img1, mask1, thermal1, img2, mask2, thermal2 = loadImgs(image_1_path, mask_1_path, thermal_1_path, image_2_path, mask_2_path, thermal_2_path)
    img1, mask1, thermal1, img2, mask2, thermal2 = resizeImgs(img1, mask1, thermal1, img2, mask2, thermal2, out)
    assert img1.shape == mask1.shape
    assert img2.shape == mask2.shape
    assert thermal1.shape == img1.shape
    assert thermal2.shape == img2.shape

    center_m1 = compute_center(mask1, out + "m1_center.png")
    center_m2 = compute_center(mask2, out + "m2_center.png")

    x1 = (center_m1[0] + center_m2[0])//2
    x2 = (center_m1[1] + center_m2[1])//2
    center = (x1,x2)

    m1_edge_pts = compute_polar_line(mask1, center, out + "m1_edges.png")
    m2_edge_pts = compute_polar_line(mask2, center, out + "m2_edges.png")

    # visualize_pairs(img1, m1_edge_pts, img2, m2_edge_pts)

    # Now we have the centers, edges, and the lines that connect them. We simply have to "extend" the lines of pixels in one image to the other image.
    deform_image(img1, center, m1_edge_pts, m2_edge_pts, thermal1, out + "deformed_" + image_1_path.split('/')[-1], out + "thermal_deformed_" + thermal_1_path.split('/')[-1])
    cv2Deform(img1, center, m1_edge_pts, m2_edge_pts, thermal1, out + "deformed_" + image_1_path.split('/')[-1], out + "thermal_deformed_" + thermal_1_path.split('/')[-1])

    # Try this: https://open.win.ox.ac.uk/pages/fsl/fslpy/fsl.transform.nonlinear.html#fsl.transform.nonlinear.DeformationField.__init__
    # https://pypi.org/project/fslpy/
    # https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=a863ece2c1c96e2e89c8640bb071cd5b489ae867
    # https://mathlab.github.io/PyGeM/ffd.html
    # https://examples.itk.org/src/filtering/imagegrid/warpanimageusingadeformationfield/documentation
    
    # meshDeform(img1, center, m1_edge_pts, m2_edge_pts, thermal1, out + "deformed_" + image_1_path.split('/')[-1], out + "thermal_deformed_" + thermal_1_path.split('/')[-1])