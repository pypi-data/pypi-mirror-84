from abc import ABC, abstractmethod
from typing import Callable

from .service_types import ServiceTypes


class EventListenerDescriptor:
    def __init__(self, service_type: ServiceTypes, slug: str, event_name: str, fn: Callable):
        self.service_type = service_type
        self.slug = slug
        self.event_name = event_name
        self.fn = fn


class EventSystemBase(ABC):
    def __init__(self, client):
        self.client = client

        self._event_listener_descriptors = []

    def register_event_listener(self, service_type: ServiceTypes, slug: str, event_name: str, fn: Callable) -> None:
        self.client.validate_service_access(service_type, slug)
        self._event_listener_descriptors.append(
            EventListenerDescriptor(service_type=service_type, slug=slug,
                                    event_name=event_name, fn=fn)
        )

    def trigger_event(self, service_type: ServiceTypes, slug: str, event_name: str, payload: dict) -> None:
        for descriptor in self._event_listener_descriptors:
            if descriptor.service_type == service_type and descriptor.slug == slug and descriptor.event_name == event_name:
                descriptor.fn(payload=payload)

    @abstractmethod
    def start(self) -> None:
        pass


def get_event_listener_decorator(event_system: EventSystemBase) -> Callable:
    def event_listener(service_type: ServiceTypes, slug: str, event_name: str) -> Callable:
        def decorator(fn) -> Callable:
            event_system.register_event_listener(service_type=service_type, slug=slug, event_name=event_name, fn=fn)
            return fn

        return decorator

    return event_listener
