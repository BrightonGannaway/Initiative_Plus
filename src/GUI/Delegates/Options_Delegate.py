from PyQt6.QtWidgets import (QStyledItemDelegate, QFrame, QVBoxLayout, QCheckBox, 
                             QStyle, QStyleOptionButton, QDialog,
                            QRadioButton, QButtonGroup, QHBoxLayout, QGroupBox, QScrollArea,
                            QWidget, QPushButton)
from PyQt6.QtCore import Qt, QRect, pyqtSignal, pyqtBoundSignal, QSizeF, QEvent, pyqtSlot
from PyQt6.QtGui import QTextDocument, QAbstractTextDocumentLayout, QPixmap
from constants import Constants
from controller import Controller

class Options_Delegate(QStyledItemDelegate):

    emitted_value = pyqtSignal(int, list)
    emitted_value_with_sub_options = pyqtSignal(int, dict)

    def __init__(self, parent=None, icon=None, options=None, use_html_display=False, sub_options=None, option_tooltips=None):
        super().__init__(parent)
        self.arrow_width = 16
        self.global_index = 0
        self.arrow_Button = QStyleOptionButton()
        self.controller = Controller()
        self.options_checked = []
        self.icon = icon 
        self.options = options or []
        self.saved_options = []
        self.sub_options = sub_options or []
        self.sub_options_checked = {}
        self.saved_sub_options = {}
        self.button_group_dict = {}
        self.option_tooltips = option_tooltips or {}
        self.use_html_display = use_html_display
    

    
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
        
        if isinstance(self.icon, QPixmap):
            option.widget.style().drawItemPixmap(painter, arrow_rect, Qt.AlignmentFlag.AlignCenter, self.icon.scaled(self.arrow_width, self.arrow_width))
            return
        option.widget.style().drawPrimitive(self.icon or QStyle.PrimitiveElement.PE_IndicatorSpinPlus , self.arrow_Button, painter)

        if self.use_html_display:
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
    

    def eventFilter(self, object, event):
        if object == self.options_Scroll_Area:
            if event.type() == QEvent.Type.WindowDeactivate:
                 self.close_Popup()
                 self.popup = None
        return super().eventFilter(object, event)
    
    
    def show_Popup(self, option, model, index):
        self.options_checked.clear()

        self.popup = None
        if self.popup:
            self.popup.close()

        self.options_Scroll_Area = None
        if self.options_Scroll_Area:
                self.options_Scroll_Area.close()
        
        self.popup = QFrame(option.widget.parent()) 
        self.popup.setWindowFlags(Qt.WindowType.Popup) 
        self.popup.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        layout = QVBoxLayout(self.popup) 

        self.scroll_Area = QScrollArea(option.widget.parent())
        self.scroll_Area.setWidget(self.popup)
        self.scroll_Area.setWidgetResizable(True)
        

        #popup positioning below cell
        rect = option.widget.visualRect(index)
        global_pos = option.widget.mapToGlobal(rect.bottomRight())

        popup_width = 150
        popup_height = len(self.options) * 25

        # Position popup just under the cell, aligned to right edge
        # popup_x = global_pos.x() 
        # popup_y = global_pos.y()
        popup_x = rect.bottomRight().x()
        popup_y = rect.bottomRight().y()

        # self.popup.setGeometry(popup_x, popup_y, popup_width, popup_height) -OP
        # self.popup.move(popup_x - popup_width, popup_y) -OP
        self.scroll_Area.setGeometry(popup_x, popup_y, popup_width * 3 if self.sub_options else popup_width, popup_height)
        self.scroll_Area.move(popup_x - popup_width, popup_y)
        
        self.saved_options = [s.strip() for s in self.saved_options] if self.saved_options else []
        
        
        for option in self.options:
            if len(self.sub_options) <= 1:
                checkbox = QRadioButton(option)
                checkbox.setAutoExclusive(False)
                if (self.option_tooltips):
                    checkbox.setToolTip(self.option_tooltips[option])
                checkbox.setChecked(option.strip().lower() in [s.lower() for s in self.saved_options])
                self.options_checked.append(checkbox)
                layout.addWidget(checkbox) 
            else:
                box_group = QGroupBox(option)
                button_Group = QButtonGroup()
                button_Group.setExclusive(False)
                button_layout = QHBoxLayout()
                button_list = []
                for sub_option in self.sub_options:
                    sub_checkbox = QRadioButton(sub_option)
                    sub_checkbox.setAutoExclusive(True)
                    sub_checkbox.setChecked(option in self.saved_sub_options.keys() and self.saved_sub_options[option] == sub_option)
                    button_Group.addButton(sub_checkbox)
                    self.button_group_dict[sub_checkbox] = button_Group
                    sub_checkbox.toggled.connect(self.uncheck_excluded_buttons)
                    button_layout.addWidget(sub_checkbox)
                    button_list.append(sub_checkbox)
                self.sub_options_checked[option] = button_list
                box_group.setLayout(button_layout)
                layout.addWidget(box_group)
        
        

        # self.popup.focusOutEvent = self.close_Popup -OP

        self.popup.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.scroll_Area.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.scroll_Area.viewport().setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.scroll_Area.setFocus()
        self.popup.setFocus()
        self.scroll_Area.show()

        #fixed an issue where 
        self.popup.focusOutEvent = self.close_Popup
    
    @pyqtSlot(bool)
    def uncheck_excluded_buttons(self, toggled_state:bool):
        button_target = self.sender()

        if isinstance(button_target, QRadioButton):
            button_Group = self.button_group_dict.get(button_target)
            for button in button_Group.buttons():
                if button.isChecked() and button is not button_target:
                    button.setChecked(False)
        
            if toggled_state: button_target.setChecked(True) 
            
            


    def emit_selection(self):
        self.emitted_value.emit(self.global_index.row(), self.saved_options)
    
    def emit_selections_with_sub_options(self):
        self.emitted_value_with_sub_options.emit(self.global_index.row(), self.saved_sub_options)

    def set_saved_options(self, options=[], sub_options={}):
        self.saved_options = options
        self.saved_sub_options = sub_options

            


    #saves options and closes
    def close_Popup(self, event):
        if self.scroll_Area.hasFocus():
            return
        self.saved_options.clear()
        self.saved_options = [option.text() for option in self.options_checked if option.isChecked()]
       
        #create saved dictionary for sub items
        self.saved_sub_options.clear()
        for option, sub_options in self.sub_options_checked.items():
            for sub_op in sub_options:
                if sub_op.isChecked():
                    self.saved_sub_options[option] = sub_op.text()
                    break
        #clear other data 
        self.button_group_dict.clear()

        self.emit_selection()
        self.emit_selections_with_sub_options()
        self.popup.close()
        self.scroll_Area.close()

    def get_selected(self):
        return self.saved_options        