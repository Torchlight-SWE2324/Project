from abc import ABC, abstractmethod

class ResponseGeneratorInterface(ABC):

    @abstractmethod
    def generateResponse(emb, user_query, dictionary_path):
        pass