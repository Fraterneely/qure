"""Adapters exposing the pre-registry template functions through the
CardTemplate interface, so "Template 1" and "Kaascan Only" are reachable
via `templates.get(name).render(...)` without changing their drawing code.

This is a migration aid, not the pattern to copy for a new template: a
template written against the registry from the start should just subclass
CardTemplate directly (see base.py) instead of wrapping a positional-arg
function like the ones below.
"""
from typing import Optional

from .base import CardTemplate
from .registry import templates
from .template1 import template1
from .kaascan_only import template_kaascan_only


class _Template1(CardTemplate):
    name = "Template 1"

    def render(self, gen, config: dict, cards_path: Optional[str] = None):
        return template1(
            gen,
            self.name,
            config["primaryColor"],
            config["secondarColor"],
            config["school_logo"],
            config["school_name"],
            config.get("school_slogan", ""),
            config.get("academic_year", ""),
            config.get("expiration_date", ""),
            config["student_photo"],
            cards_path,
        )


class _KaascanOnly(CardTemplate):
    name = "Kaascan Only"

    def render(self, gen, config: dict, cards_path: Optional[str] = None):
        return template_kaascan_only(
            gen,
            self.name,
            config["primaryColor"],
            config["secondarColor"],
            config.get("academic_year", ""),
            config.get("expiration_date", ""),
            config["student_photo"],
            config["school_name"],
            cards_path,
        )


templates.add("Template 1", _Template1())
templates.add("Kaascan Only", _KaascanOnly())
