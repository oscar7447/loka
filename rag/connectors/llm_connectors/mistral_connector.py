from llama_index.llms.mistralai import MistralAI
from rag.connectors.llm_connectors.abstract_connector import AbstractConnector

class MistralAiLlmConnector(AbstractConnector):


        def get_llm(self):
            llm = MistralAI()
            return llm