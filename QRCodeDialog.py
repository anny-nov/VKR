from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class QRCodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        confirmation_button = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(confirmation_button)
        self.buttonBox.accepted.connect(self.accept)

        text = QLabel("QRCode for user is created. Please scan it before closing the window.")
        text.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        image = QLabel()
        image.setPixmap(QPixmap('api_key_qr.png'))
        image.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(text)
        self.layout.addWidget(image)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)