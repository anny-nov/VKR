from PyQt6.QtWidgets import QWidget
from ui_send import Ui_Form as form

class Widget(QWidget, form):
    def __init__(self):
        super(Widget, self).__init__()
        QWidget.__init__(self)
        self.setupUi(self)