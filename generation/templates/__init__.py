from .template1 import template1, template1_back
from .template2 import template2, template2_back
from .template3 import template3
from .template4 import template4, template4_back
from .template5 import template5, template5_back
from .template6 import template6, template6_back
from .template7 import template7, template7_back
from .template8 import template8
from .template9 import template9, template9_back
from .kaascan_only import template_kaascan_only, template_kaascan_only_back

from .base import CardTemplate
from .registry import templates
# Registers "Template 1" and "Kaascan Only" into `templates` as a side effect;
# see legacy_adapters.py for why those two and not the rest, for now.
from . import legacy_adapters  # noqa: F401

# Lookup used by CGenerator.create_student_card to validate a requested template
# name and find its front-side function. Only templates actually wired into the
# dispatcher are listed here; template7/template8 exist (see their modules) but
# have never been reachable through create_student_card.
TEMPLATES = {
    "Template 1": template1,
    "Template 2": template2,
    "Template 3": template3,
    "Template 4": template4,
    "Template 5": template5,
    "Template 6": template6,
    "Template 9": template9,
    "Kaascan Only": template_kaascan_only,
}

__all__ = [
    "TEMPLATES",
    "CardTemplate",
    "templates",
    "template1", "template1_back",
    "template2", "template2_back",
    "template3",
    "template4", "template4_back",
    "template5", "template5_back",
    "template6", "template6_back",
    "template7", "template7_back",
    "template8",
    "template9", "template9_back",
    "template_kaascan_only", "template_kaascan_only_back",
]
