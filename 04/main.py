import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QCheckBox
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

API_KEY_STATIC = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'


class MainWindow(QMainWindow):
    g_map: QLabel
    press_delta = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('main_window.ui', self)

        self.map_zoom = 10
        self.map_ll = [37.977751, 55.757718]
        self.map_key = ''
        self.is_dark_theme = False

        self.toggle_theme_checkbox = self.findChild(QCheckBox, 'toggleTheme')

        self.toggle_theme_checkbox.stateChanged.connect(self.toggle_theme)

        self.refresh_map()
        self.apply_theme()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            if self.map_zoom < 17:
                self.map_zoom += 1
        elif key == Qt.Key.Key_PageDown:
            if self.map_zoom > 0:
                self.map_zoom -= 1
        elif key == Qt.Key.Key_Right:
            self.map_ll[0] += self.press_delta
            if self.map_ll[0] > 180:
                self.map_ll[0] = self.map_ll[0] - 360
        elif key == Qt.Key.Key_Left:
            self.map_ll[0] -= self.press_delta
            if self.map_ll[0] < 0:
                self.map_ll[0] = self.map_ll[0] + 360
        elif key == Qt.Key.Key_Up:
            if self.map_ll[1] + self.press_delta < 90:
                self.map_ll[1] += self.press_delta
        elif key == Qt.Key.Key_Down:
            if self.map_ll[1] - self.press_delta > -90:
                self.map_ll[1] -= self.press_delta
        else:
            return

        self.refresh_map()

    def toggle_theme(self):
        self.is_dark_theme = self.toggle_theme_checkbox.isChecked()
        self.refresh_map()
        self.apply_theme()

    def refresh_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            'z': self.map_zoom,
            'apikey': API_KEY_STATIC,
        }

        if self.is_dark_theme:
            map_params['theme'] = 'dark'
        else:
            map_params['theme'] = 'light'

        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get('https://static-maps.yandex.ru/v1',
                               params=map_params)
        img = QImage.fromData(response.content)
        pixmap = QPixmap.fromImage(img)
        self.g_map.setPixmap(pixmap)

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2e2e2e;
                }
                QLabel {
                    color: white;
                }
                QCheckBox {
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: white;
                }
                QLabel {
                    color: black;
                }
                QCheckBox {
                    color: black;
                }
            """)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
