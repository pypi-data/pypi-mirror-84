from PyQt5.QtCore import QObject, pyqtSignal

from mp3monitoring.core.signal._signal_no_qt import Signal as SignalNQ


class Signal(SignalNQ, QObject):
    _s: pyqtSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def connect(self, callback):
        self._s.connect(callback)

    def disconnect(self):
        try:
            self._s.disconnect()
        except Exception:
            pass

    def emit(self, idx: int):
        self._s.emit(idx)
