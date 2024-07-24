from llama_index.llms.openai import OpenAI
from rag.connectors.llm_connectors.abstract_connector import AbstractConnector

class OpenAILlmConnector(AbstractConnector):
        def __init__(self, model_name):
            self.model_name = model_name


        def get_llm(self):
            llm = OpenAI(model=self.model_name)
            return llm