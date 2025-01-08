import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class StartAppointmentGUI(QMainWindow):
    app_started = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Start Appointment")
        self.controller = controller

        # create all components
        label_phn = QLabel("Personal Health Number (PHN): ")
        self.text_phn = QLineEdit()
        self.button_back = QPushButton("Back")
        self.button_start = QPushButton("Start")
        self.button_clear = QPushButton("Clear")

        # create upper layout
        layout1 = QHBoxLayout()
        layout1.addWidget(label_phn)
        layout1.addWidget(self.text_phn)

        # create lower layout
        layout2 = QHBoxLayout()
        layout2.addWidget(self.button_back)
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_start)

        # set sub layouts as widgets
        widget1 = QWidget()
        widget2 = QWidget()
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)

        # create main layout
        layout3 = QVBoxLayout()
        layout3.addWidget(widget1)
        layout3.addWidget(widget2)

        # create a QWidget to QWidget to act as a container for the layout
        widget3 = QWidget()
        widget3.setLayout(layout3)
        self.setCentralWidget(widget3)

        # connect the buttons' clicked signals to the slots below
        self.button_back.clicked.connect(self.back_button_clicked)
        self.button_start.clicked.connect(self.start_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)

    def clear_button_clicked(self):
        self.text_phn.clear()

    def back_button_clicked(self):
        self.clear_button_clicked()
        self.close()

    def start_button_clicked(self):
        # get inputed phn
        phn = int(self.text_phn.text().strip())

        # start appointment
        try:
            # set patient to current patient
            self.controller.set_current_patient(phn)
            current_patient = self.controller.get_current_patient()
            # emit appoitment started signal to main menu
            self.app_started.emit()
            self.clear_button_clicked()

        # patient does not exist
        except IllegalOperationException:
            QMessageBox.warning(self, "Error Starting Appointment", "There is no patient registered with PHN %d" % phn)
            self.clear_button_clicked()
