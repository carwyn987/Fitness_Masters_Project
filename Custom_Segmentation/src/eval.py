import os
import torch
import numpy as np

from src.plot import save_prediction

'''
Given a single input image path, and a model .pth file, predict the mask and show in opencv (and save)

Note that test_data is given in the form: (image_np_array, label_np_array)
'''

def eval_sample(model, test_data, device, folder_to_create, sample_size=10):
    
    # Extract a sample of test data images:
    
    img_indeces = np.random.choice(test_data[0].shape[0], sample_size)
    imgs = [test_data[0][i, :, :] for i in img_indeces]

    # Make predictions

    model.eval()
    segmented_imgs = [np.squeeze(model(torch.tensor(np.expand_dims(img, axis=0)).float().to(device)).detach().cpu().numpy()) for img in imgs]
    model.train()

    # for i in range(len(segmented_imgs)):
    #     segmented_imgs[i][segmented_imgs[i]>=0.1] = 1
    #     segmented_imgs[i][segmented_imgs[i]<0.1] = 0
    
    # Make output directory

    folder_to_create = "media/" + folder_to_create
    if not os.path.exists(folder_to_create):
        os.makedirs(folder_to_create)

    # Save images

    for i in range(len(imgs)):
        save_prediction(imgs[i].transpose(1,2,0), segmented_imgs[i], folder_to_create + "image_" + str(i) + ".png")