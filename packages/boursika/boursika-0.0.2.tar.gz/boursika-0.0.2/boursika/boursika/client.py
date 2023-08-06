from .action_system import BoursikaActionSystem
from .event_system import BoursikaEventSystem
from .predictor_system import BoursikaPredictorSystem
from ..core import StrategyClientBase, PredictorClientBase


class BoursikaStrategyClient(StrategyClientBase):
    _action_system_class = BoursikaActionSystem
    _event_system_class = BoursikaEventSystem
    _predictor_system_class = BoursikaPredictorSystem


class BoursikaPredictorClient(PredictorClientBase):
    _action_system_class = BoursikaActionSystem
    _event_system_class = BoursikaEventSystem
    _predictor_system_class = BoursikaPredictorSystem
