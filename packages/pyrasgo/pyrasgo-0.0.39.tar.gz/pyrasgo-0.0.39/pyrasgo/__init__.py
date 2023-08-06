__all__ = [
    'connect',
    'orchestrate',
]

from pyrasgo.api import RasgoConnection
from pyrasgo.orchestration import RasgoOrchestration


def connect(api_key):
    return RasgoConnection(api_key=api_key)

def orchestrate(api_key):
    return RasgoOrchestration(api_key=api_key)