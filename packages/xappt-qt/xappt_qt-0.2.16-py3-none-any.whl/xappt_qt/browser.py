import os
import platform
import sys


from PyQt5 import QtWidgets, QtGui, QtCore

import xappt

import xappt_qt.config
from xappt_qt.gui.ui.browser import Ui_Browser
from xappt_qt.gui.utilities.dark_palette import apply_palette
from xappt_qt.gui.utilities.tray_icon import TrayIcon
from xappt_qt.constants import *
from xappt_qt.gui.tab_pages import ToolsTabPage, OptionsTabPage, AboutTabPage

# noinspection PyUnresolvedReferences
from xappt_qt.gui.resources import icons

DISABLE_TRAY_ICON = platform.system() == "Darwin"


class XapptBrowser(xappt.ConfigMixin, QtWidgets.QMainWindow, Ui_Browser):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":appicon"))
        self.setWindowTitle(APP_TITLE)

        self.tray_icon = TrayIcon(self, QtGui.QIcon(":appicon"))
        self.init_tray_icon()

        self.tools = ToolsTabPage(on_info=self.tray_icon.info, on_warn=self.tray_icon.warn,
                                  on_error=self.tray_icon.critical)
        self.options = OptionsTabPage()
        self.about = AboutTabPage()

        self.tabWidget.addTab(self.tools, self.tools.windowTitle())
        self.tabWidget.addTab(self.options, self.options.windowTitle())
        self.tabWidget.addTab(self.about, self.about.windowTitle())
        self.tabWidget.setCurrentIndex(0)

        self.config_path = APP_CONFIG_PATH.joinpath("browser.cfg")
        self.init_config()
        self.load_config()

    def init_config(self):
        self.add_config_item('launch-new-process',
                             saver=lambda: xappt_qt.config.launch_new_process,
                             loader=lambda x: setattr(xappt_qt.config, "launch_new_process", x),
                             default=True)
        self.add_config_item('minimize-to-tray',
                             saver=lambda: xappt_qt.config.minimize_to_tray,
                             loader=lambda x: setattr(xappt_qt.config, "minimize_to_tray", x),
                             default=True)
        self.add_config_item('window-size',
                             saver=lambda: (self.width(), self.height()),
                             loader=lambda x: self.setGeometry(0, 0, *x),
                             default=(350, 600))
        self.add_config_item('window-position',
                             saver=lambda: (self.geometry().x(), self.geometry().y()),
                             loader=lambda x: self.set_window_position(*x),
                             default=(-1, -1))
        if DISABLE_TRAY_ICON:
            self.options.chkMinimizeToTray.setChecked(False)
            self.options.chkMinimizeToTray.setEnabled(False)
            xappt_qt.config.minimize_to_tray = False

    def init_tray_icon(self):
        if DISABLE_TRAY_ICON:
            return
        self.tray_icon.add_menu_item("Show", self.show, self.isHidden)
        self.tray_icon.add_menu_item("Hide", self.hide, self.isVisible)
        self.tray_icon.add_menu_item(None, None, None)
        self.tray_icon.add_menu_item("Quit", self.on_quit, None)
        self.tray_icon.on_trigger = self.on_activate
        self.tray_icon.show()

    def set_window_position(self, x: int, y: int):
        if x < 0 or y < 0:
            app = QtWidgets.QApplication.instance()
            cursor_pos = QtGui.QCursor.pos()
            screen = app.screenAt(cursor_pos)

            screen_rect = screen.availableGeometry()
            window_rect = QtCore.QRect(QtCore.QPoint(0, 0), self.frameSize().boundedTo(screen_rect.size()))
            self.resize(window_rect.size())
            self.move(screen_rect.center() - window_rect.center())
        else:
            self.move(x, y)

    def changeEvent(self, event: QtCore.QEvent):
        if not DISABLE_TRAY_ICON:
            if event.type() == QtCore.QEvent.WindowStateChange:
                if self.windowState() == QtCore.Qt.WindowMinimized:
                    if xappt_qt.config.minimize_to_tray and self.tray_icon.tray_available:
                        self.hide()
        super().changeEvent(event)

    def closeEvent(self, event: QtGui.QCloseEvent):
        if xappt_qt.config.minimize_to_tray and self.tray_icon.tray_available:
            event.ignore()
            self.hide()
        else:
            self.on_quit()

    def on_activate(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def on_quit(self):
        self.tray_icon.destroy()
        self.save_config()
        QtWidgets.QApplication.instance().quit()


def main(args) -> int:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(args)
    apply_palette(app)

    browser = XapptBrowser()
    browser.show()

    app.setProperty(APP_PROPERTY_RUNNING, True)
    return app.exec_()


def entry_point() -> int:
    os.environ[xappt.INTERFACE_ENV] = APP_INTERFACE_NAME
    return main(sys.argv)


if __name__ == '__main__':
    sys.exit(entry_point())
