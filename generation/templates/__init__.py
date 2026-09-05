from .template6 import template6, template6_back
from .template9 import template9, template9_back
from .kaascan_only import template_kaascan_only, template_kaascan_only_back

from .base import CardTemplate
from .registry import templates
# Registers "Template 6", "Template 9", and "Kaascan Only" into `templates`
# as a side effect - see legacy_adapters.py.
from . import legacy_adapters  # noqa: F401

__all__ = [
    "CardTemplate",
    "templates",
    "template6", "template6_back",
    "template9", "template9_back",
    "template_kaascan_only", "template_kaascan_only_back",
]
