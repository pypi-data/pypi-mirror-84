import time
from abc import ABC, abstractmethod
from typing import ClassVar

from .action_system import ActionSystemBase
from .event_system import EventSystemBase, get_event_listener_decorator
from .predictor_system import PredictorSystemBase
from .service_proxy import ServiceActionProxyFactory
from .service_types import ServiceTypes


class BasicClientBase(ABC):
    _action_system_class: ClassVar[ActionSystemBase] = None
    _event_system_class: ClassVar[EventSystemBase] = None
    _predictor_system_class: ClassVar[PredictorSystemBase] = None

    def __init__(self, api_key: str):
        self.api_key = api_key

        self.is_prepared = False
        self.is_started = False

        self._action_system = self._action_system_class(client=self)
        self._event_system = self._event_system_class(client=self)
        self._predictor_system = self._predictor_system(client=self)

        self.event_listener = get_event_listener_decorator(event_system=self._event_system)

        self._requirements = []

    def add_requirement(self, service_type: ServiceTypes, slug: str) -> None:
        if self.is_prepared:
            raise Exception('you should add requirements before calling prepare')

        self._requirements.append({
            'service_type': service_type,
            'slug': slug,
        })

    def _check_requirement(self, service_type: ServiceTypes, slug: str) -> bool:
        for requirement in self._requirements:
            if requirement.get('service_type') == service_type and requirement.get('slug') == slug:
                return True

        return False

    @abstractmethod
    def validate_service_access(self, service_type: ServiceTypes, slug: str):
        pass

    def prepare(self) -> None:
        self.is_prepared = True

    def get_time(self) -> int:
        return int(time.time())

    def start(self) -> None:
        self._event_system.start()


class PredictorClientBase(BasicClientBase, ABC):
    def __init__(self, api_key: str, slug: str):
        super().__init__(api_key=api_key)

        self.providers = ServiceActionProxyFactory(action_system=self._action_system,
                                                   service_type=ServiceTypes.PROVIDER)
        self.predictor = self._predictor_system
        self.slug = slug

    def validate_service_access(self, service_type: ServiceTypes, slug: str):
        if not self.is_prepared:
            raise Exception('you should call prepare before calling actions or registering event listeners')

        if not self._check_requirement(service_type, slug):
            raise Exception('add all services to requirements before using them')

        if service_type == ServiceTypes.TRADER:
            raise Exception('predictors cannot access traders')


class StrategyClientBase(BasicClientBase, ABC):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

        self.providers = ServiceActionProxyFactory(action_system=self._action_system,
                                                   service_type=ServiceTypes.PROVIDER)
        self.traders = ServiceActionProxyFactory(action_system=self._action_system, service_type=ServiceTypes.TRADER)

    def validate_service_access(self, service_type: ServiceTypes, slug: str):
        if not self.is_prepared:
            raise Exception('you should call prepare before calling actions or registering event listeners')

        if not self._check_requirement(service_type, slug):
            raise Exception('add all services to requirements before using them')
