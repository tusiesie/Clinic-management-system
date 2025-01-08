import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QGridLayout, QLabel, QLineEdit
from clinic.exception.illegal_operation_exception import IllegalOperationException

class AddPatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Add Patient")
        self.resize(400, 300)
        self.controller = controller

        # create components
        self.label_phn = QLabel("Personal Health Number (PHN)")
        self.text_phn = QLineEdit()
        self.label_name = QLabel("Full Name")
        self.text_name = QLineEdit()
        self.label_birth = QLabel("Bith Date (YYY-MM-DD)")
        self.text_birth = QLineEdit()
        self.label_phone = QLabel("Phone Number")
        self.text_phone = QLineEdit()
        self.label_email = QLabel("Email")
        self.text_email = QLineEdit()
        self.label_address = QLabel("Address")
        self.text_address = QLineEdit()
        self.button_add = QPushButton("Add Patient")
        self.button_back = QPushButton("Back")
        self.button_clear = QPushButton("Clear")

        # set upper layout type
        layout1 = QGridLayout()

        # add compondents to upper layout
        layout1.addWidget(self.label_phn, 0, 0)
        layout1.addWidget(self.text_phn, 0, 1)
        layout1.addWidget(self.label_name, 1, 0)
        layout1.addWidget(self.text_name, 1, 1)
        layout1.addWidget(self.label_birth, 2, 0)
        layout1.addWidget(self.text_birth, 2, 1)
        layout1.addWidget(self.label_phone, 3, 0)
        layout1.addWidget(self.text_phone, 3, 1)
        layout1.addWidget(self.label_email, 4, 0)
        layout1.addWidget(self.text_email, 4, 1)
        layout1.addWidget(self.label_address, 5, 0)
        layout1.addWidget(self.text_address, 5, 1)
        layout1.addWidget(self.button_clear, 6, 0)
        layout1.addWidget(self.button_add, 6, 1)

        # create main layout
        layout2 = QVBoxLayout()

        # configure main layout
        top_widget = QWidget()
        top_widget.setLayout(layout1)
        layout2.addWidget(top_widget)
        layout2.addWidget(self.button_back)

        # Create a QWidget to act as a container for the layout
        widget = QWidget()
        widget.setLayout(layout2)
        self.setCentralWidget(widget)

        # connect the buttons' clicked signals to the slots below
        self.button_add.clicked.connect(self.add_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_back.clicked.connect(self.back_button_clicked)

    def add_button_clicked(self):
        phn = self.text_phn.text().strip()
        name = self.text_name.text().strip()
        birth = self.text_birth.text().strip()
        phone = self.text_phone.text().strip()
        email = self.text_email.text().strip()
        address = self.text_address.text().strip()

        # one or more field is empty
        if phn == "" or name == "" or birth == "" or phone == "" or email == "" or address == "":
            QMessageBox.warning(self, "Invalid Input", "All fields must be filled out")
        else:

            try:
                # add patient to the system
                self.controller.create_patient(int(phn), name, birth, phone, email, address)
                QMessageBox.information(self, "Add Patient Successful", "Successfully added a new patient")
                self.clear_button_clicked()
                self.close()

            except IllegalOperationException:
                # phn already exists in system
                QMessageBox.warning(self, "Invalid Input", "Cannot add patient with a PHN taht is already registered")
                self.text_phn.clear()

    def clear_button_clicked(self):
        self.text_phn.clear()
        self.text_name.clear()
        self.text_birth.clear()
        self.text_phone.clear()
        self.text_email.clear()
        self.text_address.clear()

    def back_button_clicked(self):
        self.close()
