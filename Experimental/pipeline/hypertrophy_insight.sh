#!/bin/bash

while getopts f:i:j:t:u:o:m: flag
do
    case "${flag}" in
        f) folder=${OPTARG};;
        i) img1=${OPTARG};;
        j) img2=${OPTARG};;
        t) thermal1=${OPTARG};;
        u) thermal2=${OPTARG};;
        o) outfolder=${OPTARG};;
        m) model=${OPTARG};;
    esac
done

echo "Folder: $folder";
echo "Image 1: $img1";
echo "Image 2: $img2";
echo "Thermal Image 1: $thermal1";
echo "Thermal Image 2: $thermal2";
echo "Out Folder: $outfolder"

# Run images through model to get segmented view
python3 segment.py -folder "$folder" -image "$img1" -outfolder "$outfolder" -model "$model"
python3 segment.py -folder "$folder" -image "$img2" -outfolder "$outfolder" -model "$model"

# Model example: "../Test/LapPicVision/models/custom_dataset_p_0.25_25000.torch"

# Set mask variables
mask1="${outfolder}Mask_$img1"
mask2="${outfolder}Mask_$img2"

echo "Mask 1: $mask1"
echo "Mask 2: $mask2"

# Now that we have segmented images, run deformation script to edge find, and scale.
python3 deform.py -img1 "$folder$img1" -mask1 "$mask1" -img2 "$folder$img2" -mask2 "$mask2" -out "$outfolder" -thermal1 "$folder$thermal1" -thermal2 "$folder$thermal2"

# Need to improve the algorithm and mask training. It introduces artifacts to the thermal image, especially when masking is incomplete.
# Perhaps adding a gaussian blur would help, although it would reduce information.
# Finally, I need to introduce a thermal difference script to provide insights.

python3 difference.py -thermal1 "${outfolder}thermal_deformed_${thermal1}" -thermal2 "${outfolder}thermal2.png" -out "$outfolder"