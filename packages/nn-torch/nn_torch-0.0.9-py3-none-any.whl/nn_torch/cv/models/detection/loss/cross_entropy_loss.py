# -*- coding: utf-8 -*-
import torch


def cross_entropy_loss_bi(input_: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    return -torch.mean(target * input_.log() + (1. - target) * (1. - input_).log())
