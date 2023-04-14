import cv2
import torch
import argparse
import numpy as np
import torchvision.models.segmentation
import torchvision.transforms as tf
import matplotlib.pyplot as plt

def setup(imagePath, modelPath, outfolder, imageName, show):
    height=width=900
    transformImg = tf.Compose([tf.ToPILImage(), tf.Resize((height, width)), tf.ToTensor(),tf.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))])

    img = cv2.imread(imagePath) # load test image
    imheight , imwidth ,d = img.shape # Get image original size 

    if show:
        plt.imshow(img[:,:,::-1])  # Show image
        plt.show(block=False)
        plt.pause(0.5)
        plt.close()

    cv2.imwrite(outfolder + imageName, img)

    return transformImg, imheight, imwidth, img

def predict(transformImg, modelPath, img):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')  # Check if there is GPU if not set trainning to CPU (very slow)
    Net = torchvision.models.segmentation.deeplabv3_resnet50(pretrained=True)  # Load net
    Net.classifier[4] = torch.nn.Conv2d(256, 3, kernel_size=(1, 1), stride=(1, 1))  # Change final layer to 3 classes
    Net = Net.to(device)  # Set net to GPU or CPU
    Net.load_state_dict(torch.load(modelPath)) # Load trained model
    Net.eval() # Set to evaluation mode
    
    img = transformImg(img)  # Transform to pytorch
    img = torch.autograd.Variable(img, requires_grad=False).to(device).unsqueeze(0)
    with torch.no_grad():
        Prd = Net(img)['out']  # Run net
    
    return Prd

def Save(imageName, outfolder, height_orgin, widh_orgin, prd, show):
    prd = tf.Resize((height_orgin,widh_orgin))(prd[0]) # Resize to origninal size
    seg = torch.argmax(prd, 0).cpu().detach().numpy()  # Get  prediction classes

    # print(seg.shape)
    # print(seg.min(), seg.max())
    seg[seg == 1] = 255
    seg = seg[..., np.newaxis]
    seg = np.concatenate((seg, seg, seg),2)

    if show:

        plt.imshow(seg)  # display image
        plt.show(block=False)
        plt.pause(0.5)

        # plt.savefig(outfolder + "Mask_" + imageName)
        plt.close()
    
    print("WRITING TO ", outfolder + "Mask_" + imageName)
    cv2.imwrite(outfolder + "Mask_" + imageName, seg)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Segmentation Masks.')
    parser.add_argument('-folder')
    parser.add_argument('-image')
    parser.add_argument('-outfolder')
    parser.add_argument('-model')
    parser.add_argument('-show')

    args = parser.parse_args()
    args.show = int(args.show)
    print(args.folder, args.image, args.outfolder, args.model, args.show)

    # Setup transform
    transformImg, imheight, imwidth, img = setup(args.folder + args.image, args.model, args.outfolder, args.image, args.show)

    # Predict
    prd = predict(transformImg, args.model, img)

    # Predict and save
    Save(args.image, args.outfolder, imheight, imwidth, prd, args.show)