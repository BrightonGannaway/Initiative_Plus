from PyQt6.QtWidgets import QStyledItemDelegate, QFrame, QVBoxLayout, QCheckBox, QStyle, QStyleOptionButton, QDialog
from PyQt6.QtCore import Qt, QRect, pyqtSignal, pyqtBoundSignal, QSizeF
from PyQt6.QtGui import QTextDocument, QAbstractTextDocumentLayout
from constants import Constants
from controller import Controller

class Options_Delegate(QStyledItemDelegate):

    emmited_value = pyqtSignal(int, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.arrow_width = 16
        self.global_index = 0
        self.arrow_Button = QStyleOptionButton()
        self.controller = Controller()
        self.checkboxes = []
        self.saved_conditions = [] 
    

    
    #draws dropdown arrow for UI
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        self.global_index = index

        # Draw dropdown arrow (▼)
        style = option.widget.style()
        arrow_rect = QRect(option.rect.right() - self.arrow_width, option.rect.top(), self.arrow_width, option.rect.height())

        self.arrow_Button = QStyleOptionButton()
        self.arrow_Button.rect = arrow_rect
        self.arrow_Button.state = QStyle.StateFlag.State_Enabled
        option.widget.style().drawPrimitive(QStyle.PrimitiveElement.PE_IndicatorSpinPlus, self.arrow_Button, painter)

        painter.save()
        document = QTextDocument()
        document.setHtml(index.data(Qt.ItemDataRole.UserRole))
        document.setDefaultFont(Constants.Fonts.kCell_Display)
        document.setPageSize(QSizeF(option.rect.size()))
        context = QAbstractTextDocumentLayout.PaintContext()
        painter.translate(option.rect.x(), option.rect.y())
        document.documentLayout().draw(painter, context)
        painter.restore()




    #upon mouse click, show popup
    def editorEvent(self, event, model, option, index):

        arrow_rect = QRect(option.rect.right() - self.arrow_width, option.rect.top(), self.arrow_width, option.rect.height())

        if event.type() == event.Type.MouseButtonPress and arrow_rect.contains(event.pos()):
            self.current_index = index
            self.show_Popup(option, model, index)
            return True
        return super().editorEvent(event, model, option, index)
    
    def show_Popup(self, option, model, index):
        self.checkboxes.clear()
        self.popup = None
        if self.popup:
            self.popup.close()
        
        self.popup = QFrame(option.widget.parent())
        self.popup.setWindowFlags(Qt.WindowType.Popup)
        self.popup.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        layout = QVBoxLayout(self.popup)

        #popup positioning below cell
        rect = option.widget.visualRect(index)
        global_pos = option.widget.mapToGlobal(rect.bottomRight())
        popup_x = global_pos.x()
        popup_y = global_pos.y()
        popup_width = 150
        popup_height = len(Constants.Properties.kConditions) * 25
        self.popup.setGeometry(popup_x, popup_y, popup_width, popup_height)
        self.popup.move(popup_x - popup_width, popup_y)
        
        self.saved_conditions = [s.strip() for s in self.saved_conditions] if self.saved_conditions else []
        
        
        for condition in Constants.Properties.kConditions:
            checkbox = QCheckBox(condition)
            checkbox.setChecked(condition.strip().lower() in [s.lower() for s in self.saved_conditions])
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.popup.setFocus()
        self.popup.show()

        self.popup.focusOutEvent = self.close_Popup

    def emit_conditions(self):
        self.emmited_value.emit(self.global_index.row(), self.saved_conditions)
    
    def set_saved_conditions(self, conditions):
        self.saved_conditions = conditions

    #saves options and closes
    def close_Popup(self, event):
        self.saved_conditions.clear()
        self.saved_conditions = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        #self.parent().model().setData(self.current_index, ", ".join(self.saved_conditions), Qt.ItemDataRole.EditRole)
        #self.controller.delegate_options_call(Constants.Delegate_Options.kConditions_Command_Call, self.global_index.row(), self.saved_conditions)
        self.emit_conditions()
        self.popup.close()

    def get_selected(self):
        return self.saved_conditions


        