from typing import Callable

from .action_system import ActionSystemBase
from .service_types import ServiceTypes


class ServiceActionProxy:
    def __init__(self, action_system: ActionSystemBase, service_type: ServiceTypes, slug: str):
        self.action_system = action_system
        self.service_type = service_type
        self.slug = slug

    def __getattr__(self, action_name: str) -> Callable:
        def f(**kwargs: dict):
            return self.action_system.trigger_action(service_type=self.service_type,
                                                     slug=self.slug,
                                                     action_name=action_name,
                                                     parameters=kwargs)

        return f


class ServiceActionProxyFactory:
    def __init__(self, action_system: ActionSystemBase, service_type: ServiceTypes):
        self.action_system = action_system
        self.service_type = service_type

    def __getattr__(self, slug: str) -> ServiceActionProxy:
        return ServiceActionProxy(action_system=self.action_system, service_type=self.service_type, slug=slug)
