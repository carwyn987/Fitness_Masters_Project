# Custom segmentation network

This folder contains self-written code for segmenting images using a CNN and PyTorch.

## Instructions to run

$ python3 train.py

## Info:
 - Swapped out the classification step (softmax) and crossentropyloss for an l1loss (no classification, just regressing the image segmentation)
 - Increased learning rate from 0.005 to 0.025
 - TODO: create a file for graphing and abstract out the matplotlib and image saving.


Observations:
1. After loading my custom curated dataset of 69 images and masks, 30 percent of main memory is filled. Therefore, to keep the training speeds higher, a maximum of about 200 observations (images and labels) will keep the program from using swap.

## Approaches for image segmentation that I wish to attempt
1. U-Net or V-Net
2. Encoder-Decoder based models
3. Fully convolutional network

# Sources
 - I am using SegNet as a baseline model to ensure the rest of the code is correct before implementing my own models.
 - The resources for that come from https://github.com/vinceecws/SegNet_PyTorch and https://arxiv.org/pdf/1511.00561.pdf 