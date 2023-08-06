import torch

def MSEMetric(tensor1, tensor2):
    """
    Arguments
    ---------
    x : torch.Tensor
    y : torch.Tensor
    """
    return torch.mean((tensor1 - tensor2)**2)

def MAEMetric(tensor1, tensor2):
    """
    Arguments
    ---------
    x : torch.Tensor
    y : torch.Tensor
    """
    return torch.mean((tensor1 - tensor2))
