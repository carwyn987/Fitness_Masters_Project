import torch
import argparse
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import numpy as np
import time
import cv2
import matplotlib.pyplot as plt

from src.load import load_and_split
from src.model import SegmentAE, SegmentUNet
from src.SegNet import SegNet, load_model_json

def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Train a segmentation CNN model.')
    # parser.add_argument('--sum', type=int, default=0, help='train')
    parser.add_argument('--model', type=str, default='AE', choices=['AE', 'UNet', 'SegNet'])
    args = parser.parse_args()

    # Load Data

    data_folder = '../Skin_Anatomical_Image_Dataset/simple_image_config'
    train, validation, test = load_and_split(data_folder)
    
    # Create model

    if args.model == 'AE':
        model = SegmentAE()
    elif args.model == 'UNet':
        model = SegmentUNet()
    elif args.model == 'SegNet':
        model_json = load_model_json()
        model = SegNet(in_chn=model_json['in_chn'], out_chn=model_json['out_chn'], BN_momentum=model_json['bn_momentum'])
        train_model(model, train[0], train[1], test[0], test[1], model_json)

def train_model(model, train_data, train_labels, test_data, test_labels, model_json=None):

    epochs = 100
    
    optimizer = optim.SGD(model.parameters(), lr=model_json['learning_rate'], momentum=model_json['sgd_momentum'])
    # loss_fn = nn.CrossEntropyLoss(weight=torch.tensor(model_json['cross_entropy_loss_weights']))
    loss_fn = nn.L1Loss()
    loss_save = []
    test_loss_save = []
    loss = None

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device) # cuda()
    loss_fn.to(device) # cuda()

    # Training Loop
    for e in tqdm(range(epochs)):
        
        # Because training samples don't fit in memory, do each one individually
        for i in range(train_data.shape[0]):            
            d = torch.tensor(np.expand_dims(train_data[i], axis=0)).float().to(device)
            optimizer.zero_grad()
            predict = model(d)

            loss = loss_fn(predict, torch.tensor(np.expand_dims(np.expand_dims(train_labels[i][0,:,:], axis=0), axis=0)).float().to(device))
            loss_save.append(loss.item())
            loss.backward()
            optimizer.step()

            # Memory Optimization
            # del d, predict
            # torch.cuda.empty_cache()
        
        if e % 10 == 0:
            loss_save.append(loss.item())

            # Perform test or validation loss:
            model.eval()
            with torch.no_grad():
                average_loss = 0
                for i in range(test_data.shape[0]):
                    d = torch.tensor(np.expand_dims(train_data[i], axis=0)).float().to(device)
                    predict = model(d)
                    loss = loss_fn(predict, torch.tensor(np.expand_dims(np.expand_dims(train_labels[i][0,:,:], axis=0), axis=0)).float().to(device))
                    average_loss += loss.item()
                test_loss_save.append(average_loss/test_data.shape[0])
            model.train()


    fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    ax.plot(np.arange(len(loss_save)), loss_save)
    fig.suptitle('Training Loss vs Iteration Curve', fontsize='large')
    ax.set_xlabel('Training Iteration (Not Epoch)', fontsize='medium')
    ax.set_ylabel('Training Loss', fontsize='medium')
    fig.savefig(f'media/training_vs_{epochs}_image_iterations.png')   # save the figure to file

    fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    ax.plot(np.arange(len(test_loss_save)), test_loss_save)
    fig.suptitle('Testing Loss vs Iteration Curve', fontsize='large')
    ax.set_xlabel('v Iteration (Not Epoch)', fontsize='medium')
    ax.set_ylabel('Testing Loss', fontsize='medium')
    fig.savefig(f'media/testing_vs_{epochs}_image_iterations.png')   # save the figure to file

if __name__ == "__main__":
    main()