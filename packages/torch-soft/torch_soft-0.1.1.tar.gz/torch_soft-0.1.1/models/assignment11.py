import torch
import torch.nn as nn
import torch.nn.functional as F

gbn_splits = 4
dropout_value = 0.05

class A11(nn.Module):
    def __init__(self):
        super(A11,self).__init__()

        self.preblock = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(3, 3), padding=1,stride=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Dropout(dropout_value)
        )

        self.layer11 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128,kernel_size=(3,3),padding=1,stride=1,bias=False),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Dropout(dropout_value),
        )

        self.layer12 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=1, stride=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Dropout(dropout_value),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=1, stride=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Dropout(dropout_value),
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(3, 3), padding=1, stride=1, bias=False),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Dropout(dropout_value),
        )

        self.layer31 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=512,kernel_size=(3,3),padding=1,stride=1,bias=False),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Dropout(dropout_value),
        )

        self.layer32 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), padding=1, stride=1, bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Dropout(dropout_value),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), padding=1, stride=1, bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Dropout(dropout_value),
        )

        self.pool = nn.MaxPool2d(4, 4)

        self.gap = nn.Sequential(
            nn.AvgPool2d(kernel_size=4)
        )

        self.fc = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=10, kernel_size=(1, 1), padding=0, bias=False),
        )

        self.dropout = nn.Dropout(dropout_value)

    def forward(self, x):
        x = self.preblock(x)
        x1 = self.layer11(x)
        r1 = self.layer12(x1)
        x2 = self.layer2(x1+r1)
        x3 = self.layer31(x2)
        r3 = self.layer32(x3)
        x = self.pool(x3+r3)
        # x = self.gap(x)
        x = self.fc(x)
        x = x.view(-1, 10)
        return F.log_softmax(x, dim=-1)


