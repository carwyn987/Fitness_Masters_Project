The purpose of this directory is two-fold
1. Compute an estimate of a contiguous line surrounding the mask
2. Transform between two images with such estimated lines

Sample execution commands:

`
python3 polar_line_estimation.py "sample_images/PXL_20230208_042455615.jpg" "sample_images/PXL_20230208_042455615_mask.jpg" "sample_images/PXL_20230208_042446197.jpg" "sample_images/PXL_20230208_042446197_mask.jpg"
`