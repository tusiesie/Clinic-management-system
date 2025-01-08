import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableView
from clinic.gui.patient_table_model import PatientTableModel
from clinic.gui.show_cur_patient_gui import ShowCurPatientGUI

class ListAllGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("List All Patients")
        self.resize(650, 700)
        self.controller = controller

        # add subwindow
        self.show_cur_patient_gui = ShowCurPatientGUI(self.controller)

        # create table view and components
        self.patient_table = QTableView()
        self.patient_model = PatientTableModel()
        self.patient_table.setModel(self.patient_model)
        self.button_back = QPushButton("Back")

        # setup of layout
        layout = QVBoxLayout()
        layout.addWidget(self.patient_table)
        layout.addWidget(self.button_back)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # create a main QWidget to act as a container for the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # trigger the table view or button clicked
        self.button_back.clicked.connect(self.back_button_clicked)

        # connect the double click signal to allow storing the current patient
        self.current_patient_phn = None
        self.patient_table.doubleClicked.connect(self.list_patient_requested)

    def list_patient_requested(self):
        index = self.patient_table.selectionModel().currentIndex()
        # get the phn
        self.current_patient_phn = int(index.sibling(index.row(), 0).data())
        self.show_cur_patient_gui.list_patient(self.current_patient_phn)
        self.show_cur_patient_gui.show()

    def showEvent(self, event):
        '''Called when the window is shown'''
        super().showEvent(event)  # Ensure the parent class's showEvent is called
        self.on_window_opened()  # Call the custom method

    def on_window_opened(self):
        '''Custom method triggered when the window is opened'''
        self.show_table()

    def show_table(self):
        # get list of all patients
        patient_list = self.controller.list_patients()

        # no patients in system
        if not patient_list:
            QMessageBox.warning(self, "Invalid Entry", "No patients registered in the clinic")
            self.button_back_clicked()
        else:
            self.patient_model.search_patient(patient_list)
            self.patient_table.setEnabled(True)

    def back_button_clicked(self):
        # clear table
        self.patient_table.reset()
        self.patient_table.setEnabled(False)
        self.show_cur_patient_gui.close()
        self.close()
