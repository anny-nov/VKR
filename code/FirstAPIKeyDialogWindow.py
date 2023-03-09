from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit


class FirstAPIKeyDialogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        confirmation_buttons = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(confirmation_buttons)
        self.buttonBox.accepted.connect(self.ok_clicked)

        self.layout = QGridLayout()
        message = QLabel("Welcome! Enter your first API Key")
        self.input_box = QLineEdit()
        self.layout.addWidget(message, 0, 0)
        self.layout.addWidget(self.input_box, 1, 0)
        self.layout.addWidget(self.buttonBox, 2, 0)
        self.setLayout(self.layout)

    def ok_clicked(self):
        key = self.input_box.text()
        if len(key)>0:
            file = open('../api_key', 'w')
            file.write(key)
            self.accept()
        else:
            pass

    def closeEvent(self, event):
        event.ignore()