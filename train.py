import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torch.autograd as autograd
import torch.optim as optims
import numpy as np
from torch.autograd import Variable
import generator
import discriminator
import helpers

LEARNING_RATE_G = 0.002
LEARNING_RATE_D = 0.002

#################
#Helper functions
#################
def get_vgg19(nf, pretrained,path):
    net= torchvision.models.vgg19()
    if pretrained:
        net.load_state_dict(torch.load(path))
    net.classifier = nn.Sequential(
        nn.Linear(512 * 7 * 7, 4096),
        nn.ReLU(True),
        nn.Dropout(),
        nn.Linear(4096,4096),
        nn.ReLU(True),
        nn.Dropout(),
        nn.Linear(4096, nf),
    )
    return net

def load_training_set(data_path):
    train_dataset = torchvision.datasets.ImageFolder(
        root = data_path,
        transform = torchvision.transforms.ToTensor()
    )
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=64,
        num_workers=0,
        shuffle=True
    )
    return train_loader

#################
# Model building
#################
Generator_model = generator.generator_nn(3,3)
Discriminator_model = discriminator.discriminator_nn(3,1)
BCE_loss = nn.BCELoss()
L1_loss = nn.L1Loss()
Generator_optimizer = optims.Adam(Generator_model.parameters(), lr = LEARNING_RATE_G, betas = (0.5, 0.999))
Discriminator_model = optims.Adam(Discriminator_model.parameters(), lr = LEARNING_RATE_D, betas = (0.5, 0.999))


#################
#Testing field
#################
# print(get_vgg19(16, True, "vgg19-dcbb9e9d.pth"))
anime_figure_dataset = load_training_set("training_set")
print(len(anime_figure_dataset))
for batch_idx, (data, target) in enumerate(anime_figure_dataset):
    print(data, target)
