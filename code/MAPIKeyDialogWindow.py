from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit
import qrcode



class MAPIKeyDialogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        confirmation_buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(confirmation_buttons)
        self.buttonBox.accepted.connect(self.ok_clicked)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()
        message = QLabel("Enter the name of API Key owner")
        self.input_box = QLineEdit()
        self.layout.addWidget(message, 0, 0)
        self.layout.addWidget(self.input_box, 1, 0)
        self.layout.addWidget(self.buttonBox, 2, 0)
        self.setLayout(self.layout)

    def ok_clicked(self):
        username = self.input_box.text()
        filename = "api_key_qr.png"
        img = qrcode.make(username)
        img.save(filename)
        self.accept()


