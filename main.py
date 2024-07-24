from fastapi import (
    FastAPI,
    status,
    Depends,
    HTTPException,
    BackgroundTasks,
    Request,
)
from rag.connectors.llm_connectors.enum import SuportedModels
import uvicorn
import os
from rag.connectors.embedder.baai_embedder import BAAIModel
from llama_index.vector_stores.postgres import PGVectorStore
from rag.ingestors.directory_ingestor import DirectoryIngestor
from llama_index.core.query_engine import RetrieverQueryEngine
from rag.connectors.llm_connectors.openai_connector import OpenAILlmConnector
from rag.connectors.embedder.baai_embedder import BAAIModel
from llama_index.vector_stores.postgres import PGVectorStore
from rag.retrievers.vector_db_retriever import VectorDBRetriever
from rag.connectors.llm_connectors.factory import LlmConnectorFactory
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

endpoint = "http://phoenix:6006/v1/traces"
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

app = FastAPI(title="Loka Test",description="RAG system for AWS documentation.")

@app.get("/ingest_data")
def ingest_data(
    background_tasks: BackgroundTasks,
    path: str = "./sagemaker_documentation"):


    vector_store = PGVectorStore.from_params(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        table_name="aws_documentation",
        embed_dim=384,
    )
    #Here we can use a factory pattern to get any abstracted embedder
    embed_model = BAAIModel().get_model()
    try:
        background_tasks.add_task(
        DirectoryIngestor(vector_store=vector_store, embed_model=embed_model).ingest,
        path=path,
        )
    except Exception as e:
        return str(e)
    return {"status": "success"}

@app.get("/query")
def query_information(query_str: str, supported_models:SuportedModels = SuportedModels.openai_3_5_turbo):
    if len(query_str) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query string cannot be empty",
        )
    vector_store = PGVectorStore.from_params(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        table_name="aws_documentation",
        embed_dim=384,
    )

    llm_connector = LlmConnectorFactory().get_connector(supported_models)
    llm = llm_connector.get_llm()
    embed_model = BAAIModel().get_model()
    retriever = VectorDBRetriever(
        vector_store, embed_model, query_mode="default", similarity_top_k=2
    )
    query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)

    response = query_engine.query(query_str)
    return response.response
