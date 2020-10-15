"""Slack service."""
from functools import lru_cache
from typing import List

from slackcli.cli import send_message, slack

from .. import Message, Service
from .._config import Config


class SlackService(Service):
    """Slack Service."""

    def send_one(self, message: Message) -> None:
        _init_cli()
        send_message(self._receiver_id, self._format(message))

    def send_many(self, messages: List[Message]) -> None:
        if not messages:
            return
        self.send_one(Message(text="\n".join(map(self._format, messages))))

    @staticmethod
    def _format(message: Message) -> str:
        if message.style.startswith("HEADING"):
            return f"*{message.text}*"
        if message.style == "LIST":
            return "\n".join([f"* {_}" for _ in message.items])
        return message.text


@lru_cache(maxsize=128)
def _init_cli() -> None:
    return slack.init(user_token=Config.get("slack_token"))
