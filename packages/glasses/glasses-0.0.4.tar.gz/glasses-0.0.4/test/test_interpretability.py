import torch
from torch import nn
from glasses.interpretability import GradCam, SaliencyMap
from glasses.interpretability.utils import *
import matplotlib.pyplot as plt

def test_gradcam():
    x = torch.rand((1, 3, 224, 224))

    model = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3),
        nn.Conv2d(32, 32, kernel_size=3),
        nn.AdaptiveAvgPool2d((1,1)),
        nn.Flatten(),
        nn.Linear(32, 10)
    )

    cam = GradCam()

    cam_res = cam(x, model)

    assert cam_res.show()


def test_saliency_map():
    x = torch.rand((1, 3, 224, 224))

    model = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3),
        nn.Conv2d(32, 32, kernel_size=3),
        nn.AdaptiveAvgPool2d((1,1)),
        nn.Flatten(),
        nn.Linear(32, 10)
    )

    saliency = SaliencyMap()

    saliency_res = saliency(x, model)

    assert saliency_res.show()

    assert len(saliency_res.saliency_map.squeeze(0).shape) == 2

def test_find_last_layer():
    x = torch.rand((1, 3, 224, 224))

    model = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3),
        nn.Conv2d(32, 32, kernel_size=3)
    )

    last  = find_last_layer(x, model, nn.Conv2d)

    assert last is model[1]


def test_find_first_layer():
    x = torch.rand((1, 3, 224, 224))

    model = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3),
        nn.Conv2d(32, 32, kernel_size=3)
    )

    last  = find_first_layer(x, model, nn.Conv2d)

    assert last is model[0]

    
        