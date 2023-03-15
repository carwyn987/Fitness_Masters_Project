# Custom segmentation network

This folder contains self-written code for segmenting images using a CNN and PyTorch.

# Instructions to run

$ python3 train.py


Observations:
1. After loading my custom curated dataset of 69 images and masks, 30 percent of main memory is filled. Therefore, to keep the training speeds higher, a maximum of about 200 observations (images and labels) will keep the program from using swap.