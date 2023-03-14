import json

import requests
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QCheckBox, QComboBox
import qrcode

API_KEY = 'TZPP8LaSPoYCAU6iTtDnWA'

class APIKeyDialogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.security_descriptor = None
        self.name = None
        self.type = "user"

        confirmation_buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(confirmation_buttons)
        self.buttonBox.accepted.connect(self.ok_clicked)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()
        name_label = QLabel("Enter the name of API Key owner")
        self.name_input_box = QLineEdit()

        type_label = QLabel("Select key user type")
        type_list = QComboBox()
        type_list.addItems(["desktop_operator", "mobile_operator", "user"])
        type_list.textActivated.connect(self.type_select)

        params_label = QLabel("Select the set of rights that the key grants:")
        comps_label = QLabel("Computers")
        self.comp_read = QCheckBox("Read")
        self.comp_update = QCheckBox("Update")
        self.comp_add = QCheckBox("Add")
        self.comp_delete = QCheckBox("Delete")

        client_label = QLabel("API Keys")
        self.client_read = QCheckBox("Read")
        self.client_update = QCheckBox("Update")
        self.client_add = QCheckBox("Add")
        self.client_delete = QCheckBox("Delete")

        logs_label = QLabel("Logs")
        self.log_read = QCheckBox("Read")
        self.log_update = QCheckBox("Update")
        self.log_add = QCheckBox("Add")
        self.log_delete = QCheckBox("Delete")

        checkbox_layout = QGridLayout()
        checkbox_layout.addWidget(comps_label, 0, 0)
        checkbox_layout.addWidget(client_label, 0, 1)
        checkbox_layout.addWidget(logs_label, 0, 2)
        checkbox_layout.addWidget(self.client_read, 1, 1)
        checkbox_layout.addWidget(self.client_update, 2, 1)
        checkbox_layout.addWidget(self.client_add, 3, 1)
        checkbox_layout.addWidget(self.client_delete, 4, 1)
        checkbox_layout.addWidget(self.comp_read, 1, 0)
        checkbox_layout.addWidget(self.comp_update, 2, 0)
        checkbox_layout.addWidget(self.comp_add, 3, 0)
        checkbox_layout.addWidget(self.comp_delete, 4, 0)
        checkbox_layout.addWidget(self.log_read, 1, 2)
        checkbox_layout.addWidget(self.log_update, 2, 2)
        checkbox_layout.addWidget(self.log_add, 3, 2)
        checkbox_layout.addWidget(self.log_delete, 4, 2)

        self.layout.addWidget(name_label, 0, 0)
        self.layout.addWidget(self.name_input_box, 1, 0)
        self.layout.addWidget(type_label, 2, 0)
        self.layout.addWidget(type_list, 3, 0)
        self.layout.addWidget(params_label, 4, 0)
        self.layout.addLayout(checkbox_layout, 5, 0)
        self.layout.addWidget(self.buttonBox, 6, 0)
        self.setLayout(self.layout)

    def ok_clicked(self):
        self.name = self.name_input_box.text()
        self.security_descriptor = self.form_descriptor()
        self.create_client()
        filename = "api_key_qr.png"
        img = qrcode.make(self.name)
        img.save(filename)
        self.accept()

    def create_client(self):
        url = 'http://46.151.30.76:5000?api_key=' + API_KEY
        client_json_dict = {"id": 0,
                            "name": self.name,
                            "api_key": "",
                            "type": self.type,
                            "security_descriptor": self.security_descriptor}
        request = json.dumps(client_json_dict)
        page = requests.post(url, json=request, verify=False)
        print(page)
        return page

    def type_select(self, text):
        self.type = text

    def form_descriptor(self):
        desc_string = ""
        if self.comp_read.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.comp_update.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.comp_add.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.comp_delete.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        desc_string += ":"

        if self.client_read.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.client_update.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.client_add.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.client_delete.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        desc_string += ":"

        if self.log_read.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.log_update.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.log_add.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        if self.log_delete.isChecked():
            desc_string += "1"
        else:
            desc_string += "0"
        return desc_string
