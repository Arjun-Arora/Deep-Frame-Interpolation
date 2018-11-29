import numpy as np
import torch
import torch.nn as nn

# TODO: import pre-trained CNNs

class GANGenerator(torch.nn.Module):
    def __init__(self, conv_layers_size=3, channels=16):
        '''
        :param conv_layers_size: how many conv layers to add in between
        :input (N, C, H, W, 2)
        :output (N, C, H, W)
        '''
#         super(GANGenerator, self).__init__()
#         self.conv_left_first = nn.Conv2d(3, channels, kernel_size=3, stride=1, padding=1)
#         self.conv_right_first = nn.Conv2d(3, channels, kernel_size=3, stride=1, padding=1)
#         self.conv_left_list = nn.ModuleList(
#             [nn.Conv2d(channels, channels, kernel_size=5, stride=1, padding=2) for i in range(conv_layers_size)])
#         self.conv_right_list = nn.ModuleList(
#             [nn.Conv2d(channels, channels, kernel_size=5, stride=1, padding=2) for i in range(conv_layers_size)])
#         self.conv_left_last = nn.Conv2d(channels, 3, kernel_size=3, stride=1, padding=1)
#         self.conv_right_last = nn.Conv2d(channels, 3, kernel_size=3, stride=1, padding=1)
#         self.final_layer = torch.nn.Bilinear(1, 1, 1)  # simple bilinear layer to combine first and last frame
#         self.activation = nn.LeakyReLU()
#         self.final_activation = nn.Tanh()
        super(GANGenerator, self).__init__()
        self.conv_first = nn.Conv2d(6, channels, kernel_size=3, stride=1, padding=1)
        self.conv_list = nn.ModuleList(
            [nn.Conv2d(channels, channels, kernel_size=5, stride=1, padding=2) for i in range(conv_layers_size)])
        self.conv_last = nn.Conv2d(channels, 3, kernel_size=3, stride=1, padding=1)
        self.activation = nn.LeakyReLU()
        self.final_activation = nn.Tanh()
    def forward(self, x):
#         x_left, x_right = x
#         x_left = self.conv_left_first(x_left)
#         x_left = self.activation(x_left)

#         x_right = self.conv_right_first(x_right)
#         x_right = self.activation(x_right)
#         for i in range(len(self.conv_left_list)):
#             x_left = self.conv_left_list[i](x_left)
#             x_left = self.activation(x_left)

#             x_right = self.conv_right_list[i](x_right)
#             x_right = self.activation(x_right)

#         x_left = self.conv_left_last(x_left)
#         x_right = self.conv_right_last(x_right)
#         output = self.final_layer(torch.unsqueeze(x_left, dim=-1),torch.unsqueeze(x_right, dim=-1))
#         return self.final_activation(torch.squeeze(output, dim=-1))
        x = torch.cat(x, dim=1)
        x = self.conv_first(x)
        x = self.activation(x)
        for i in range(len(self.conv_list)):
            x = self.conv_list[i](x)
            x = self.activation(x)

        x = self.conv_last(x)
        return self.final_activation(x)
        # return torch.squeeze(output,dim=-1)


class GANDiscriminator(torch.nn.Module):
    def __init__(self, height=288, width=512, hidden_size=300, channels=16):
        '''
        :param flattened_img_size: size of img when flattened
        :param hidden_size: size of hidden layer
        :input (N, C, H, W)
        :output (N)
        '''
        super(GANDiscriminator, self).__init__()
        self.conv1 = nn.Conv2d(3, channels, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, stride=2)
        self.norm = nn.BatchNorm2d(channels)
        self.linear1 = nn.Linear(channels * height * width, hidden_size)
        self.linear2 = nn.Linear(hidden_size, 1)
        self.activation = nn.LeakyReLU()
        self.final_activation = nn.Sigmoid()
        self.DropoutLinear = torch.nn.Dropout(0.5)
        self.DropoutConv = torch.nn.Dropout(0.1)


    def forward(self, x):
        x = self.conv1(x)
        x = self.norm(x)
        x = self.activation(x)
        x = self.pool(x) # 144 x 256
        x = self.DropoutConv(x)
        x = self.conv2(x)
        x = self.norm(x)
        x = self.DropoutConv(x)
        x = self.activation(x)
        x = self.pool(x) # 72 x 128
        x = self.linear1(x.view(x.shape[0], -1))
        x = self.activation(x)
        x = self.DropoutLinear(x)
        x = self.linear2(x)
        x = self.DropoutLinear(x)
        return self.final_activation(x)
