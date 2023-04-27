from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from ComputerInfoWindow import ComputerInfoWindow


class QCustomQWidget(QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.ComputerName = QLabel()
        self.ComputerStatus = QLabel()
        self.textQVBoxLayout.addWidget(self.ComputerName)
        self.textQVBoxLayout.addWidget(self.ComputerStatus)

        self.allQHBoxLayout = QHBoxLayout()
        self.comp_iconQLabel = QLabel()
        self.comp_iconQLabel.setMinimumSize(80, 80)
        self.comp_iconQLabel.setMaximumSize(80, 80)
        self.more_info_button = QPushButton("More info")
        self.more_info_button.clicked.connect(self.clicked)
        self.more_info_button.setFixedSize(100, 30)
        self.allQHBoxLayout.addWidget(self.comp_iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.allQHBoxLayout.addWidget(self.more_info_button, 2)
        self.setLayout(self.allQHBoxLayout)

    def setComputerName(self, text):
        self.ComputerName.setText(text)

    def setComputerStatus(self, status):
        if status == 1:
            self.ComputerStatus.setText('Active')
            self.ComputerStatus.setStyleSheet('color: rgb(3, 192, 60);')
        else:
            self.ComputerStatus.setText('Inactive')
            self.ComputerStatus.setStyleSheet('color: rgb(255, 0, 0);')

    def setIcon(self):
        self.comp_iconQLabel.setPixmap(QPixmap('../computer_icon.png'))

    def setButtonName(self, text):
        self.more_info_button.setObjectName(str(text))

    def clicked(self):
        sender = self.sender()
        self.window = ComputerInfoWindow(sender.objectName())
        self.window.show()