from abc import ABC, abstractmethod

class IndexGenerator(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def generate_index(self, model, commands):
        pass