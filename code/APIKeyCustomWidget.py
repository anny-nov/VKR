from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton


class QKeyCustomQWidget(QWidget):
    def __init__(self, parent=None):
        super(QKeyCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.ClientName = QLabel()
        self.KeyType = QLabel()
        self.textQVBoxLayout.addWidget(self.ClientName)
        self.textQVBoxLayout.addWidget(self.KeyType)

        self.allQHBoxLayout = QHBoxLayout()
        self.more_info_button = QPushButton("More info")
        self.more_info_button.clicked.connect(self.clicked)
        self.more_info_button.setFixedSize(100, 30)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 0)
        self.allQHBoxLayout.addWidget(self.more_info_button, 1)
        self.setLayout(self.allQHBoxLayout)

    def setClientName(self, text):
        self.ClientName.setText(text)

    def setKeyType(self, text):
        self.KeyType.setText(text)
        self.KeyType.setStyleSheet('color: rgb(120, 120, 120);')

    def setButtonName(self, text):
        self.more_info_button.setObjectName(str(text))

    def clicked(self):
        pass
        #sender = self.sender()
        #self.window = ComputerInfoWindow(sender.objectName())
        #self.window.show()