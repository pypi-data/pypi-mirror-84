import requests

from ..config import BOURSIKA_API_BASE_URL
from ..core import PredictorSystemBase


class BoursikaPredictorSystem(PredictorSystemBase):
    def publish_event(self, event_name: str, payload: dict) -> None:
        endpoint = f'{BOURSIKA_API_BASE_URL}/predictors/{self.client.slug}/events/{event_name}/'

        try:
            response = requests.post(endpoint, json={
                'payload': payload,
            }, headers={
                'ApiKey': self.client.api_key,
            }, timeout=10)

            response.raise_for_status()

            return response.json().get('result')
        except requests.exceptions.HTTPError as e:
            raise Exception(e.response.json().get('message'))
