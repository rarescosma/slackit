"""Jinja templating directives."""
from pathlib import Path
from typing import Any, Dict

import jinja2


def render_jinja_template(
    template_file: Path, context: Dict[str, Any], output_file: Path
) -> None:
    """Render the given jinja template file into the output file using
    the context."""
    output_file.write_text(
        render_jinja(template=template_file.read_text(), context=context)
    )


def render_jinja(template: str, context: Dict[str, Any]) -> str:
    """Render the input jinja string using the context and return it."""
    jinja_env = jinja2.Environment(
        loader=jinja2.FunctionLoader(load_func=lambda _: template),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return jinja_env.get_template("").render(context)
