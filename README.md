## Mission Statement and Product Description

Gym interest, and the lengths people are willing to go to get great results, are both rising. However, improving muscle activation is often overlooked, leading the people who are able to stay consistent to sub-optimal results, and unbalanced physiques. We offer a solution to this problem, with our thermal-camera phone application named "TAct" - which stands for thermal activation. It is a non-invasive application that uses thermal imaging to estimate muscle activation, backed by science and as a data-driven solution.

It also provides a unified interfact for tracking gym progress.

## Installation

This project is implemented in python 3.7 and torch 1.13.0. Follow these steps to setup your environment:

1. [Download and install Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html "Download and install Conda")
2. Create a Conda environment with Python 3.7
```
conda create -n hypertrophy python=3.7
```
3. Activate the Conda environment. You will need to activate the Conda environment in each terminal in which you want to use this code.
```
conda activate hypertrophy
```
4. Install the requirements:
```
pip3 install -r requirements.txt
```



## Dated Notes:

### 01/22/23

Currently working on matching the skin regions of two matching images of a body part. For example, let us assume that we have two pictures of the quadriceps muscles; in one the leg is slightly more extended than in the other one, making comparison and henceforth muscle group identification quite challenging. Therefore, the skin regions of the images must match. This step needs to be bulletproof as it is the basis of the entire project.

To match two corresponding image regions, the following structure was chosen:
1. Use Mask R-CNN to provide an initial "guess" for our object (may have to retrain with the option to specify part of the object in question)
 -- which would be easy enough to augment given the Mask R-CNN training dataset
2. Use OpenCV's implementation of GrabCut to refine our "guess"

We will still have to see and compare each individual and combined efforts to make a decision for production use.



### 01/23/23

Goal today is to use 1. and 2. references to implement the naive Mask R-CNN and GrabCut image segmentation method

## Next Steps:

1. Create a sample dataset of appendeges and muscle groups. Should be at least 50 images.
2. Test our model(s) on the sample dataset.
3. Decide how to improve model, if it is acceptable, and if so, move onto transforming the segmented images to match eachothers outline.
4. Check out 2D deformation image matching algorithms, however use matching edge points rather than features and descriptors.


## References:

1. https://pyimagesearch.com/2020/07/27/opencv-grabcut-foreground-segmentation-and-extraction/ 
2. https://pyimagesearch.com/2020/09/28/image-segmentation-with-mask-r-cnn-grabcut-and-opencv/ 
3. https://davis.wpi.edu/~matt/courses/morph/2d.htm 