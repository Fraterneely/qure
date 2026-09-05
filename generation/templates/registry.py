"""Registry mapping template names to CardTemplate instances.

Replaces the closed if/elif dispatch that used to live entirely in
CGenerator.create_student_card: registering a template - via `register` as
a class decorator, or `add` for an already-built instance - is enough to
make it reachable by name. core.py no longer needs to be edited to add one.
"""
from typing import Dict, List

from .base import CardTemplate


class TemplateRegistry:
    def __init__(self) -> None:
        self._templates: Dict[str, CardTemplate] = {}

    def register(self, name: str):
        """Class decorator: `@templates.register("My Template")`."""
        def decorator(cls):
            self._templates[name] = cls()
            return cls
        return decorator

    def add(self, name: str, template: CardTemplate) -> None:
        """Register an already-constructed template instance directly."""
        self._templates[name] = template

    def get(self, name: str) -> CardTemplate:
        try:
            return self._templates[name]
        except KeyError:
            raise ValueError(
                f"Invalid template name: {name!r}. Available: {sorted(self._templates)}"
            ) from None

    def list(self) -> List[str]:
        return sorted(self._templates)


templates = TemplateRegistry()
