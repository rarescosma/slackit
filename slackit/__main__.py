""" Impersonate myself.
"""
import argparse
import sys
import time
from collections import OrderedDict
from multiprocessing.dummy import Pool
from pathlib import Path
from typing import Dict, List

from slackit import Event, Message, Receiver
from slackit._config import Config, configure
from slackit.roam import today
from slackit.services import SERVICE_REGISTRY


def _report(receiver: Receiver, messages: List[Message], delay: int) -> None:
    print(f"Sending {messages} to receiver {receiver} after {delay} seconds.")


def _shoot(receiver: Receiver, messages: List[Message], delay: int) -> None:
    """For multiprocessing."""
    time.sleep(delay)
    service = SERVICE_REGISTRY[receiver.service_name](receiver.receiver_id)
    service.send_many(messages=messages)


def main() -> None:
    """Impersonate myself."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        "-c",
        "--config",
        type=argparse.FileType("r"),
        required=True,
    )
    parser.add_argument(
        "-e",
        "--event",
        required=True,
    )
    parser.add_argument(
        "--check-date",
        action="store_true",
        help="Only run if today's date matches the config.",
    )

    args = parser.parse_args()

    try:
        configure(Path(args.config.name))

        event_spec = Config.get(args.event)

        if args.check_date and today() not in str(event_spec):
            print(f"Couldn't find {today()} in the event spec. Aborting!")
            sys.exit(0)

        event = Event.from_spec(event_spec)
        per_recv: Dict[Receiver, List[Message]] = OrderedDict()

        for r_spec, m_spec in event.message_gen:
            _messages = per_recv.setdefault(Receiver.from_spec(r_spec), [])
            _messages.append(Message.from_spec(m_spec))

        if not per_recv:
            print("Nothing to do!")
            sys.exit(0)

        _args = list(zip(per_recv.keys(), per_recv.values(), event.delay_gen()))
        for _arg in _args:
            _report(*_arg)

        with Pool(len(per_recv)) as pool:
            pool.starmap(_shoot, _args)

    except Exception as exc:  # pylint: disable=broad-except
        sys.exit(exc)

    print("Done!")


if __name__ == "__main__":
    main()
