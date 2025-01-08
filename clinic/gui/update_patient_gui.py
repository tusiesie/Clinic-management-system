import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QLineEdit, QHBoxLayout, QFormLayout
from clinic.exception.illegal_operation_exception import IllegalOperationException

class UpdatePatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.resize(400, 300)
        self.controller = controller
        self.cur_phn = None
        self.cur_name = None

        # search patient section
        layout1 = QHBoxLayout()
        self.label_search_phn = QLabel("PHN:")
        self.text_search_phn = QLineEdit()
        self.button_search = QPushButton("Search")

        layout1.addWidget(self.label_search_phn)
        layout1.addWidget(self.text_search_phn)
        layout1.addWidget(self.button_search)

        # current patient section
        layout2 = QHBoxLayout()
        self.label_cur = QLabel("Editing Patient with PHN:")
        self.text_cur = QLineEdit()

        layout2.addWidget(self.label_cur)
        layout2.addWidget(self.text_cur)
        # not for edit, just for information
        self.text_cur.setEnabled(False)

        # update section
        layout3 = QFormLayout()
        self.text_phn = QLineEdit()
        self.text_name = QLineEdit()
        self.text_birth = QLineEdit()
        self.text_phone = QLineEdit()
        self.text_email = QLineEdit()
        self.text_address = QLineEdit()

        layout3.addRow("Personal Health Number (PHN):", self.text_phn)
        layout3.addRow("Full Name:", self.text_name)
        layout3.addRow("Birth Date (YYY-MM-DD):", self.text_birth)
        layout3.addRow("Phone Number:", self.text_phone)
        layout3.addRow("Email:", self.text_email)
        layout3.addRow("Address:", self.text_address)

        # fields not editable until cur patient is set
        self.text_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_address.setEnabled(False)

        # update section
        layout4 = QHBoxLayout()
        self.button_back = QPushButton("Back")
        self.button_clear = QPushButton("Clear")
        self.button_update = QPushButton("Update")

        layout4.addWidget(self.button_back)
        layout4.addWidget(self.button_clear)
        layout4.addWidget(self.button_update)
        # update button not available until cur patient is set
        self.button_update.setEnabled(False)

        # set main layout
        layout5 = QVBoxLayout()

        # set sub layouts to be widgets
        widget1 = QWidget()
        widget1.setLayout(layout1)
        widget2 = QWidget()
        widget2.setLayout(layout2)
        widget3 = QWidget()
        widget3.setLayout(layout3)
        widget4 = QWidget()
        widget4.setLayout(layout4)

        # add widgets to main layout
        layout5.addWidget(widget1)
        layout5.addWidget(widget2)
        layout5.addWidget(widget3)
        layout5.addWidget(widget4)

        # Create a QWidget to act as a container for the layout
        main_widget = QWidget()
        main_widget.setLayout(layout5)
        self.setCentralWidget(main_widget)

        # connect the buttones' clicked to the slots below
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_update.clicked.connect(self.update_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_back.clicked.connect(self.back_button_clicked)

    def search_button_clicked(self):
        # get the input text
        phn = int(self.text_search_phn.text().strip())
        self.cur_phn = phn

        # set title for cur patient
        self.text_cur.setText(str(phn))

        # clear search field
        self.text_search_phn.clear()

        # get the current patient details according to searched phn
        try:
            cur_patient = self.controller.search_patient(phn)
            self.cur_name = cur_patient.name

            # input cur patient data into fields for user to reference
            self.text_phn.setText(str(cur_patient.phn))
            self.text_name.setText(cur_patient.name)
            self.text_birth.setText(cur_patient.birth_date)
            self.text_phone.setText(cur_patient.phone)
            self.text_email.setText(cur_patient.email)
            self.text_address.setText(cur_patient.address)

            # enable editing for the fields
            self.text_phn.setEnabled(True)
            self.text_name.setEnabled(True)
            self.text_birth.setEnabled(True)
            self.text_phone.setEnabled(True)
            self.text_email.setEnabled(True)
            self.text_address.setEnabled(True)

            # enable update button
            self.button_update.setEnabled(True)

        # patient does not exit
        except IllegalOperationException:
            QMessageBox.warning(self, "Error Getting Patient", "There is not patient registered with this PHN.")
            self.text_earch_phn.clear()

    def update_button_clicked(self):
        # show question box with options yes or no
        reply = QMessageBox.question(self, "Update Patient", "Are you sure you want to change patient data? %s" % self.cur_name, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:

            # get all information for patient update
            old_phn = self.cur_phn
            phn = self.text_phn.text().strip()
            name = self.text_name.text().strip()
            birth = self.text_birth.text().strip()
            phone = self.text_phone.text().strip()
            email = self.text_email.text().strip()
            address = self.text_address.text().strip()

            # makes sure all fields are filled out
            if phn == "" or name == "" or birth == "" or phone == "" or email == "" or email == "" or address == "":
                QMessageBox.warning(self, "Invalid Input", "All fields must be filled out")

            else:
                # update patient
                try:
                    self.controller.update_patient(old_phn, int(phn), name, birth, phone, email, address)
                    QMessageBox(self, "Update Successful", "Patient data changed.")
                    self.clear_button_clicked()
                    self.close()

                # new phn already exists in system
                except IllegalOperationException:
                    QMessageBox.warning(self, "Error Chaning Patient Data", "Cannot change the current patient data to a new PHN that is already registered in the system")
                    self.text_phn.clear()


    def clear_button_clicked(self):
        # clear each fields
        self.text_phn.clear()
        self.text_name.clear()
        self.text_birth.clear()
        self.text_phone.clear()
        self.text_email.clear()
        self.text_address.clear()

        # disable editing for the fields
        self.text_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_address.setEnabled(False)

        # disable update button
        self.button_update.setEnabled(False)

        # clear cur phn
        self.cur_phn = None
        self.text_cur.clear()

        # clear search
        self.text_search_phn.clear()

    def back_button_clicked(self):
        self.clear_button_clicked()
        self.close()
