import torch
import torch.nn as nn
import torch.autograd as autograd
import torch.optim as optim
import numpy as np


def initialize_weights(networks):
    for m in networks.modules():
        if isinstance(m, nn.Conv2d):
            m.weight.data.normal_(0, 0.02)
            m.bias.data.zero_()
        elif isinstance(m, nn.ConvTranspose2d):
            m.weight.data.normal_(0, 0.02)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.weight.data.normal_(0, 0.02)
            m.bias.data.zero_()
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()

#######################
# discriminator model #
#######################
class discriminator_nn(nn.Module):
    # initializers
    def __init__(self, input_nc, output_nc, nf=32):
        super(discriminator_nn, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(input_nc, nf * 1, kernel_size=3, stride=1, padding=1),
            nn.LeakyReLU(0.2, True),
            nn.Conv2d(nf * 1, nf * 2, kernel_size=3, stride=2, padding=1),
            nn.LeakyReLU(0.2, True),
            nn.Conv2d(nf * 2, nf * 4, kernel_size=3, stride=1, padding=1),
            nn.InstanceNorm2d(nf * 4),
            nn.LeakyReLU(0.2, True),
            nn.Conv2d(nf * 4, nf * 4, kernel_size=3, stride=2, padding=1),
            nn.LeakyReLU(0.2, True),
            nn.Conv2d(nf * 4, nf * 8, kernel_size=3, stride=1, padding=1),
            nn.InstanceNorm2d(nf * 4),
            nn.LeakyReLU(0.2, True),
            nn.Conv2d(nf * 8, nf * 8, kernel_size=3, stride=1, padding=1),
            nn.InstanceNorm2d(nf * 4),
            nn.LeakyReLU(0.2, True),
            nn.Conv2d(nf * 8, output_nc, kernel_size=3, stride=1, padding=1),
            nn.Sigmoid()
        )

        initialize_weights(self)

    # forward method
    def forward(self, input):
        output = self.conv(input)
        return output

###################
# generator model #
###################
# Set up resnet_block for generator model
class resnet_block(nn.Module):
    def __init__(self, nf, kernel_size, stride, padding):
        super(resnet_block, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(nf, nf, kernel_size, stride, padding),
            nn.InstanceNorm2d(nf),
            nn.ReLU(True),
            nn.Conv2d(nf, nf, kernel_size, stride, padding),
            nn.InstanceNorm2d(nf)
        )

        initialize_weights(self)

    def forward(self, input):
        output = input + self.conv(input)

        return output

# Set up generator model
class generator_nn(nn.Module):
    def __init__(self, input_nc, output_nc, nf=64, nblock=8):
        # parameters
        super(generator_nn, self).__init__()

        # down-convolution
        self.down_conv = nn.Sequential(
          nn.Conv2d(input_nc, nf, kernel_size=7, stride=1, padding = 3),
          nn.InstanceNorm2d(nf),
          nn.ReLU(True),
          nn.Conv2d(nf * 1, nf * 2, kernel_size=3, stride=2, padding = 1),
          nn.Conv2d(nf * 2, nf * 2, kernel_size=3, stride=1, padding = 1),
          nn.ReLU(True),
          nn.Conv2d(nf * 2, nf * 4, kernel_size=3, stride=2, padding = 1),
          nn.Conv2d(nf * 4, nf * 4, kernel_size=3, stride=1, padding = 1),
          nn.InstanceNorm2d(nf * 4),
          nn.ReLU(True)
        )

        # 8 residual blocks
        self.resnet_blocks = []
        for i in range(nblock):
            self.resnet_blocks.append(resnet_block(nf * 4, kernel_size=3, stride=1, padding=1))

        self.resnet = nn.Sequential(*self.resnet_blocks)

        # up-convolution
        self.up_conv = nn.Sequential(
            nn.ConvTranspose2d(nf * 4, nf * 2, 3, 2, 1, 1),
            nn.Conv2d(nf * 2, nf * 2, kernel_size=3, stride=1, padding=1),
            nn.InstanceNorm2d(nf * 2),
            nn.ReLU(True),
            nn.ConvTranspose2d(nf * 2, nf, 3, 2, 1, 1),
            nn.Conv2d(nf, nf, kernel_size=3, stride=1, padding=1),
            nn.InstanceNorm2d(nf),
            nn.ReLU(True),
            nn.Conv2d(nf, output_nc, kernel_size=7, stride=1, padding=3),
            nn.Tanh(),
        )

        initialize_weights(self)

    def forward(self, input):
        temp = self.down_conv(input)
        temp = self.resnet(temp)
        output = self.up_conv(temp)

        return output


class CartoonGAN():

    def __init__(self, args):
        '''
        :args -> dictionary of arguments
        '''
        self.args = args

    def model_name(self):
        return 'Cartoon GAN'

    def defineG_cartoon(self):
        input_nc = self.args[input_nc]
        output_nc = self.args[output_nc]
        nblock = self.args[nblock]
        return


    def initialize(self):
        args = self.args
        # create Tensors
        self.real_A = torch.Tensor(args['batch_size'], args['input_nc'], args['final_img_size'], args['final_img_size'])
        self.real_B = torch.Tensor(args['batch_size'], args['input_nc'], args['final_img_size'], args['final_img_size'])
        self.fake_B = torch.Tensor(args['batch_size'], args['input_nc'], args['final_img_size'], args['final_img_size'])
        self.edge_B = torch.Tensor(args['batch_size'], args['input_nc'], args['final_img_size'], args['final_img_size'])

        # create models
