"""Jinja2 wrapper."""
from typing import Any, Dict

import jinja2


def render_jinja(template: str, context: Dict[str, Any]) -> str:
    """Render the input jinja string using the context and return it."""
    jinja_env = jinja2.Environment(
        loader=jinja2.FunctionLoader(load_func=lambda _: template),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return jinja_env.get_template("").render(context)
