
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


class BAAIModel:
    def __init__(self, model_name="BAAI/bge-small-en"):
        self.model_name = model_name
    def get_model(self):
        return HuggingFaceEmbedding(model_name=self.model_name)
