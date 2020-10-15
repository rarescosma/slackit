""" Roam helper script.
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

from slackit._jinja import render_jinja


def _ord(of_int: int) -> str:
    """For Roam"""
    return str(of_int) + (
        "th"
        if 4 <= of_int % 100 <= 20
        else {1: "st", 2: "nd", 3: "rd"}.get(of_int % 10, "th")
    )


def _removesuffix(text: str, suffix: str) -> str:
    if suffix and text.endswith(suffix):
        return text[: -len(suffix)]
    return text[:]


def _parse_json_export(json_file: Path) -> dict:
    _parsed = json.loads(json_file.read_text())[0]
    context = {"page_title": _parsed["title"]}
    for child in _parsed["children"]:
        context[_removesuffix(child["string"].lower(), "::")] = [
            _["string"] for _ in child["children"]
        ]
    return context


def today() -> str:
    """Today's date in Roam format."""
    _today = date.today()
    return _today.strftime(f"%B {_ord(_today.day)}, %Y")


def main() -> None:
    """
    Generate YAML config from a Jinja template and a Roam JSON export.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        "-t",
        "--template",
        type=argparse.FileType("r"),
        required=True,
    )
    parser.add_argument(
        "-j",
        "--json",
        type=argparse.FileType("r"),
        required=True,
    )

    args = parser.parse_args()

    try:
        print(
            render_jinja(
                Path(args.template.name).read_text(),
                context=(_parse_json_export(Path(args.json.name))),
            )
        )
    except Exception as exc:  # pylint: disable=broad-except
        sys.exit(exc)


if __name__ == "__main__":
    main()
