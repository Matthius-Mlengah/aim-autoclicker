from __future__ import annotations
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout,
    QSizePolicy, QLineEdit
)
from ..state.prefs import Prefs

class HomePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 0)
        root.addStretch(1)
        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("Primary")
        self.start_btn.setMinimumSize(200, 56)
        root.addWidget(self.start_btn, alignment=Qt.AlignHCenter)
        root.addStretch(1)

class SettingsPage(QWidget):
    color_changed = Signal(str)
    screen_pick_requested = Signal()

    def __init__(self, prefs: Prefs) -> None:
        super().__init__()
        self._prefs = prefs
        self._hex = self._prefs.get_click_color_hex()

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)

        row = QHBoxLayout()
        self.pick_screen = QPushButton("Pick Screen Color")
        self.preview = QLabel()
        self.preview.setObjectName("ColorSwatch")
        self.preview.setFixedSize(40, 24)
        self.preview.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.hex_box = QLineEdit()
        self.hex_box.setObjectName("HexBox")
        self.hex_box.setReadOnly(True)
        self.hex_box.setFixedWidth(110)

        row.addWidget(self.pick_screen)
        row.addWidget(self.preview)
        row.addWidget(self.hex_box)
        row.addStretch(1)
        root.addLayout(row)
        root.addStretch(1)

        self._apply_preview()
        self.pick_screen.clicked.connect(lambda: self.screen_pick_requested.emit())

    def apply_external_color(self, hex_color: str) -> None:
        if not isinstance(hex_color, str) or not hex_color.startswith("#"):
            return
        self._hex = hex_color
        self._prefs.set_click_color_hex(self._hex)
        self._apply_preview()
        self.color_changed.emit(self._hex)

    def _apply_preview(self) -> None:
        self.preview.setStyleSheet(
            f"background: {self._hex}; border: 1px solid #C9CDD3; border-radius: 4px;"
        )
        self.hex_box.setText(self._hex)
