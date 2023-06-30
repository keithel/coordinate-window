import sys
import signal
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QGuiApplication, QCursor


class CoordWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        self._label = QLabel(self)
        self._label.setStyleSheet("QLabel { color: white; font: bold 16px; }")
        self._layout.addWidget(self._label)

        self._long_interval = 1000
        self._short_interval = 16
        self._no_move_count = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._updateCoordinates)
        self._timer.start(self._short_interval)
        self._last_screen_pos = None

    def mouseMoveEvent(self, event):
        self._updateCoordinates()

    def _updateCoordinates(self):
        global_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(global_pos)
        if screen:
            screen_pos = screen.geometry().topLeft()
            local_pos = global_pos - screen_pos
            self._label.setText(f"Mouse coordinates: ({local_pos.x()}, {local_pos.y()})")

            if self._timer.interval != self._long_interval and self._last_screen_pos is not None and self._last_screen_pos == local_pos:
                self._no_move_count += 1
            elif self._timer.interval() != self._short_interval:
                self._timer.setInterval(self._short_interval)
            else:
                self._no_move_count = 0

            if self._no_move_count > self._long_interval / self._short_interval:
                self._no_move_count = 0
                self._timer.setInterval(self._long_interval)

            self._last_screen_pos = local_pos


def sigint_handler(signal, frame):
    sys.exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    app = QApplication(sys.argv)

    window = CoordWindow()
    window.setGeometry(0, 0, 200, 50)
    window.show()

    sys.exit(app.exec())

