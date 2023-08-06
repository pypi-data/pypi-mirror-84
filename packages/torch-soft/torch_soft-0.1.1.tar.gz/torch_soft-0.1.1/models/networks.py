from __future__ import print_function
import torch.nn.functional as F
import torch
import torch.nn as nn
from utils.normalization import *
gbn_splits = 4
dropout_value = 0.05


class NetS6(nn.Module):
    def __init__(self, batch_normalization_type="BN"):
        super(NetS6, self).__init__()
        # Input Block
        self.convblock1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=8, kernel_size=(3, 3), padding=0, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(8) if batch_normalization_type == "BN" else GhostBatchNorm(8, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 26

        # CONVOLUTION BLOCK 1
        self.convblock2 = nn.Sequential(
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3, 3), padding=0, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(16) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 24

        # TRANSITION BLOCK 1
        self.convblock3 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=8, kernel_size=(1, 1), padding=0, bias=False),
        )  # output_size = 24
        self.pool1 = nn.MaxPool2d(2, 2)  # output_size = 12

        # CONVOLUTION BLOCK 2
        self.convblock4 = nn.Sequential(
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3, 3), padding=0, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(16) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 10
        self.convblock5 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=(3, 3), padding=0, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(16) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 8
        self.convblock6 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=(3, 3), padding=0, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(16) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 6
        self.convblock7 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=(3, 3), padding=1, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(16) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 6

        # OUTPUT BLOCK
        self.gap = nn.Sequential(
            nn.AvgPool2d(kernel_size=6)
        )  # output_size = 1

        self.convblock8 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=10, kernel_size=(1, 1), padding=0, bias=False),
            # nn.BatchNorm2d(10),
            # nn.ReLU(),
            # nn.Dropout(dropout_value)
        )

        self.dropout = nn.Dropout(dropout_value)

    def forward(self, x):
        x = self.convblock1(x)
        x = self.convblock2(x)
        x = self.convblock3(x)
        x = self.pool1(x)
        x = self.convblock4(x)
        x = self.convblock5(x)
        x = self.convblock6(x)
        x = self.convblock7(x)
        x = self.gap(x)
        x = self.convblock8(x)

        x = x.view(-1, 10)
        return F.log_softmax(x, dim=-1)

gbn_splits = 4
dropout_value = 0.05
hidden_units = [16,32,64,128,200]
class Net(nn.Module):
  def __init__(self, batch_normalization_type="BN"):
    super(Net, self).__init__()
    self.conv1 = nn.Sequential(
        nn.Conv2d(in_channels=3, out_channels=hidden_units[0], kernel_size=(3, 3), padding=2, bias=False, padding_mode = 'reflect', dilation=2), # Input=32x32x3 Kernel=3x3x1x16 Output=32x32x16 RF=3x3
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[0]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[0], gbn_splits),
        nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[0], out_channels=hidden_units[1], kernel_size=(3, 3), padding=2, bias=False, padding_mode = 'reflect'), # Input=32x32x16 Kernel=3x3x10x32 Output=32x32x32 RF=5x5
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[1]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[1], gbn_splits),
        nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[1], out_channels=hidden_units[1], kernel_size=(3, 3), padding=2, bias=False,padding_mode = 'reflect'), # Input=32x32x16 Kernel=3x3x10x32 Output=32x32x32 RF=5x5
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[1]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[1], gbn_splits),
        nn.Dropout(dropout_value),
        nn.MaxPool2d(kernel_size=2, stride=2)
        ) #output_size=16x16x32

    self.conv2 = nn.Sequential(
        nn.Conv2d(in_channels=hidden_units[1], out_channels=hidden_units[1], kernel_size=(3, 3), padding=2, bias=False, groups=hidden_units[1], padding_mode = 'reflect'), #Input=14x14x10 Kernel=3x3x10x10 Output=12x12x10 RF=10x10
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[1]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[1], gbn_splits),
        nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[1], out_channels=hidden_units[2], kernel_size=(1,1), padding=1, bias=False, padding_mode = 'reflect'), #Input=12x12x10 Kernel=3x3x10x12 Output=10x10x12 RF=14x14
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[2]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[2], gbn_splits),
        nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[2], out_channels=hidden_units[2], kernel_size=(3, 3), padding=2, bias=False, groups = hidden_units[2], padding_mode = 'reflect'), #Input=10x10x12 Kernel=3x3x12x16 Output=8x8x16 RF=18x18
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[2]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[2], gbn_splits),
        nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[2], out_channels=hidden_units[3], kernel_size=(1, 1), padding=1, bias=False, padding_mode = 'reflect'), #Input=10x10x12 Kernel=3x3x12x16 Output=8x8x16 RF=18x18
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[3]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[2], gbn_splits),
        nn.Dropout(dropout_value),
        nn.MaxPool2d(kernel_size=2, stride=2)
        )#output_size=8x8x32

    self.conv3 = nn.Sequential(
        nn.Conv2d(in_channels=hidden_units[3], out_channels=hidden_units[4], kernel_size=(3, 3), padding=1, bias=False, padding_mode = 'reflect'), #Input=14x14x10 Kernel=3x3x10x10 Output=12x12x10 RF=10x10
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[4]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[2], gbn_splits),
        nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[4], out_channels=hidden_units[4], kernel_size=(3, 3), padding=1, bias=False, padding_mode = 'reflect'), #Input=14x14x10 Kernel=3x3x10x10 Output=12x12x10 RF=10x10
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[4]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[2], gbn_splits),
        nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[4], out_channels=hidden_units[3], kernel_size=(1,1), padding=1, bias=False, padding_mode = 'reflect'), #Input=12x12x10 Kernel=3x3x10x12 Output=10x10x12 RF=14x14
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[3]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[1], gbn_splits),
        nn.Dropout(dropout_value),
        # nn.Conv2d(in_channels=hidden_units[3], out_channels=hidden_units[3], kernel_size=(3, 3), padding=1, bias=False, padding_mode = 'reflect'), #Input=10x10x12 Kernel=3x3x12x16 Output=8x8x16 RF=18x18
        # nn.ReLU(),
        # nn.BatchNorm2d(hidden_units[3]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[2], gbn_splits),
        # nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[3], out_channels=hidden_units[3], kernel_size=(3, 3), padding=1, bias=False, padding_mode = 'reflect'), #Input=10x10x12 Kernel=3x3x12x16 Output=8x8x16 RF=18x18
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[3]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[2], gbn_splits),
        nn.Dropout(dropout_value),
        nn.Conv2d(in_channels=hidden_units[3], out_channels=hidden_units[2], kernel_size=(1, 1), padding=0, bias=False, padding_mode = 'reflect'), #Input=10x10x12 Kernel=3x3x12x16 Output=8x8x16 RF=18x18
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[2]) if batch_normalization_type=="BN" else GhostBatchNorm(hidden_units[1], gbn_splits),
        nn.Dropout(dropout_value),
        nn.MaxPool2d(kernel_size=2, stride=2)
        )#output_size=8x8x32

    self.conv4 = nn.Sequential(
        nn.Conv2d(in_channels=hidden_units[2], out_channels=hidden_units[2], kernel_size=(3, 3), padding=1, bias=False, padding_mode = 'reflect'), #Input=6x6x16 Kernel=3x3x16x16 Output=4x4x16 RF=26x26
        nn.ReLU(),
        nn.BatchNorm2d(hidden_units[2]) if batch_normalization_type=="BN" else GhostBatchNorm(16, gbn_splits),
        nn.AvgPool2d(kernel_size=(7)), #Input=4x4x16 Kernel=4x4x16x16 Output=1x1x16
        nn.Conv2d(in_channels=hidden_units[2], out_channels=hidden_units[1], kernel_size=(1, 1), padding=0, bias=False), #Input=1x1x16 Kernel=1x1x16x10 Output=1x1x10
        nn.Conv2d(in_channels=hidden_units[1], out_channels=10, kernel_size=(1, 1), padding=0, bias=False)
        )


  def forward(self, x):
    x = self.conv1(x)
    x = self.conv2(x)
    x = self.conv3(x)
    x = self.conv4(x)
    x = x.view(-1, 10)
    return F.log_softmax(x, dim=1)
