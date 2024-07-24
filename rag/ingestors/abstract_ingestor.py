from abc import ABC, abstractmethod

class AbstractIngestor(ABC):
    @abstractmethod
    def ingest() -> None:
        pass