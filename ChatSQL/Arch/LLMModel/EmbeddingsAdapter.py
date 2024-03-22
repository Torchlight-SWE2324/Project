from txtai import Embeddings


class EmbeddingsAdapter(embeddingsChatSQL):
    def __init__(self, embeddingsChatSQL) -> None:
        self.embeddingsChatSQL = embeddingsChatSQL
        
    def index(self, commands):
        emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})

        for command in commands:
            emb.index([{"table_name": command["table_name"], "table_description": command["table_description"], "field_name": command["field_name"], "field_type": command["field_type"], "field_references": command["field_references"], "text": command["table_description"]}])
        
    def save(self, emb, path):
        emb.save(path)

    def close(self, emb):
        emb.close()
        
    def load(self, path):
        emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})
        emb.load(path)

    """def search(self, emb, user_query, dictionary_name):
        if emb == None:
            return "Error: there is no model connected"
        else:"""