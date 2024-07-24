import os
from llama_index.core.query_engine import RetrieverQueryEngine
from rag.connectors.llm_connectors.openai_connector import OpenAILlmConnector
from rag.connectors.embedder.baai_embedder import BAAIModel
from llama_index.vector_stores.postgres import PGVectorStore
from rag.retrievers.vector_db_retriever import VectorDBRetriever

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


    llm = OpenAILlmConnector(model_name="gpt-3.5-turbo").get_llm()
    embed_model = BAAIModel().get_model()
    retriever = VectorDBRetriever(
        vector_store, embed_model, query_mode="default", similarity_top_k=2
    )
    query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)

    query_str = "How to check if an endpoint is KMS encrypted?"

    response = query_engine.query(query_str)
    print(response)