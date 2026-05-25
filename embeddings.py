from fastembed import TextEmbedding
import faiss
import numpy as np
import json

class EmbeddingIndex:
    def __init__(self, json_path):
        self.model = TextEmbedding()
        
        with open(json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        
        self.texts = [item["definicion"] for item in self.data]
        
        # generar embeddings
        self.embeddings = list(self.model.embed(self.texts))
        self.embeddings = np.array(self.embeddings)
        
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)
    
    def buscar_similares(self, definicion, k=5):
        emb = np.array(list(self.model.embed([definicion])))
        D, I = self.index.search(emb, k)
        
        return [self.data[i] for i in I[0]]