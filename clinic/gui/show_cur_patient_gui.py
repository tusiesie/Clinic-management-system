import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QFormLayout
from PyQt6.QtCore import Qt

class ShowCurPatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("List Patient")
        self.resize(600, 300)

        # create all components
        self.text_phn = QLineEdit()
        self.text_name = QLineEdit()
        self.text_birth = QLineEdit()
        self.text_phone = QLineEdit()
        self.text_email = QLineEdit()
        self.text_address = QLineEdit()
        self.button_back = QPushButton("Back")

        # set upper layout
        layout1 = QFormLayout()
        layout1.addRow("Personal Health Number (PHN):", self.text_phn)
        layout1.addRow("Full Name:", self.text_name)
        layout1.addRow("Birth Date (YYY-MM-DD):", self.text_birth)
        layout1.addRow("Phone Number:", self.text_phone)
        layout1.addRow("Email:", self.text_email)
        layout1.addRow("Address:", self.text_address)

        # fields not editable until cur patient is set
        self.text_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_address.setEnabled(False)

        # set sub layout as widget
        widget1 = QWidget()
        widget1.setLayout(layout1)

        # set main layout
        layout2 = QVBoxLayout()
        layout2.addWidget(widget1)
        layout2.addWidget(self.button_back)

        # create a main widget to act as a container for main layout
        widget2 = QWidget()
        widget2.setLayout(layout2)
        self.setCentralWidget(widget2)

        # connect button clicked signal to slot below
        self.button_back.clicked.connect(self.back_button_clicked)

    def list_patient(self, phn):
        patient = self.controller.search_patient(phn)

        self.text_phn.setText(str(patient.phn))
        self.text_name.setText(patient.name)
        self.text_birth.setText(patient.birth_date)
        self.text_phone.setText(patient.phone)
        self.text_email.setText(patient.email)
        self.text_address.setText(patient.address)

    def back_button_clicked(self):
        self.close()

    def closeEvent(self, event):
        self.back_button_clicked()
