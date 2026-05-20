import numpy as np
import json
import faiss
from fastembed import TextEmbedding

class SchemaRetriever:
    def __init__(self):
        self.embed_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        self.index = None
        self.schema_texts = []
        self.schema_metadata = []

    def build_index(self):
        with open('tables.json', 'r') as file:
            data = json.load(file)
        for db in data:
            content = "database: " + db["db_id"] + " | " 
            for i,table in enumerate(db["table_names"]):
                content += "table: " + table.replace(" ", "_") + ", columns: "
                cols = [col[1].replace(" ", "_") for col in db["column_names"] if col[0] == i]
                content += ", ".join(cols) + " | "
            self.schema_texts.append(content)
            self.schema_metadata.append(db["db_id"])
        embeddings = list(self.embed_model.embed(self.schema_texts))
        embeddings_matrix = np.array(embeddings).astype('float32')
        dimension = embeddings_matrix.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_matrix)

    def retrieve_schema(self,query):
        query_embedding= list(self.embed_model.embed(query))
        query_embedding_matrix = np.array(query_embedding).astype('float32')
        distances, indices = self.index.search(query_embedding_matrix, k=1)
        return self.schema_metadata[indices[0][0]], self.schema_texts[indices[0][0]]