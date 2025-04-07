from PyQt6.QtWidgets import QStyledItemDelegate, QFrame, QVBoxLayout, QCheckBox, QStyle, QStyleOptionButton, QDialog
from PyQt6.QtCore import Qt, QRect
from constants import Constants

class Options_Delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.arrow_width = 16
        self.arrow_Button = QStyleOptionButton()
        self.checkboxes = []
        self.saved_conditions = [] 
    

    
    #draws dropdown arrow for UI
    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        # Draw dropdown arrow (▼)
        style = option.widget.style()
        arrow_rect = QRect(option.rect.right() - self.arrow_width, option.rect.top(), self.arrow_width, option.rect.height())

        self.arrow_Button = QStyleOptionButton()
        self.arrow_Button.rect = arrow_rect
        self.arrow_Button.state = QStyle.StateFlag.State_Enabled
        option.widget.style().drawPrimitive(QStyle.PrimitiveElement.PE_IndicatorSpinPlus, self.arrow_Button, painter)

    #upon mouse click, show popup
    def editorEvent(self, event, model, option, index):

        arrow_rect = QRect(option.rect.right() - self.arrow_width, option.rect.top(), self.arrow_width, option.rect.height())

        if event.type() == event.Type.MouseButtonPress and arrow_rect.contains(event.pos()):
            self.current_index = index
            self.show_Popup(option, model, index)
            return True
        return super().editorEvent(event, model, option, index)
    
    def show_Popup(self, option, model, index):
        print("Loading conditions: ", self.saved_conditions)
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
        popup_height = len(Constants.Proporties.kConditions) * 25
        self.popup.setGeometry(popup_x, popup_y, popup_width, popup_height)
        self.popup.move(popup_x - popup_width, popup_y)
        
        self.saved_conditions = [s.strip() for s in self.saved_conditions] if self.saved_conditions else []
        
        
        for condition in Constants.Proporties.kConditions:
            checkbox = QCheckBox(condition)
            checkbox.setChecked(condition.strip().lower() in [s.lower() for s in self.saved_conditions])
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.popup.setFocus()
        self.popup.show()

        self.popup.focusOutEvent = self.close_Popup

    #saves options and closes
    def close_Popup(self, event):
        print(self.checkboxes)
        print(f"Length of checkboxes: {len(self.checkboxes)}")
        self.saved_conditions.clear()
        print("Should be clear -> ", self.saved_conditions)
        self.saved_conditions = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        print(self.saved_conditions)
        self.parent().model().setData(self.current_index, ", ".join(self.saved_conditions), Qt.ItemDataRole.EditRole)
        self.popup.close()

        