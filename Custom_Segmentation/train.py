import torch
import argparse
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import numpy as np

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
        train_model(model, train[0], train[1], model_json)

def train_model(model, train_data, train_labels, model_json=None):

    epochs = 10
    
    optimizer = optim.SGD(model.parameters(), lr=model_json['learning_rate'], momentum=model_json['sgd_momentum'])
    loss_fn = nn.CrossEntropyLoss(weight=torch.tensor(model_json['cross_entropy_loss_weights']))
    loss_save = []

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device) # cuda()
    loss_fn.to(device) # cuda()

    # Training Loop
    for e in tqdm(range(epochs)):
        # Because training samples don't fit in memory, do each one individually
        for i in range(train_data.shape[0]):

            # t = torch.cuda.get_device_properties(0).total_memory
            r = torch.cuda.memory_reserved(0)
            a = torch.cuda.memory_allocated(0)
            f = r-a  # free inside reserved
            print("1Free inside reserved: ", f, a)

            
            d = torch.tensor(np.expand_dims(train_data[i], axis=0)).float().to(device)
            
            r = torch.cuda.memory_reserved(0)
            a = torch.cuda.memory_allocated(0)
            f = r-a  # free inside reserved
            print("2Free inside reserved: ", f, a)


            # optimizer.zero_grad()
            predict = model(d)
            # loss = loss_fn(predict)
            # loss.backward()
            # optimizer.step()
            del d, predict
            torch.cuda.empty_cache()

            r = torch.cuda.memory_reserved(0)
            a = torch.cuda.memory_allocated(0)
            f = r-a  # free inside reserved
            print("3Free inside reserved: ", f, a)
        
        if e % 10:
            loss_save.append(0)

if __name__ == "__main__":
    main()