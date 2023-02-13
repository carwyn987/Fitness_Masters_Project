# Hypertrophy Tool - Using Thermal Imagery as a Metric for Muscle Activation and Hypertrophy

## Mission Statement and Product Description

Gym interest, and the lengths people are willing to go to get great results, are both rising. However, improving muscle activation is often overlooked, leading the people who are able to stay consistent to sub-optimal results, and unbalanced physiques. We offer a solution to this problem, with our thermal-camera phone application named "TAct" - which stands for thermal activation. It is a non-invasive application that uses thermal imaging to estimate muscle activation, backed by science and as a data-driven solution.

It also provides a unified interfact for tracking gym progress.


## Current High Level Overview Details

![UML-like high-level overview](Media/UML/Hypertrophy.svg?raw=true "Planning Page")

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
5. Install ipykernel for running ipynb files
conda install -n hypertrophy ipykernel --update-deps --force-reinstall

6. For Mask R-CNN:

pip install Cython
pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI
pip install pycocotools

pip uninstall keras -y
pip uninstall keras-nightly -y
pip uninstall keras-Preprocessing -y
pip uninstall keras-vis -y
pip uninstall tensorflow -y
pip uninstall h5py -y

pip install tensorflow==1.13.1
pip install keras==2.0.8
pip install h5py==2.10.0

pip3 install imgaug
sudo apt-get install python3-tk

## Commands to Run:

$ python -m Test.mask_rcnn.mask_rcnn
$ python3 Mask_RCNN/samples/coco/coco.py train --dataset=Mask_RCNN/samples/coco --model=Mask_RCNN/samples/coco/mask_rcnn_coco.h5

## Dated Notes:

### 01/22/23

Currently working on matching the skin regions of two matching images of a body part. For example, let us assume that we have two pictures of the quadriceps muscles; in one the leg is slightly more extended than in the other one, making comparison and henceforth muscle group identification quite challenging. Therefore, the skin regions of the images must match. This step needs to be bulletproof as it is the basis of the entire project.

To match two corresponding image regions, the following structure was chosen:
1. Use Mask R-CNN to provide an initial "guess" for our object (may have to retrain with the option to specify part of the object in question)
 -- which would be easy enough to augment given the Mask R-CNN training dataset
2. Use OpenCV's implementation of GrabCut to refine our "guess"

We will still have to see and compare each individual and combined efforts to make a decision for production use.

### 01/23/23

Goal today is to use 1. and 2. references to implement the naive Mask R-CNN and GrabCut image segmentation method.
Completed the GrabCut implementation. Performance seems solid and relatively accurate but blocky outline.
Goal for tomorrow is to test robustness.

### 01/24/23

Testing robustness via a shell script and .py file to use GrabCut on a static image, but varying the bounding box initialization. They all capture the leg quite well, but the borders shift and move around significantly enough to where it is not good enough for this project.
The next step is to see if I can improve the edge precision with R-CNN.

### 01/27/23 - 01/28/23

Setting up environemnt, pulling in submodule, and testing R-CNN on our unique dataset.
I have successfully set up the testing environment. I still need to download original RCNN training set if I wish to train RCNN from scratch.

### 01/29/23

Tested RCNN upon images of a leg. Unfortunately, it was trained to identify objects that are seen in a standard environment from the human perspective, such as chairs, people, etc, but not anatomy of humans. Therefore, my plan for next steps is to create a small leg and arm dataset, labelled and masked. Then I will apply transformations such as jitter, rotation, scaling, lighting, dimming, etc. and train Mask RCNN (with frozen layers except last layer) upon this dataset. Hopefully this will resolve this issue. Then I will test mixing GrabCut and Mask RCNN to get a final accurate estimate.

### 02/01/23

Today I will set up the training of RCNN. Currently, not only are the directory submodule paths inaccurate, but I do not have the correct datasets.
When running inspect_data.ipynb, it is clear that not all the annotations for the training set line up to the coco images. Therefore, the code is erroring - note that I am running it with the 2014 dataset. Todo: Implement filtering for annotations such that at least one image matches.

### 02/02/23

Did research into simpler image segmentation algorithms, found tf image segmentation package, and tested. Unfortunately, (1) the LabPic dataset is incomplete and (2) not representative of my dataset. Therefore, I am going to build a tool for segmenting images and creating a dataset efficiently, train the model on my own dataset, and use this as a main finding of my research project. Also, I have been exploring EDA on the file input types. 

### 02/07/23

Have been collecting a dataset. Parameters for the dataset include having a variety of images, angles, backgrounds, clothing apparel, shadows, and anatomical positions. I plan to augment the dataset after applying a mask, by rotation, and zoom. Perhaps I will also request a black or asian friend to assist me in getting more data to accomodate more diverse customers. The next step is to complete the masking code. The project results may turn into an interactive tool for preparing, and labeling a mask segmentation dataset.

### 02/10/23

After a few days off for interviews, I am back to the project. Using this source https://towardsdatascience.com/generating-image-segmentation-masks-the-easy-way-dd4d3656dbd1 I am creating a masked image dataset via "VIA" (VGG Image Annotator) and then trying a few options. (1) adding the dataset to the current dataset, (2) fine tuning the model by resetting (final layer) or freezing previous layers, (3) training a whole new model on this smaller dataset (overfitting issues?). The current network architecture was taken from torchvision models segmentation.

### 02/11/23+

I have decided that dating notes about my progress is insignificant, as it simply abstracts the existing functionality out of commit logs. Futher notes can simply be understood by checking the git commit history.

## Next Steps:

1. Create a sample dataset of appendeges and muscle groups. Should be at least 50 images.
2. Test our model(s) on the sample dataset.
3. Decide how to improve model, if it is acceptable, and if so, move onto transforming the segmented images to match eachothers outline.
4. Check out 2D deformation image matching algorithms, however use matching edge points rather than features and descriptors.

## References:

1. https://pyimagesearch.com/2020/07/27/opencv-grabcut-foreground-segmentation-and-extraction/ 
2. https://pyimagesearch.com/2020/09/28/image-segmentation-with-mask-r-cnn-grabcut-and-opencv/ 
3. https://davis.wpi.edu/~matt/courses/morph/2d.htm 
4. https://github.com/MengyangPu/RINDNet 
5. https://github.com/matterport/Mask_RCNN 
