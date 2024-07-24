from rag.connectors.llm_connectors.abstract_connector import AbstractConnector
from llama_index.llms.llama_cpp import LlamaCPP
import os
class LlamaLlmConnector(AbstractConnector):

    def get_llm(self):
        model_host = os.getenv("LLAMA_MODEL_HOST")

        llm = LlamaCPP(
            # You can pass in the URL to a GGML model to download it automatically
            model_url=model_host,
            # optionally, you can set the path to a pre-downloaded model instead of model_url
            model_path=None,
            temperature=0.1,
            max_new_tokens=256,
            # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
            context_window=3900,
            # kwargs to pass to __call__()
            generate_kwargs={},
            # kwargs to pass to __init__()
            # set to at least 1 to use GPU
            model_kwargs={"n_gpu_layers": 1},
            verbose=True,
        )
        return llm