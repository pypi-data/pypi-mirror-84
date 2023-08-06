from __future__ import print_function
import torch.nn.functional as F
import torch
import torch.nn as nn
from utils.normalization import *
gbn_splits = 4
dropout_value = 0.05

hidden_units = [16,32,64,128,200]
class Quiz_net(nn.Module):
    def __init__(self, batch_normalization_type="BN"):
        super(Quiz_net, self).__init__()
        # Input Block
        self.convblock1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=8, kernel_size=(3, 3), padding=1, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(8) if batch_normalization_type == "BN" else GhostBatchNorm(8, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 26

        # CONVOLUTION BLOCK 1
        self.convblock2 = nn.Sequential(
            nn.Conv2d(in_channels=11, out_channels=11, kernel_size=(3, 3), padding=1, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(11) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 24

        self.pool1 = nn.MaxPool2d(2, 2)  # output_size = 12

        # CONVOLUTION BLOCK 2
        self.convblock3 = nn.Sequential(
            nn.Conv2d(in_channels=22, out_channels=3, kernel_size=(1, 1), padding=0, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(3) if batch_normalization_type == "BN" else GhostBatchNorm(32, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 10
        self.convblock4 = nn.Sequential(
            nn.Conv2d(in_channels=25, out_channels=25, kernel_size=(3, 3), padding=1, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(25) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 8
        self.convblock5 = nn.Sequential(
            nn.Conv2d(in_channels=50, out_channels=50, kernel_size=(3, 3), padding=1, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(50) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 6

        self.pool2 = nn.MaxPool2d(2, 2)  # output_size = 12

        self.convblock6 = nn.Sequential(
            nn.Conv2d(in_channels=78, out_channels=32, kernel_size=(1, 1), padding=0, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(32) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 6

        self.convblock7 = nn.Sequential(
            nn.Conv2d(in_channels=110, out_channels=110, kernel_size=(3, 3), padding=1, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(110) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 6

        self.convblock8 = nn.Sequential(
            nn.Conv2d(in_channels=220, out_channels=220, kernel_size=(3, 3), padding=1, bias=False),
            nn.ReLU(),
            nn.BatchNorm2d(220) if batch_normalization_type == "BN" else GhostBatchNorm(16, gbn_splits),
            nn.Dropout(dropout_value)
        )  # output_size = 6

        # OUTPUT BLOCK
        self.gap = nn.Sequential(
            nn.AvgPool2d(kernel_size=8)
        )  # output_size = 1

        self.convblock9 = nn.Sequential(
            nn.Conv2d(in_channels=220, out_channels=10, kernel_size=(1, 1), padding=0, bias=False),
            # nn.BatchNorm2d(10),
            # nn.ReLU(),
            # nn.Dropout(dropout_value)
        )

        self.dropout = nn.Dropout(dropout_value)

    def forward(self, x1):
        x2 = self.convblock1(x1)
        x3 = self.convblock2(torch.cat((x1, x2), dim=1))
        x4 = self.pool1(torch.cat((x1, x2, x3), dim=1))
        x5 = self.convblock3(x4)
        x6 = self.convblock4(torch.cat((x4, x5), dim=1))
        x7 = self.convblock5(torch.cat((x4, x5,x6), dim=1))
        x8 = self.pool1(torch.cat((x5, x6,x7), dim=1))
        x9 = self.convblock6(x8)
        x10 = self.convblock7(torch.cat((x8, x9), dim=1))
        x11 = self.convblock8(torch.cat((x8, x9,x10), dim=1))
        x12 = self.gap(x11)
        x13 = self.convblock9(x12)

        x13 = x13.view(-1, 10)
        return F.log_softmax(x13, dim=-1)