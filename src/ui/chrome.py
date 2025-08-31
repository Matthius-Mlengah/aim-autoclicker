from __future__ import annotations
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QSizePolicy, QWidget
from ..config import RADIUS

class Chrome(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        eff = QGraphicsDropShadowEffect(self)
        eff.setBlurRadius(24)
        eff.setOffset(0, 6)
        eff.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(eff)

    def sizeHint(self) -> QSize:
        return QSize(560, 360)

    def paintEvent(self, _) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), RADIUS, RADIUS)
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor("#F7F8FA"))
        grad.setColorAt(1.0, QColor("#ECEFF3"))
        p.fillPath(path, grad)
