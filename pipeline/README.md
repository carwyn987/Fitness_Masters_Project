## This folder contains files for end-to-end running of the project

To run, use the following bash file command:

`
./hypertrophy_insight.sh -f '../Media/Images/original_leg_day/' -i 'FLIR_20220906_104014_048-Visual.jpeg' -j 'FLIR_20220906_103225_633-Visual.jpeg' -t 'FLIR_20220906_104014_048.jpg' -u 'FLIR_20220906_103225_633.jpg' -o 'out/'
`

Keep in mind that img1 and thermal1 (i.e. -i and -t) should reference the after images in the set of {before, after, beforethermal, afterthermal}.

Entire pipline directions

0. Enter the 'Skin_Anatomical_Image_Dataset/' directory.
1. Open VIA tool. The html file is stored in 'Skin_Anatomical_Image_Dataset/via_install'.
2. Load in previous masks if desired. Add any images that are to be trained. Mask images manually. Save project.
3. Make sure the images in the via project are stored in 'Skin_Anatomical_Image_Dataset/original_images_concat/'.
4. Modify paths in 'Skin_Anatomical_Image_Dataset/maskGenSimple.py' to match the annotation file and image files.
5. Activate hypertrophy conda environment
6. Run 'Skin_Anatomical_Image_Dataset/maskGenSimple.py'
7. At this point, the dataset is completely setup. Time to train a segmentation model.
8. Move to the 'Test/LapPicVision/' directory.
9. Open 'model_segmnetation.ipynb'.
10. Modify 'secondTrainFolder', 'full_path_images', and 'full_path_masks' paths to reflect image dataset updates. Modify any other desired parameters.
11. Make sure to modify the model save file in last line of training loop.
12. Run all blocks of model_segmentation.ipynb, and by doing so, train a new model.
13. Move to pipeline folder. Run hypertrophy pipeline with a command such as the following.
 - ./hypertrophy_insight.sh -f '../Media/Images/original_leg_day/' -i 'FLIR_20220906_104014_048-Visual.jpeg' -j 'FLIR_20220906_103225_633-Visual.jpeg' -t 'FLIR_20220906_104014_048.jpg' -u 'FLIR_20220906_103225_633.jpg' -o 'out/' -m '../Test/LapPicVision/models/full_custom_dataset_p_0.25_25000.torch'
14. The output image "out/output.png" shows insights made by the pipeline.