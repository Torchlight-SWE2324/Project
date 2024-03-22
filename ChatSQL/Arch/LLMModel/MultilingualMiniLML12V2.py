from LLMModel import LLMModel
from txtai import Embeddings

class MultilingualMiniLML12V2(LLMModel):
    def __init__(self):
        self.model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.embeddings = Embeddings(self.model_name)

    def getEmbeddings(self):
        return self.embeddings