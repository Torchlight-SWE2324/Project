from abc import ABC, abstractmethod
from txtai import Embeddings

#define an abstract class for the LLM model, where the name of the model is passed as an argument

class LLMModel(ABC):
    def __init__(self, model_name):
        self.model_name = model_name
        self.embeddings = Embeddings(model_name)

    @abstractmethod
    def getEmbeddings(self):
        pass