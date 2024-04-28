from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment
import jinjax


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
        }
    )

    env.add_extension(jinjax.JinjaX)
    catalog = jinjax.Catalog(jinja_env=env)

    catalog.add_folder("templates/components")

    return env
