import json
import logging
from functools import wraps

from websocket import WebSocketApp

from ..config import BOURSIKA_WS_BASE_URL
from ..core import EventSystemBase, ServiceTypes

logger = logging.getLogger(__name__)


class BoursikaEventSystem(EventSystemBase):
    def start(self) -> None:
        ws = WebSocketApp(f'{BOURSIKA_WS_BASE_URL}/ws/event-system/',
                          on_open=_method_to_function(self, self._on_open),
                          on_message=_method_to_function(self, self._on_message),
                          on_error=_method_to_function(self, self._on_error),
                          on_close=_method_to_function(self, self._on_close))
        ws.run_forever()
        pass

    def _on_open(self, ws: WebSocketApp):
        try:
            body = {
                'action': 'listen',
                'payload': {
                    'events': []
                }
            }

            for event_descriptor in self._event_listener_descriptors:
                body['payload']['events'].append({
                    'service_type': event_descriptor.service_type.value,
                    'slug': event_descriptor.slug,
                    'event_name': event_descriptor.event_name,
                })

            ws.send(json.dumps(body))
        except Exception as ex:
            logger.exception(ex)
            raise ex

    def _on_message(self, ws: WebSocketApp, message: str):
        try:
            content = json.loads(message)

            if content.get('message_type') == 'EVENT':
                service_type = ServiceTypes(content.get('service_type'))
                slug = content.get('slug')
                event_name = content.get('event_name')
                payload = content.get('payload')

                super().trigger_event(service_type=service_type, slug=slug, event_name=event_name, payload=payload)
        except Exception as ex:
            logger.exception(ex)

    def _on_error(self, ws: WebSocketApp, error: Exception):
        logger.exception(error)

    def _on_close(self, ws: WebSocketApp):
        pass


def _method_to_function(container, callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):
        return callback(*args, **kwargs)

    return wrapper
