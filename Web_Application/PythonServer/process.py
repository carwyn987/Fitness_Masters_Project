import numpy as np
import subprocess
import os
import cv2
import glob

def processMain(img1, img2, t_img1, t_img2):

    save_dir = "temp_media/"
    i1 = "i1" + ".jpg"
    i2 = "i2" + ".jpg"
    t1 = "t1" + ".jpg"
    t2 = "t2" + ".jpg"
    
    # Save images to current dir
    cv2.imwrite(save_dir + i1, img1)
    cv2.imwrite(save_dir + i2, img2)
    cv2.imwrite(save_dir + t1, t_img1)
    cv2.imwrite(save_dir + t2, t_img2)

    # Change directory to experimental
    relative_pth = '../../Experimental/pipeline/'
    undo_pth = '../../Web_Application/PythonServer/'
    os.chdir(relative_pth)

    # Using the correct conda environment, run the script to process images, and create output image.
    run_cmd = f"./hypertrophy_insight.sh -f {undo_pth + save_dir} -i {i1} -j {i2} -t {t1} -u {t2} -o {undo_pth + save_dir} -m '../Test/LapPicVision/models/full_custom_dataset_p_0.25_25000.torch' -s 0"
    cmd = f'. /home/carwyn/anaconda3/etc/profile.d/conda.sh && conda activate hypertrophy && conda list && {run_cmd}' 
    subprocess.run(cmd, shell=True, executable='/bin/bash')

    # Get the image back
    img = cv2.imread("out/output.png")

    # Make stateless by deleting temp_media folder contents
    files = glob.glob(undo_pth + save_dir + "*")
    for f in files:
        os.remove(f)

    return img