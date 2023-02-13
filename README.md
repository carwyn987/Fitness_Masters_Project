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

## References for Project Construction:

1. https://pyimagesearch.com/2020/07/27/opencv-grabcut-foreground-segmentation-and-extraction/ 
2. https://pyimagesearch.com/2020/09/28/image-segmentation-with-mask-r-cnn-grabcut-and-opencv/ 
3. https://davis.wpi.edu/~matt/courses/morph/2d.htm 
4. https://github.com/MengyangPu/RINDNet 
5. https://github.com/matterport/Mask_RCNN 

## Background References:

1. Saltin, B. J. A. J., Gagge, A. P., & Stolwijk, J. A. (1968). Muscle temperature during submaximal exercise in man. Journal of applied physiology, 25(6), 679-688.
 > The authors Bengt Saltin et al. performed research on the topic of muscle temperature during submaximal exercise at the John B. Pierce Laboratory which specializes in studying physiology and health in the modern environment. The researchers had subjects perform steady state cardio on a stationary cycling machine. While exercising, they measured core temperature, average skin temperature over the entire body using IR, and intramuscular temperature of the legs. The findings were that in submaximal steady state exercise, skin temperature behaved inverse to that of the muscle temperature measurements with the thermocouples. As ambient temperature increased however, the relationship did not hold, and the skin temperature was concave before plateauing above the initial skin temperature. Another interesting finding was that the difference between the temperature at differing depths of thermocouple-needle measurements diminished as workload increased. Note that the muscles were measured to vary three degrees celsius from baseline to the converged muscle temperature.

2. Priego Quesada, J. I., Carpes, F. P., Bini, R. R., Salvador Palmer, R., Pérez-Soriano, P., & Cibrián Ortiz de Anda, R. M. (2015). Relationship between skin temperature and muscle activation during incremental cycle exercise. Journal of Thermal Biology, 48, 28–35. https://doi.org/10.1016/j.jtherbio.2014.12.005
 > A group of researchers primarily based in Valencia, Spain studied the effects on skin temperature by cycling exercise, primarily muscles in the quadriceps. The study found that (1) the localized area of skin over an exercised muscle had a statistically significant increase in temperature, (2) overall activation of the vastus lateralis was inversely related with skin temperature, and (3) low frequency activation of the vastus lateralis had a strong positive correlation with skin temperature. An interesting conclusion was that “Participants with larger overall activation and reduced low frequency component for vastus lateralis activation presented a better adaptive response of their thermoregulatory system by showing fewer changes in skin temperature after incremental cycling test”.

3. Oliveira, U. F. de, Araújo, L. C. de, Andrade, P. R. de, Santos, H. H. dos, Moreira, D. G., Sillero-Quintana, M., & Almeida Ferreira, J. J. de. (2018). Skin temperature changes during muscular static stretching exercise. Journal of Exercise Rehabilitation, 14(3), 451–459. https://doi.org/10.12965/jer.1836056.028
 > Researchers at the Federal University of Paraíba measured the skin temperatures of subjects over 180 seconds of hamstring stretching using a thermographic camera. There was a statistically significant increase in temperature of about 0.3°C, with changes in temperature during this time being linear. An unrelated observation is that the stress or work done on a muscle may be correlated to the temperature-skin area, rather than any single point of maximal temperature.


4. Priego-Quesada, J. I., De la Fuente, C., Kunzler, M. R., Perez-Soriano, P., Hervás-Marín, D., & Carpes, F. P. (2020). Relationship between Skin Temperature, Electrical Manifestations of Muscle Fatigue, and Exercise-Induced Delayed Onset Muscle Soreness for Dynamic Contractions: A Preliminary Study. International Journal of Environmental Research and Public Health, 17(18), 6817. https://doi.org/10.3390/ijerph17186817 
 > With the knowledge that “during muscle contractions, most of the energy generated is heat (>70%) that is transferred to the skin by conduction between tissues or by convection through capillary blood flow”, researchers performed a correlation analysis between skin temperature during exercise - specifically single arm bicep curls to failure (the other arm acted as a control group) - and muscle fatigue post-workout - 24 hours later. The researchers used a FLIR camera with resolution 320 x 240 after calibration. Delayed Onset Muscle Fatigue (DOMS) was found not to be correlated with skin temperature, or any other quantity measured. The more sets that were performed, the less correlation between skin temperature and repetition existed. Furthermore, the temperature did not continue to rise. Increases were only measured in the first two sets in a declining manner. The third set actually had a decrease in skin temperature recorded. The researchers surmised that this trend may have been caused by sweating, and that the three minute rest period may have caused the trend to exacerbate. This study is relevant to my research project as they use similar equipment, and indicate that more data is required to determine DOMS. The researchers concluded that “Although we considered in our study that the presence of sweat was negligible, it may have affected the temperature responses of the skin during the exercise.”
Read the related works of this paper as it correlates highly with research topic.

5. da Silva, W., Machado, Á. S., Souza, M. A., Kunzler, M. R., Priego-Quesada, J. I., & Carpes, F. P. (2018). Can exercise-induced muscle damage be related to changes in skin temperature? Physiological Measurement, 39(10), 104007. https://doi.org/10.1088/1361-6579/aae6df
 > Researchers again used a FLIR camera system with resolution 320 x 240 pixels, and this time tested the hypothesis that there is a correlation between creatine kinase (CK) activity. CK activity “ is widely employed to estimate the magnitude of exercise-induced muscle damage in sports”. The researchers “found that CK and infrared thermography responses to exercise-induced muscle damage are different. At least for exercise of a specific muscle group in untrained participants, skin temperature did not correlate with the creatine kinase activity. Therefore, the use of infrared thermography to predict or monitor muscle damage deserves further attention”. Note that the exercise-induced muscle damage (EIMD) is not necessarily correlated with muscle hypertrophy. While highly cited on the matter, many believe it is possible to grow muscle without such painful indications.


Summary of background information

 - Steady state exercise is inversely related to muscle temperature.
 - Muscle temperature varied three degrees celsius over steady state exercise.
 - The localized skin over an exercised muscle had a significant increase in temperature
 - Low frequency activation of the muscle has a strong positive correlation with skin temperature. However, overall activation has an inverse trend.
 - Stretching has a minimal (0.3๐C) increase in muscle temperature.
 - Stress or work done on a muscle may be correlated to the temperature-skin area, rather than any single point of maximal temperature.
 - DOMS does not correlate with skin temperature.
 - Skin temperature may even decrease with work as sweat impacts readings.
 - Measuring muscle damage via CK has no measurable correlation with skin temperature.