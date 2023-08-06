import requests

from ..config import BOURSIKA_API_BASE_URL
from ..core import ActionSystemBase, ServiceTypes, ActionError


class BoursikaActionSystem(ActionSystemBase):
    def trigger_action(self, service_type: ServiceTypes, slug: str, action_name: str, parameters: dict) -> dict:
        super().trigger_action(service_type, slug, action_name, parameters)

        if service_type == ServiceTypes.PROVIDER:
            endpoint = f'{BOURSIKA_API_BASE_URL}/providers/{slug}/actions/{action_name}/calls/'
        elif service_type == ServiceTypes.TRADER:
            endpoint = f'{BOURSIKA_API_BASE_URL}/traders/{slug}/actions/{action_name}/calls/'
        else:
            raise Exception('this type of service doesn\'t support actions')

        try:
            response = requests.post(endpoint, json={
                'parameters': parameters,
            }, headers={
                'ApiKey': self.client.api_key,
            }, timeout=10)

            response.raise_for_status()

            return response.json().get('result')
        except requests.exceptions.HTTPError as e:
            raise ActionError(message=e.response.json().get('message'))
