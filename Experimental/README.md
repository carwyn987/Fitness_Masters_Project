# Experimental Directory

This directory is responsible for containing files regarding the experimentation and construction of algorithms to further the projects mission statement.

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
```
conda install -n hypertrophy ipykernel --update-deps --force-reinstall
```

6. For Mask R-CNN (Not Required):

```
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

```

## Commands to Run:

```
$ python -m Experimental.Test.mask_rcnn.mask_rcnn
$ python3 Experimental/Mask_RCNN/samples/coco/coco.py train --dataset=Mask_RCNN/samples/coco --model=Mask_RCNN/samples/coco/mask_rcnn_coco.h5
```