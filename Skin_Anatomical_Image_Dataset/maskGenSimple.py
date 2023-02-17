# Sourced from https://towardsdatascience.com/generating-image-segmentation-masks-the-easy-way-dd4d3656dbd1

import os
import cv2
import json
import numpy as np 

source_folder = os.path.join(os.getcwd(), "original_images_concat")
to_base_folder = os.getcwd()

# MODIFY THESE PATHS!
json_path = "via_custom_annotations_image_sets_1_2_3/anatomy_set2_json.json" # Relative to root directory
out = "simple_image_config2"


count = 0                                           # Count of total images saved
file_bbs = {}                                       # Dictionary containing polygon coordinates for mask
MASK_WIDTH = 256				    # Dimensions should match those of ground truth image
MASK_HEIGHT = 256									

# Read JSON file
with open(json_path) as f:
  data = json.load(f)

# Extract X and Y coordinates if available and update dictionary
def add_to_dict(data, itr, key, count):
    try:
        x_points = data[itr]["regions"][count]["shape_attributes"]["all_points_x"]
        y_points = data[itr]["regions"][count]["shape_attributes"]["all_points_y"]
    except:
        print("No BB. Skipping", key)
        return
    
    all_points = []
    for i, x in enumerate(x_points):
        all_points.append([x, y_points[i]])
    
    file_bbs[key] = all_points
  
for itr in data:
    file_name_json = data[itr]["filename"]
    sub_count = 0               # Contains count of masks for a single ground truth image
    
    if len(data[itr]["regions"]) > 1:
        for _ in range(len(data[itr]["regions"])):
            key = file_name_json[:-4] + "*" + str(sub_count+1)
            add_to_dict(data, itr, key, sub_count)
            sub_count += 1
    else:
        add_to_dict(data, itr, file_name_json[:-4], 0)

			
print("\nDict size: ", len(file_bbs))

# Make new simple images folder
new_dir = os.path.join(to_base_folder, out)
image_folder = os.path.join(new_dir, "images")
mask_folder = os.path.join(new_dir, "masks")

os.mkdir(new_dir)
os.mkdir(image_folder)
os.mkdir(mask_folder)

for file_name in os.listdir(source_folder):
    curr_img = os.path.join(source_folder, file_name)
    # os.rename(curr_img, os.path.join(image_folder, file_name))
    os.system('cp ' + curr_img + ' ' + os.path.join(image_folder, file_name))
        
# For each entry in dictionary, generate mask and save in correponding 
# folder
for itr in file_bbs:
    # print("itr: ", itr)
    num_masks = itr.split("*")
    to_save_folder = os.path.join(source_folder, num_masks[0])

    # Set image dimensions
    # print("SRC: ", to_save_folder)
    print(os.path.join(to_save_folder + ".jpg"))
    img = cv2.imread(os.path.join(to_save_folder + ".jpg"))
    if img is None:
        print("Image failed to load. Attempting .jpeg extension...")
        img = cv2.imread(os.path.join(to_save_folder + "jpeg"))
    MASK_WIDTH, MASK_HEIGHT, channels = img.shape
    print(MASK_HEIGHT, MASK_WIDTH, channels)


    mask = np.zeros((MASK_WIDTH, MASK_HEIGHT))
    try:
        arr = np.array(file_bbs[itr])
        print(np.count_nonzero(arr))
    except:
        print("Not found:", itr)
        continue
    count += 1
    cv2.fillPoly(mask, [arr], color=(255))
    # if count < 10:
    #     cv2.imshow('image',mask)
    #     cv2.waitKey(0)

    # print("Saving: ", itr)
    if itr[-1] == ".":
        itr = itr[0:len(itr)-1]
    # print("Saving2: ", itr)
    
    if len(num_masks) > 1:
        cv2.imwrite(os.path.join(mask_folder, itr.replace("*", "_") + ".png") , mask)    
    else:
        cv2.imwrite(os.path.join(mask_folder, itr + ".png") , mask)
        
print("Images saved:", count)