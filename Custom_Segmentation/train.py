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
from src.plot import plot_loss
from src.eval import eval_sample

def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Train a segmentation CNN model.')
    # parser.add_argument('--sum', type=int, default=0, help='train')
    parser.add_argument('--model', type=str, default='AE', choices=['AE', 'UNet', 'SegNet'])
    args = parser.parse_args()

    # Load Data

    data_folder = '../Skin_Anatomical_Image_Dataset/simple_image_config'
    train, validation, test = load_and_split(data_folder)
    
    # Create model + parameters

    epochs = 500
    train_losses = []
    test_losses = []
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    if args.model == 'AE':
        model = SegmentAE()
        model_json = load_model_json()
        train_losses, test_losses = train_model(model, train[0], train[1], test[0], test[1], epochs, device, model_json)
    elif args.model == 'UNet':
        model = SegmentUNet()
    elif args.model == 'SegNet':
        model_json = load_model_json()
        model = SegNet(in_chn=model_json['in_chn'], out_chn=model_json['out_chn'], BN_momentum=model_json['bn_momentum'])
        train_losses, test_losses = train_model(model, train[0], train[1], test[0], test[1], epochs, device, model_json)

    # Evaluate model
    plot_loss(train_losses, 'Training Loss vs Iteration Curve', 'Training Iteration (Not Epoch)', 'Training Loss', filename=f'media/training_vs_{epochs}_image_iterations_{args.model}.png')
    plot_loss(test_losses, 'Testing Loss vs Iteration Curve', 'Iteration (Not Epoch)', 'Testing Loss', filename=f'media/testing_vs_{len(test_losses)}_image_iterations_{args.model}.png')

    eval_sample(model, test, device, folder_to_create=f"sample_test_predictions_{args.model}/")

def train_model(model, train_data, train_labels, test_data, test_labels, epochs, device, model_json=None):
    
    optimizer = optim.SGD(model.parameters(), lr=model_json['learning_rate'], momentum=model_json['sgd_momentum'])
    # loss_fn = nn.CrossEntropyLoss(weight=torch.tensor(model_json['cross_entropy_loss_weights']))
    loss_fn = nn.L1Loss()
    loss_save = []
    test_loss_save = []
    loss = None

    model.to(device) # cuda()
    loss_fn.to(device) # cuda()

    # Training Loop
    for _ in tqdm(range(epochs)):
        
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

    return loss_save, test_loss_save

if __name__ == "__main__":
    main()