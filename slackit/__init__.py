"""Models and stuff."""
import abc
import random
from dataclasses import dataclass
from itertools import product
from typing import Iterable, Iterator, List, Sequence, Tuple, Union, cast

__version__ = "0.3.5"

EventSpec = dict
ReceiverSpec = str
ReceiverId = str
MessageSpec = Union[dict, str]
Delay = Tuple[int, int, int]


@dataclass(frozen=True)
class Event:
    """Event."""

    receivers: Sequence[ReceiverSpec]
    strategy: str
    messages: Sequence[MessageSpec]
    delay: Delay

    @classmethod
    def from_spec(cls, spec: EventSpec) -> "Event":
        """Create from spec."""
        return cls(
            receivers=spec.get("receivers", []) or [],
            strategy=spec.get("strategy", "UNKNOWN"),
            messages=spec.get("messages", []) or [],
            delay=cast(Delay, spec.get("delay", (0, 0, 0))),
        )

    def delay_gen(self) -> Iterator[int]:
        """Obtain next delay sample."""
        _next = random.randint(0, self.delay[0])
        for _ in iter(int, 1):
            yield _next
            _next = _next + random.randint(self.delay[1], self.delay[2])

    @property
    def message_gen(self) -> Iterable[Tuple[ReceiverSpec, MessageSpec]]:
        """Generate (receiver, message) tuples based on selected strategy."""
        if self.strategy == "BROADCAST":
            return product(self.receivers, self.messages)
        if self.strategy == "SAMPLE":
            return zip(self.receivers, self._message_samples)
        raise ValueError(f"Uknown strategy: '{self.strategy}'")

    @property
    def _message_samples(self) -> List[MessageSpec]:
        num_receivers = len(self.receivers)
        if num_receivers <= len(self.messages):
            return random.sample(self.messages, k=num_receivers)
        return [random.choice(self.messages) for _ in range(num_receivers)]


@dataclass(frozen=True)
class Receiver:
    """Receiver."""

    service_name: str
    receiver_id: ReceiverId

    @classmethod
    def from_spec(cls, spec: ReceiverSpec) -> "Receiver":
        """Create from spec."""
        if len(_parts := spec.split(":")) >= 2:
            return cls(
                service_name=_parts[0],
                receiver_id=":".join(_parts[1:]),
            )
        raise ValueError(f"Invalid {cls.__name__} spec: {spec}")


@dataclass(frozen=True)
class Message:
    """Message."""

    text: str = ""
    style: str = "NORMAL_TEXT"
    items: Sequence[str] = ()

    @classmethod
    def from_spec(cls, spec: MessageSpec) -> "Message":
        """Create from spec."""
        if isinstance(spec, dict):
            return cls(**spec)
        if isinstance(spec, str):
            return cls(text=spec)
        raise ValueError(f"Invalid {cls.__name__} spec: {spec}")


class Service(metaclass=abc.ABCMeta):
    """Service abstraction."""

    _receiver_id: ReceiverId

    def __init__(self, receiver_id: ReceiverId) -> None:
        self._receiver_id = receiver_id

    @abc.abstractmethod
    def send_one(self, message: Message) -> None:
        """Send one message."""

    @abc.abstractmethod
    def send_many(self, messages: List[Message]) -> None:
        """Send multiple messages."""
