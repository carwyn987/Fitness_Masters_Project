import torch
import torch.nn as nn
import torch.nn.functional as F

class SegmentAE(torch.nn.Module):
    def __init__(self):
        super().__init__()

        '''
        This model is a very small convolutional autoencoder for image segmentation.
        
        Goal: use the minimum operations (conv, pool, batchnorm) and benchmark loss

        Network structure:

        Input:
        (1, 3, 94, 126)
        Conv2d(out_channels=16, stride=2, padding=2, dilation=1)
        (1, 16, 48, 64)
        Max Pooling(2, stride=2)
        (1, 16, 24, 32)
        MaxUnpool2d(2, stride=2)
        (1, 16, 48, 64)
        ConvTranspose2d(in_channels=16, out_channels=3, kernel_size=3, stride=2, padding=2, output_padding=1)
        (1, 3, 94, 126)
        ConvTranspose2d()
        (1, 1, 94, 126)
        '''

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=2, padding=2) # no dilation
        self.pool1 = nn.MaxPool2d(2, stride=2, return_indices=True) # using 2d rather than 3d should preserve the number of channels
        self.batchNorm1 = nn.BatchNorm2d(16)

        self.deconv1 = nn.ConvTranspose2d(in_channels=16, out_channels=3, kernel_size=3, stride=2, padding=2, output_padding=1)
        self.depool = nn.MaxUnpool2d(2, stride=2)
        self.batchNorm2 = nn.BatchNorm2d(3)

        self.deconv2 = nn.ConvTranspose2d(in_channels=3, out_channels=1, kernel_size=3, stride=1, padding=1)
    
    def forward(self, input):
        
        # Encode
        x = self.conv1(input)
        x = self.batchNorm1(x)
        x = F.relu(x)
        x, indices = self.pool1(x)
        # print("After pool & relu: ", x.shape) # x is now a tuple - because MaxPool2d returns x, indices (required for MaxUnpool2d)

        x = self.depool(x, indices=indices)
        x = self.batchNorm1(x)
        x = self.deconv1(x)
        x = self.batchNorm2(x)
        x = self.deconv2(x)

        return x

class SegmentUNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=2, padding=2) # no dilation
        self.pool1 = nn.MaxPool2d(2, stride=2, return_indices=True) # using 2d rather than 3d should preserve the number of channels
        self.batchNorm1 = nn.BatchNorm2d(16)

        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=2, stride=2, padding=2)
        self.pool2 = nn.MaxPool2d(2, stride=2, return_indices=True) # using 2d rather than 3d should preserve the number of channels
        self.batchNorm2 = nn.BatchNorm2d(32)

        self.deconv1 = nn.ConvTranspose2d(in_channels=32, out_channels=16, kernel_size=2, stride=2, padding=2, output_padding=0)
        self.depool = nn.MaxUnpool2d(2, stride=2)

        self.deconv2 = nn.ConvTranspose2d(in_channels=16, out_channels=3, kernel_size=3, stride=2, padding=2, output_padding=1)
        self.depool2 = nn.MaxUnpool2d(2, stride=2)

        self.batchNorm0 = nn.BatchNorm2d(3)
        self.deconv3 = nn.ConvTranspose2d(in_channels=3, out_channels=1, kernel_size=3, stride=1, padding=1)
            
    def forward(self, input):
        # Encode
        x1 = self.conv1(input)
        x2 = self.batchNorm1(x1)
        x3 = F.relu(x2)
        x4, indices = self.pool1(x3)

        x5 = self.conv2(x4)
        x6 = self.batchNorm2(x5)
        x7 = F.relu(x6)
        x8, indices2 = self.pool2(x7)
        # print("After pool & relu: ", x.shape) # x is now a tuple - because MaxPool2d returns x, indices (required for MaxUnpool2d)

        x = self.depool2(x8, indices=indices2)
        x = self.batchNorm2(x)
        x = self.deconv1(x+x5)
        
        x = self.depool(x, indices=indices)
        x = self.batchNorm1(x)
        x = self.deconv2(x + x1)

        x = self.batchNorm0(x)
        x = self.deconv3(x + input)

        # x = torch.sigmoid(x)

        return x