from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from main_code.LogInfo import LogInfo


class LogCustomQWidget(QWidget):
    def __init__(self, parent=None):
        super(LogCustomQWidget, self).__init__(parent)
        textQVBox = QVBoxLayout()
        self.log_text = QLabel()
        self.time_label = QLabel()
        self.icon = QLabel()
        self.id = 0
        textQVBox.addWidget(self.log_text)
        textQVBox.addWidget(self.time_label)

        self.allQHBoxLayout = QHBoxLayout()
        self.icon.setFixedSize(25, 25)
        self.allQHBoxLayout.addLayout(textQVBox, 1)
        self.allQHBoxLayout.addWidget(self.icon, 0)
        self.setLayout(self.allQHBoxLayout)

    def mouseDoubleClickEvent(self, event):
        self.window = LogInfo(self.id)
        self.window.show()


    def setText(self, text):
        self.log_text.setText(text)

    def setIcon(self, text):
        pass

    def setTime(self,text):
        self.time_label.setText(text)
        font = QFont()

    def setId(self, integer):
        self.id = integer