import torch
from precision_recall import Precision, Recall

class F1Metric:
    def __init__(self):
        self.prec = Precision()
        self.recall = Recall()
        self.epsilon = 1e-10
    def __call__(self, tensor1, tensor2):
        precision = self.prec(tensor1, tensor2)
        recall = self.recall(tensor1, tensor2)
        return 2*((precision*recall)/(precision+recall+self.epsilon))
