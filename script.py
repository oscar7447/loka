import psycopg2
import os
from rag.connectors.llm_connectors.llama_connector import LlamaLlmConnector

if __name__ == "__main__":
    conn = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
    )
    conn.autocommit = True

   # with conn.cursor() as c:
   #     db_name = os.getenv("POSTGRES_DB")
   #     c.execute(f"DROP DATABASE IF EXISTS {db_name}")
   #     c.execute(f"CREATE DATABASE {db_name}")

