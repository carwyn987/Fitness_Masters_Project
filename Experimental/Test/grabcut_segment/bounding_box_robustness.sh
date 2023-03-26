#! /bin/sh

# Define variables
OUTFILEPATH="Media/Computed_Media/image_segmentation/robustness_testing/"
FILENAMEOUT="image_"
FILEEXTENSION=".png"

# Initialize RANDOM
RANDOM=$(date +%s)

iter=0
while [ $iter -ne 10 ]
do
    random=$(od -vAn -N4 -t u4 < /dev/urandom);
    X=$((($random%100)  + 246 - 50 ))
    random=$(od -vAn -N4 -t u4 < /dev/urandom);
    Y=$((($random%100)  + 200 - 50 ))
    random=$(od -vAn -N4 -t u4 < /dev/urandom);
    W=$((($random%100)  + 700 - 50 ))
    random=$(od -vAn -N4 -t u4 < /dev/urandom);
    H=$((($random%100)  + 1330 - 50 ))

    python3 Test/grabcut_segment/image_segment.py --x $X --y $Y --w $W --h $H --folderout "$OUTFILEPATH$FILENAMEOUT$(($iter))$FILEEXTENSION"

    iter=$((iter+1))
    echo "$iter"
done