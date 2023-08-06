from abc import ABC, abstractmethod


class PredictorSystemBase(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def publish_event(self, event_name: str, payload: dict) -> None:
        pass
