# Run via "python -m Test.mask_rcnn.mask_rcnn" from base directory


import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt

# Root directory of the project
ROOT_DIR = os.path.abspath("Mask_RCNN/")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from Mask_RCNN.mrcnn import utils
from Mask_RCNN.mrcnn import model as modellib
from Mask_RCNN.mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
from pycocotools import mask as mask
from pycocotools import coco as coco