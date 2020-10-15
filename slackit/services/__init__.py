"""Services module."""
from typing import Dict, Type

from .. import Service
from .gdoc import GdocService
from .slack import SlackService

SERVICE_REGISTRY: Dict[str, Type[Service]] = {
    "slack": SlackService,
    "gdoc": GdocService,
}
