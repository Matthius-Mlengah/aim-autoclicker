from __future__ import annotations
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy

class OverlayMenu(QWidget):
    navigate = Signal(str)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("Overlay")
        self.setVisible(False)
        self.setAttribute(Qt.WA_StyledBackground, True)   # paint dim background
        self._top_offset = 0

        self.drawer = QWidget(self)
        self.drawer.setObjectName("Drawer")
        self.drawer.setAttribute(Qt.WA_StyledBackground, True)  # enable rounded clipping

        col = QVBoxLayout(self.drawer)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(0)
        col.setAlignment(Qt.AlignTop)

        self.btn_home = self._item("Home")
        self.btn_settings = self._item("Settings")
        col.addWidget(self.btn_home)
        col.addWidget(self.btn_settings)

        self.btn_home.clicked.connect(lambda: self._go("home"))
        self.btn_settings.clicked.connect(lambda: self._go("settings"))

    def _item(self, text: str) -> QPushButton:
        b = QPushButton(text)
        b.setObjectName("DrawerItem")
        b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        b.setMinimumHeight(36)
        return b

    def setTopOffset(self, px: int) -> None:
        self._top_offset = max(0, int(px))
        self.updateGeometry()
        self.update()

    def setActive(self, route: str) -> None:
        self.btn_home.setProperty("active", route == "home")
        self.btn_settings.setProperty("active", route == "settings")
        for w in (self.btn_home, self.btn_settings):
            w.style().unpolish(w)
            w.style().polish(w)

    def resizeEvent(self, _) -> None:
        p = self.parentWidget()
        if not p:
            return
        self.setGeometry(0, self._top_offset, p.width(), p.height() - self._top_offset)
        w = max(220, int(self.width() * 0.28))
        self.drawer.setGeometry(QRect(0, 0, w, self.height()))

    def mousePressEvent(self, e) -> None:
        if not self.drawer.geometry().contains(e.position().toPoint()):
            self.hide()

    def show(self) -> None:
        super().show()
        self.raise_()

    def _go(self, route: str) -> None:
        self.hide()
        self.navigate.emit(route)
