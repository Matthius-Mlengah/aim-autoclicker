from __future__ import annotations
from pathlib import Path
import sys
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QStackedWidget
from .config import RADIUS, TITLEBAR_HEIGHT, ORG_NAME, APP_NAME
from .ui.chrome import Chrome
from .ui.titlebar import TitleBar
from .ui.overlay_menu import OverlayMenu
from .ui.pages import HomePage, SettingsPage
from .ui.style import load_stylesheet
from .ui.color_picker import ScreenColorPicker
from .state.prefs import Prefs

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

        self.pages = QStackedWidget()
        self.prefs = Prefs()
        self.home = HomePage()
        self.settings = SettingsPage(self.prefs)
        self.pages.addWidget(self.home)
        self.pages.addWidget(self.settings)
        inner.addWidget(self.pages)
        outer.addWidget(self.chrome)

        self.overlay = OverlayMenu(self.chrome)
        self.overlay.setTopOffset(self.titlebar.height())
        self.overlay.setActive("home")
        self.overlay.navigate.connect(self._navigate)
        self.titlebar.menuRequested.connect(self._toggle_menu)

        self.settings.screen_pick_requested.connect(self._start_screen_pick)

        qss_path = Path(__file__).parent / "ui" / "styles.qss"
        qss = load_stylesheet(str(qss_path), RADIUS=RADIUS, TITLEBAR_HEIGHT=TITLEBAR_HEIGHT)
        self.setStyleSheet(qss)

    def _toggle_menu(self) -> None:
        self.overlay.setTopOffset(self.titlebar.height())
        self.overlay.setVisible(not self.overlay.isVisible())
        if self.overlay.isVisible():
            self.overlay.raise_()

    def _navigate(self, route: str) -> None:
        if route == "home":
            self.pages.setCurrentWidget(self.home)
        elif route == "settings":
            self.pages.setCurrentWidget(self.settings)
        self.overlay.setActive(route)
        self.overlay.hide()

    def _start_screen_pick(self) -> None:
        picker = ScreenColorPicker()
        picker.selected = lambda hexc: self.settings.apply_external_color(hexc)
        picker.canceled = lambda: None
        picker.show()

def run() -> None:
    QCoreApplication.setOrganizationName(ORG_NAME)
    QCoreApplication.setApplicationName(APP_NAME)
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec())
