from PyQt6.QtWidgets import (
    QStyledItemDelegate, QWidget, QHBoxLayout, QPushButton,
    QSpinBox, QTableWidget, QTableWidgetItem, QFrame, QComboBox, 
    QVBoxLayout )

from PyQt6.QtCore import Qt, QRect, QEvent, pyqtSignal, QModelIndex
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QApplication
from constants import Constants

class Damage_Delegate(QStyledItemDelegate):

    emitted_value_damage = pyqtSignal(int, str, int)
    emitted_value_heal = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.global_index = QModelIndex()

    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseButtonPress:
            self.show_Popup(option, model, index)
            return True
        return super().editorEvent(event, model, option, index)
    
    def show_Popup(self, option, model, index):
        self.global_index = index
        self.popup = None

        if self.popup:
            self.popup.close()

        #creates a popup widget
        self.popup = QFrame(option.widget.window())
        self.popup.setWindowFlag(Qt.WindowType.Popup)
        self.popup.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)

        #popup position right near cell
        rect = option.widget.visualRect(index)
        global_pos = option.widget.mapToGlobal(rect.topLeft())
        popup_width = 130
        popup_height = 70
        popup_x = global_pos.x()
        popup_y = global_pos.y() - popup_height
        self.popup.resize(popup_width, popup_height)
        self.popup.setGeometry(popup_x, popup_y, popup_width, popup_height)
        
        layout = QHBoxLayout(self.popup)

        box_layout = QVBoxLayout()
        button_layout = QVBoxLayout()
        self.minus_button = QPushButton("-")
        self.minus_button.setFixedSize(popup_width // 4, popup_height // 3)
        self.plus_button = QPushButton("+")
        self.plus_button.setFixedSize(popup_width // 4, popup_height // 3)

        self.spin_box = QSpinBox()
        self.spin_box.setRange(-999, 999)
        self.spin_box.setValue(0) 
        self.spin_box.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.spin_box.setFocus()
        self.spin_box.setFixedSize(popup_width // 2, popup_height // 3)

        self.damage_Type_Box = QComboBox()
        self.damage_Type_Box.addItems(Constants.Properties.KDamage_Types)
        self.damage_Type_Box.setFocus()
        self.damage_Type_Box.setFixedSize(popup_width // 2, popup_height // 4)

        button_layout.addWidget(self.minus_button, alignment=Qt.AlignmentFlag.AlignTop)
        button_layout.addWidget(self.plus_button, alignment=Qt.AlignmentFlag.AlignBottom)
        box_layout.addWidget(self.spin_box, alignment=Qt.AlignmentFlag.AlignRight)
        box_layout.addWidget(self.damage_Type_Box, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(button_layout)
        layout.addLayout(box_layout)


        
        self.popup.show()
        self.popup.setFocus() #make it focus so that it can detect when focus is lost

        def eventFilter(obj, event):
            """Closes the popup when clicking outside of it."""
            if event.type() == QEvent.Type.MouseButtonPress and self.popup:
                if isinstance(event, QMouseEvent):
                    if not self.popup.geometry().contains(event.globalPosition().toPoint()):
                        self.popup.close()
                        QApplication.instance().removeEventFilter(self)
            return super().eventFilter(obj, event)

        def closePopupOnFocusLoss(event):
            if self.spin_box.hasFocus() or self.plus_button.hasFocus() or self.minus_button.hasFocus() or self.damage_Type_Box.hasFocus():
                event.ignore()
                return
            self.popup.close()
            event.accept() #ensure event is handles correctly

        def endSpinBoxFocus(event):
            if self.popup.hasFocus() or self.damage_Type_Box.hasFocus():
                event.ignore()
                return
            self.popup.close()
            event.accept()
        
        def endDamageTypeBox(event):
            if self.popup.hasFocus() or self.spin_box.hasFocus() or self.popup.isActiveWindow():
                event.ignore()
                return
            self.damage_Type_Box.close()
            event.accept()
        
        

        self.popup.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.popup.focusOutEvent = closePopupOnFocusLoss
        self.spin_box.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.spin_box.focusOutEvent = endSpinBoxFocus
        self.damage_Type_Box.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.damage_Type_Box.focusOutEvent = endDamageTypeBox

        #applies damage by finding cell hp
        def get_Current_HP():
            current_hp = model.data(index, Qt.ItemDataRole.DisplayRole)
            try:
                current_hp = int(current_hp)
                return current_hp
            except (ValueError, TypeError):
                current_hp = 0 #default
                return current_hp

        #multiuplying by factors of 2 for some reason 
        def apply_damage():
            self.emit_damage()

        #multiplying by factors of -3 for some reason
        def heal():
            self.emit_heal()

        self.minus_button.clicked.connect(apply_damage)
        self.plus_button.clicked.connect(heal)
            
    def emit_damage(self):
        self.emitted_value_damage.emit(self.global_index.row(), self.damage_Type_Box.currentText(), self.spin_box.value())

    def emit_heal(self):
        self.emitted_value_heal.emit(self.global_index.row(), self.spin_box.value())


#TODO: 2 bugs -> plus minus don't damage or heal but merely replace. Once spinwheel clicked QFrame thinks focus is still on spinwheel and thus popup doesnt close



