from __future__ import annotations
from PySide6.QtCore import QSettings

class Prefs:
    def __init__(self) -> None:
        self._s = QSettings()

    def get_click_color_hex(self) -> str:
        v = self._s.value("click_color", "#00A3FF", type=str)
        return v if isinstance(v, str) and v.startswith("#") and len(v) in (7, 9) else "#00A3FF"

    def set_click_color_hex(self, hex_color: str) -> None:
        if not isinstance(hex_color, str) or not hex_color.startswith("#") or len(hex_color) not in (7, 9):
            return
        self._s.setValue("click_color", hex_color)
        self._s.sync()
