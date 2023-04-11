import numpy as np

def processMain(img1, img2, t_img1, t_img2):

    # Blur image
    kernel = np.ones((10,10),np.float32)/100
    img = (img1[0:400, 0:400, :] + img2[0:400, 0:400, :])/2 # cv2.filter2D(img,-1,kernel) # blur image

    return img