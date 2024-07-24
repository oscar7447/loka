from rag.connectors.llm_connectors.openai_connector import OpenAILlmConnector
from rag.connectors.llm_connectors.mistral_connector import MistralAiLlmConnector
from rag.connectors.llm_connectors.enum import SuportedModels
class LlmConnectorFactory:

    def get_connector(self, model_name):

        models = {
        SuportedModels.openai_3_5_turbo:OpenAILlmConnector("gpt-3.5-turbo"), 
         SuportedModels.mistral:MistralAiLlmConnector(),
         SuportedModels.openai_4:OpenAILlmConnector("gpt-4")
         }
        return models.get(model_name)
