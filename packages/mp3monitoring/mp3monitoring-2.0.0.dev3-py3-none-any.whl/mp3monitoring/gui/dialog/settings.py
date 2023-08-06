from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from mp3monitoring.core.manager import Manager
from mp3monitoring.core.settings import Settings, save_config
from mp3monitoring.gui.ui.settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, settings: Settings, manager: Manager, parent):
        super().__init__(parent)

        self._manager: Manager = manager
        self._settings: Settings = settings

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~(Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint))

        self.start_minimized.setChecked(self._settings.start_minimized)
        self.start_with_system.setChecked(self._settings.start_with_system)
        # TODO:
        self.start_with_system.setEnabled(False)

        self.button_box.accepted.connect(self.apply)
        self.button_box.rejected.connect(self.cancel)

    def apply(self):
        self._settings.start_minimized = self.start_minimized.isChecked()

        save_config(self._settings, self._manager.get_configurations())

        self.close()

    def cancel(self):
        self.close()
