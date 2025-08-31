from __future__ import annotations
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QGuiApplication, QColor
from PySide6.QtWidgets import QWidget
from typing import Optional

class ScreenColorPicker(QWidget):
    selected = None  # Signal-like callbacks set by caller
    canceled = None

    def __init__(self) -> None:
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        geom = QGuiApplication.primaryScreen().virtualGeometry()
        self.setGeometry(geom)

    def _sample_at(self, p: QPoint) -> Optional[QColor]:
        screen = QGuiApplication.screenAt(p)
        if not screen:
            return None
        geo = screen.geometry()
        px = screen.grabWindow(0, p.x() - geo.x(), p.y() - geo.y(), 1, 1)
        if px.isNull():
            return None
        img = px.toImage()
        return QColor(img.pixel(0, 0))

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.LeftButton:
            c = self._sample_at(e.globalPosition().toPoint())
            if c:
                hexc = c.name(QColor.HexArgb if c.alpha() < 255 else QColor.HexRgb)
                if callable(self.selected):
                    self.selected(hexc)
            self.close()
            return
        if e.button() == Qt.RightButton and callable(self.canceled):
            self.canceled()
            self.close()

    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_Escape and callable(self.canceled):
            self.canceled()
            self.close()
