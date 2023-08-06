from abc import ABC, abstractmethod

from .service_types import ServiceTypes


class ActionSystemBase(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def trigger_action(self, service_type: ServiceTypes, slug: str, action_name: str, parameters: dict) -> dict:
        self.client.validate_service_access(service_type, slug)
