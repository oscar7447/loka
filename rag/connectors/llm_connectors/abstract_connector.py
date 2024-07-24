from abc import abstractmethod, ABC

class AbstractConnector(ABC):
    @abstractmethod
    def get_llm():
        pass