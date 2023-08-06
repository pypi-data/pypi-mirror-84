from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget


class SpinAnimation(QWidget):
    def __init__(self, parent=None, background_color=QColor(255, 255, 255, 255), rotate_color=QColor(255, 113, 0, 255)):
        super().__init__(parent)

        self._timer = None
        self._degree = 0

        self.circle_width = 0.3
        self.rotate_length = 5760 / 360 * 42
        self.speed = 12  # 1/16 _degree
        self.background_color = background_color
        self.rotate_color = rotate_color

    def radius(self):
        return min(self.width(), self.height()) / 2

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        x_mid, y_mid = self.get_middle_point(self.radius())

        # background circle
        radius = self.radius()
        pen = QPen()
        pen.setWidth(self.radius() * self.circle_width)
        pen.setColor(self.background_color)
        painter.setPen(pen)
        painter.drawArc(x_mid, y_mid, radius, radius, 0, 5760)

        # rotate circle
        pen.setColor(self.rotate_color)
        painter.setPen(pen)
        painter.drawArc(x_mid, y_mid, radius, radius, -self._degree, self.rotate_length)

    def showEvent(self, event):
        self._timer = self.startTimer(5)
        self._degree = 0

    def timerEvent(self, event):
        self._degree = (self._degree + self.speed) % 5760
        self.update()

    def get_middle_point(self, outer_radius):
        return self.width() / 2 - outer_radius / 2, self.height() / 2 - outer_radius / 2
