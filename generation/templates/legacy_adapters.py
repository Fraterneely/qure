"""Adapters exposing the pre-registry template functions through the
CardTemplate interface, so "Template 6", "Template 9", and "Kaascan Only" -
the three templates actually in use - are reachable via
`templates.get(name).render(...)` without changing their drawing code.

This is a migration aid, not the pattern to copy for a new template: a
template written against the registry from the start should just subclass
CardTemplate directly (see base.py) instead of wrapping a positional-arg
function like the ones below.
"""
from typing import Optional

from .base import CardTemplate
from .registry import templates
from .template6 import template6
from .template9 import template9
from .kaascan_only import template_kaascan_only


class _PositionalTemplate(CardTemplate):
    """Shared adapter for template6/template9, whose functions take an
    identical positional signature."""
    _func = None

    def render(self, gen, config: dict, cards_path: Optional[str] = None):
        return self._func(
            gen,
            self.name,
            config["primaryColor"],
            config["secondarColor"],
            config["school_logo"],
            config.get("school_stamp", ""),
            config["school_name"],
            config.get("school_slogan", ""),
            config.get("academic_year", ""),
            config.get("expiration_date", ""),
            config["student_photo"],
            config.get("school_phone", ""),
            config.get("school_email", ""),
            config.get("location", ""),
            config.get("website", ""),
            config.get("principal_name", ""),
            config.get("principal_phone", ""),
            config.get("principal_mail", ""),
            config.get("principal_signature", ""),
            cards_path,
        )


class _Template6(_PositionalTemplate):
    name = "Template 6"
    _func = staticmethod(template6)


class _Template9(_PositionalTemplate):
    name = "Template 9"
    _func = staticmethod(template9)


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


templates.add("Template 6", _Template6())
templates.add("Template 9", _Template9())
templates.add("Kaascan Only", _KaascanOnly())
