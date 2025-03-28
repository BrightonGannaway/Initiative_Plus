from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QLabel

#Picture Button Implementation
class Clickable_Image(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_object = None
        self.connected_method = None
        self.setScaledContents(True)
    
    def setPixmap(self, pixmap, width=None, height=None):
        super().setPixmap(pixmap)
        self.pixmap_object = pixmap
        if width and height:
            self.setFixedSize(width, height)
        print("added pixmap")

    def mousePressEvent(self, event: QMouseEvent):
        if self.connected_method:
            self.connected_method()

    def connect(self, method):
        self.connected_method = method