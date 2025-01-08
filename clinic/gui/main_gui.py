import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox

from clinic.gui.add_patient_gui import AddPatientGUI
from clinic.gui.search_patient_gui import SearchPatientGUI
from clinic.gui.retrieve_patients_gui import RetrievePatientsGUI
from clinic.gui.list_all_gui import ListAllGUI
from clinic.gui.update_patient_gui import UpdatePatientGUI
from clinic.gui.delete_patient_gui import DeletePatientGUI
from clinic.gui.start_appointment_gui import StartAppointmentGUI
from clinic.gui.appointment_menu_gui import AppointmentMenuGUI

class MainGUI(QMainWindow):
    # signal to notify logout
    logout_signal = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.resize(500, 400)
        self.controller = controller

        # set layout type
        layout = QVBoxLayout()

        # add sub windows
        self.add_patient_gui = AddPatientGUI(self.controller)
        self.search_patient_gui = SearchPatientGUI(self.controller)
        self.retrieve_patients_gui = RetrievePatientsGUI(self.controller)
        self.list_all_gui = ListAllGUI(self.controller)
        self.update_patient_gui = UpdatePatientGUI(self.controller)
        self.delete_patient_gui = DeletePatientGUI(self.controller)
        self.start_appointment_gui = StartAppointmentGUI(self.controller)
        self.appointment_menu_gui = AppointmentMenuGUI(self.controller)

        # create buttons
        self.button_add_patient = QPushButton("Add New Patient")
        self.button_search_patient = QPushButton("Search Patient by PHN")
        self.button_retrieve_patients = QPushButton("Retrieve Patients by Name")
        self.button_update_patient = QPushButton("Change Patient Data")
        self.button_remove_patient = QPushButton("Remove Patient")
        self.button_list_all = QPushButton("List All Patients")
        self.button_start_appointment = QPushButton("Start Appointment with Patient")
        self.button_logout = QPushButton("Log Out")

        # set constant button width size
        button_width = self.width() // 1.5
        self.button_add_patient.setFixedWidth(button_width)
        self.button_search_patient.setFixedWidth(button_width)
        self.button_retrieve_patients.setFixedWidth(button_width)
        self.button_update_patient.setFixedWidth(button_width)
        self.button_remove_patient.setFixedWidth(button_width)
        self.button_list_all.setFixedWidth(button_width)
        self.button_start_appointment.setFixedWidth(button_width)
        self.button_logout.setFixedWidth(button_width)

        # add buttons to layout
        layout.addWidget(self.button_add_patient)
        layout.addWidget(self.button_search_patient)
        layout.addWidget(self.button_retrieve_patients)
        layout.addWidget(self.button_update_patient)
        layout.addWidget(self.button_remove_patient)
        layout.addWidget(self.button_list_all)
        layout.addWidget(self.button_start_appointment)
        layout.addWidget(self.button_logout)

        # Create a QWidget to act as a container for the layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # connect the buttons' clicked to the slots below
        self.button_add_patient.clicked.connect(self.add_patient)
        self.button_search_patient.clicked.connect(self.search_patient)
        self.button_retrieve_patients.clicked.connect(self.retrieve_patients)
        self.button_list_all.clicked.connect(self.list_all)
        self.button_update_patient.clicked.connect(self.update_patient)
        self.button_remove_patient.clicked.connect(self.delete_patient)
        self.button_logout.clicked.connect(self.logout_button_clicked)
        self.button_start_appointment.clicked.connect(self.start_appointment)

    def add_patient(self):
        self.add_patient_gui.show()

    def search_patient(self):
        self.search_patient_gui.show()

    def retrieve_patients(self):
        self.retrieve_patients_gui.show()

    def list_all(self):
        self.list_all_gui.show()

    def update_patient(self):
        self.update_patient_gui.show()

    def delete_patient(self):
        self.delete_patient_gui.show()

    def start_appointment(self):
        self.start_appointment_gui.app_started.connect(self.start_appointment_menu)
        self.start_appointment_gui.show()

    def start_appointment_menu(self):
        # if appointment menu gives appointment finished signal, show again
        self.appointment_menu_gui.app_finished.connect(self.show_again)
        # show appointement menu
        self.appointment_menu_gui.show()
        self.hide()

    def show_again(self):
        self.show()

    def logout_button_clicked(self):
        # message box that has yes or no options
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # yest button clicked
        if reply == QMessageBox.StandardButton.Yes:
            # emit logout signal to clinic_gui.py
            self.logout_signal.emit()
            self.controller.logout()
            self.close()
