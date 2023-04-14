## This folder contains files for end-to-end running of the project

To run, use the following bash file command:

`
./hypertrophy_insight.sh -f '../Media/Images/original_leg_day/' -i 'FLIR_20220906_104014_048-Visual.jpeg' -j 'FLIR_20220906_103225_633-Visual.jpeg' -t 'FLIR_20220906_104014_048.jpg' -u 'FLIR_20220906_103225_633.jpg' -o 'out/' -s 0
`
may need to add  
```
-m '../Test/LapPicVision/models/full_custom_dataset_p_0.25_25000.torch'
```

Note that -s 0 makes there be no cv2 imshow images. If this is set to 1, then images will be displayed directly from python script.

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


## Documentation of deformation technique

As found in previous experimentation, deforming the image via a polar expansion technique introduced artifacts. This was likely due to a non 1:1 transformation, as a result of deformation rays overlapping on a pixel granularity much more commonly than when r (radius) was low.

The deformation technique was implemented with the following pseudocode:
```
transform = skimage.transform.PiecewiseAffineTransform()
transform.estimate(source points, destination points)
out = skimage.transform.warp(image, transform)
```

The python library skimage was utilized. The basis is to use piecewise affine transformation - a transformation technique that instead of warping the entire image at once, first splits the image into a set of triangles, and then performs affine transformation to each region independently. As defined by the skimage documentation, "Control points are used to define the mapping. The transform is based on a Delaunay triangulation [implemented via scipy.spatial.Delaunay function] of the points to form a mesh. Each triangle is used to find a local affine transform." The source and destination points were computed using the polar search algorithm documented in ../Deformation_Matching.

Sources:
1. https://github.com/dfdx/PiecewiseAffineTransforms.jl
2. https://scikit-image.org/docs/stable/auto_examples/transform/plot_piecewise_affine.html
3. https://scikit-image.org/docs/stable/api/skimage.transform.html#skimage.transform.PiecewiseAffineTransform
4. 