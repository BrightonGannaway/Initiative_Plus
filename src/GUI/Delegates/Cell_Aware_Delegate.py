from PyQt6.QtWidgets import QStyledItemDelegate, QFrame, QVBoxLayout, QCheckBox, QStyle, QStyleOptionButton, QDialog
from PyQt6.QtCore import Qt, QRect
from constants import Constants

class Cell_Aware_Delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cell_delegates = {} # {(row, col): delegate}

    def register_delegate(self, row, col, delegate):
        self.cell_delegates[(row, col)] = delegate
    
    def paint(self, painter, option, index):
        delegate = self.cell_delegates.get((index.row(), index.column()), self)
        delegate.paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        delegate = self.cell_delegates.get((index.row(), index.column()), self)
        return delegate.editorEvent(event, model, option, index)
    
    #add more when needed