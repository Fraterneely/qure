"""Base interface for pluggable card templates.

A template renders one record's card (front and back - the back side
generally needs data only available while the front is built, e.g. a
QR-code payload or a shared color palette) and saves both sides.

`gen` is the CGenerator instance for the current record: `gen.data` holds
the arbitrary per-record fields (e.g. Firstname, Trade, Department) and
`gen` exposes the shared drawing helpers (load_fonts, generate_qr_code,
save_double_sided_card, lighten_color, ...). `config` holds the
template-facing options that used to be individual positional arguments -
primaryColor, school_name, academic_year, and so on - so a template only
needs to read the keys it actually uses instead of matching a fixed
parameter list shared by every other template.
"""
from typing import Optional


class CardTemplate:
    name: str

    def render(self, gen, config: dict, cards_path: Optional[str] = None):
        """Render and save both sides of the card.

        Returns whatever the underlying save step returns - today that's a
        (front_path, back_path) tuple, matching CGenerator.create_student_card.
        """
        raise NotImplementedError
