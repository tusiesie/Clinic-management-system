import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QGridLayout, QLabel, QLineEdit, QHBoxLayout

class SearchPatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.resize(400, 300)
        self.controller = controller

        # set layout type of upper half
        layout1 = QGridLayout()

        # create layout1 components
        self.label_phn = QLabel("PHN")
        self.text_phn = QLineEdit()
        self.label_name = QLabel("Full Name")
        self.text_name = QLineEdit()
        self.label_birth = QLabel("Birth Date (YYY-MM-DD)")
        self.text_birth = QLineEdit()
        self.label_phone = QLabel("Phone Number")
        self.text_phone = QLineEdit()
        self.label_email = QLabel("Email")
        self.text_email = QLineEdit()
        self.label_address = QLabel("Address")
        self.text_address = QLineEdit()

        # add compondents to the first layout
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

        # create a second layout for phn searching
        layout2 = QHBoxLayout()

        # create layout2 components
        self.label_search_phn = QLabel("Personal Health Number (PHN):")
        self.text_search_phn = QLineEdit()

        # add components to layout2
        layout2.addWidget(self.label_search_phn)
        layout2.addWidget(self.text_search_phn)


        # create layout 3
        layout3 = QHBoxLayout()

        # create layout 3 components
        self.button_clear = QPushButton("Clear")
        self.button_back = QPushButton("Back")
        self.button_search = QPushButton("Search")

        # add components to layout 3
        layout3.addWidget(self.button_back)
        layout3.addWidget(self.button_clear)
        layout3.addWidget(self.button_search)

        # set main layout
        layout4 = QVBoxLayout()

        # layout all widgets and set layout4 main widget
        widget1 = QWidget()
        widget2 = QWidget()
        widget3 = QWidget()
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)
        widget3.setLayout(layout3)

        # add widget to main layout
        layout4.addWidget(widget1)
        layout4.addWidget(widget2)
        layout4.addWidget(widget3)

        # Create a QWidget to act as a container for the layout
        main_widget = QWidget()
        main_widget.setLayout(layout4)
        self.setCentralWidget(main_widget)

        # define widgets initial state
        self.text_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_address.setEnabled(False)

        # connect the buttons' clicked signals to the slots below
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_back.clicked.connect(self.back_button_clicked)

    def clear_button_clicked(self):
        self.text_search_phn.clear()
        self.text_phn.clear()
        self.text_name.clear()
        self.text_birth.clear()
        self.text_phone.clear()
        self.text_email.clear()
        self.text_address.clear()

    def search_button_clicked(self):
        # get the inputed phn
        phn = self.text_search_phn.text().strip()

        # get patient with the corresponding phn
        patient = self.controller.search_patient(int(phn))

        if patient:
            # get fields
            name = patient.name
            birth = patient.birth_date
            phone = patient.phone
            email = patient.email
            address = patient.address

            # show results
            self.text_phn.setText(phn)
            self.text_name.setText(name)
            self.text_birth.setText(birth)
            self.text_phone.setText(phone)
            self.text_email.setText(email)
            self.text_address.setText(address)
            self.text_search_phn.clear()

        else:
            # no patient with given phn
            QMessageBox.warning(self, "Invalid PHN", "No patient with that PHN found")
            self.clear_button_clicked()

    def back_button_clicked(self):
        self.close()
