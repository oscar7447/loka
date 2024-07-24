import os
from rag.connectors.embedder.baai_embedder import BAAIModel
from llama_index.vector_stores.postgres import PGVectorStore
from rag.ingestors.directory_ingestor import DirectoryIngestor
if __name__ == "__main__":

    vector_store = PGVectorStore.from_params(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        table_name="aws_documentation",
        embed_dim=384,
    )
    embed_model = BAAIModel().get_model()

    DirectoryIngestor(vector_store=vector_store, embed_model=embed_model).ingest("./sagemaker_documentation")

