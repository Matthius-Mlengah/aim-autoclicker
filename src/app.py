from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy
from .config import RADIUS, TITLEBAR_HEIGHT
from .ui.chrome import Chrome
from .ui.titlebar import TitleBar
from .ui.style import load_stylesheet_pkg

class App(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(0)

        self.chrome = Chrome()
        inner = QVBoxLayout(self.chrome)
        inner.setContentsMargins(0, 0, 0, 16)
        inner.setSpacing(0)

        self.titlebar = TitleBar(self)
        inner.addWidget(self.titlebar)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(24, 24, 24, 0)
        body_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("Primary")
        self.start_btn.setMinimumSize(200, 56)
        body_layout.addWidget(self.start_btn, alignment=Qt.AlignHCenter)

        body_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        inner.addWidget(body)
        outer.addWidget(self.chrome)

        qss = load_stylesheet_pkg("src.ui", "styles.qss", RADIUS=RADIUS, TITLEBAR_HEIGHT=TITLEBAR_HEIGHT)
        self.setStyleSheet(qss)

def run() -> None:
    import sys
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec())
