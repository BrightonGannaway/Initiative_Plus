from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

class Error_Popup(QMessageBox):
    def __init__(self, parent=None, title="Error", message="An error occured"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Icon.Warning)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setDefaultButton(QMessageBox.StandardButton.Ok)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def show_popup(self):
        self.exec()


