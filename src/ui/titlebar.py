from __future__ import annotations
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QSizePolicy, QToolButton, QWidget
)
from ..config import TITLEBAR_HEIGHT, CLOSE_WIDTH, BTN_WIDTH

class TitleBar(QWidget):
    def __init__(self, host: QWidget) -> None:
        super().__init__()
        self.host = host
        self._drag = QPoint()
        self.setFixedHeight(TITLEBAR_HEIGHT)

        row = QHBoxLayout(self)
        row.setContentsMargins(12, 0, 0, 0)
        row.setSpacing(0)

        self.title = QLabel("AutoClicker")
        self.title.setObjectName("Title")

        self.min_btn = self._btn("−", "MinBtn", BTN_WIDTH)
        self.max_btn = self._btn("▢", "MaxBtn", BTN_WIDTH)
        self.close_btn = self._btn("×", "CloseBtn", CLOSE_WIDTH)

        self.min_btn.clicked.connect(self.host.showMinimized)
        self.max_btn.setEnabled(False)
        self.close_btn.clicked.connect(self.host.close)

        row.addWidget(self.title)
        row.addStretch(1)
        row.addWidget(self.min_btn)
        row.addWidget(self.max_btn)
        row.addWidget(self.close_btn)

    def _btn(self, text: str, name: str, width: int) -> QToolButton:
        b = QToolButton(self)
        b.setText(text)
        b.setObjectName(name)
        b.setFocusPolicy(Qt.NoFocus)
        b.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        b.setMinimumWidth(width)
        return b

    def paintEvent(self, _) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(QColor("#C7CCD6"))
        p.drawLine(0, self.height() - 1, self.width(), self.height() - 1)

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.LeftButton:
            self._drag = e.globalPosition().toPoint() - self.host.frameGeometry().topLeft()
            e.accept()

    def mouseMoveEvent(self, e) -> None:
        if e.buttons() & Qt.LeftButton:
            self.host.move(e.globalPosition().toPoint() - self._drag)
            e.accept()
