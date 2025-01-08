import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QTableView, QHBoxLayout, QLineEdit
from clinic.gui.patient_table_model import PatientTableModel
from clinic.gui.show_cur_patient_gui import ShowCurPatientGUI

class RetrievePatientsGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Retrieve Patient")
        self.resize(650, 700)
        self.controller = controller

        # add subwindow
        self.show_cur_patient_gui = ShowCurPatientGUI(self.controller)

        # create table view and components
        self.patient_table = QTableView()
        self.patient_model = PatientTableModel()
        self.patient_table.setModel(self.patient_model)
        self.label_name = QLabel("Name:")
        self.text_name = QLineEdit()
        self.button_search = QPushButton("Search")
        self.button_clear = QPushButton("Clear")
        self.button_back = QPushButton("Back")

        # add components to layout 1
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label_name)
        layout1.addWidget(self.text_name)
        layout1.addWidget(self.button_search)

        # add components to layout 2
        layout2 = QHBoxLayout()
        layout2.addWidget(self.button_back)
        layout2.addWidget(self.button_clear)

        # make other layouts as widget to add to main layout
        widget1 = QWidget()
        widget1.setLayout(layout1)
        widget2 = QWidget()
        widget2.setLayout(layout2)

        # setup of main layout
        layout3 = QVBoxLayout()
        layout3.addWidget(self.patient_table)
        layout3.addWidget(widget1)
        layout3.addWidget(widget2)
        layout3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # create a main QWidget to act as a container for the layout
        widget = QWidget()
        widget.setLayout(layout3)
        self.setCentralWidget(widget)

        # connect the buttons' clicked signals to the slots below
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
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

    def search_button_clicked(self):
        # get input string
        name = self.text_name.text().strip()

        # get list of patients with given name
        patient_list = self.controller.retrieve_patients(name)

        # clear all fields before showing data
        self.clear_button_clicked()

        if not patient_list:
            # no patients that match the given name
            QMessageBox.warning(self, "Invalid Entry", "No patients found with name %s" % name)
        else:
            # show retrieved data
            self.patient_model.search_patient(patient_list)
            self.patient_table.setEnabled(True)


    def clear_button_clicked(self):
        self.patient_model.reset()
        self.text_name.clear()
        self.patient_table.setEnabled(False)


    def back_button_clicked(self):
        self.show_cur_patient_gui.close()
        self.close()
