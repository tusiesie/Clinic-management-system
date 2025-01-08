import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QLineEdit, QHBoxLayout

class DeletePatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Delete Patient")
        self.resize(400, 200)
        self.controller = controller

        # set layout types
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()

        # create all components
        label_phn = QLabel("PHN:")
        self.text_phn = QLineEdit()
        self.button_clear = QPushButton("Clear")
        self.button_delete = QPushButton("Delete")
        self.button_back = QPushButton("Back")

        # add components to layout1 or layout2
        layout1.addWidget(label_phn)
        layout1.addWidget(self.text_phn)
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_delete)

        # turn layout1 and layout2 to widgets
        widget1 = QWidget()
        widget2 = QWidget()
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)

        # add components to layout 3
        layout3.addWidget(widget1)
        layout3.addWidget(widget2)
        layout3.addWidget(self.button_back)

        # create a QWidget tp act as a container for the layout
        main_widget = QWidget()
        main_widget.setLayout(layout3)
        self.setCentralWidget(main_widget)

        # connect the buttons' clicked to the slots below
        self.button_delete.clicked.connect(self.delete_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_back.clicked.connect(self.back_button_clicked)

    def delete_button_clicked(self):
        # get phn of patient to be deleted
        phn = int(self.text_phn.text().strip())

        # searches if patient is in system
        patient = self.controller.search_patient(phn)

        # patient not in system
        if not patient:
            QMessageBox.warning(self, "Error Removing Patient", "There is no patient registered with this PHN.")
            self.clear_button_clicked()
        else:
            # get patient name
            name = patient.name
            # show question box with yes or no answers
            reply = QMessageBox.question(self, "Update Patient", "Are you sure you want to remove patient %s?" % name, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.controller.delete_patient(phn)
                QMessageBox.information(self, "Patient Delete Success", "Patient removed from the system.")
                # refreshes field
                self.clear_button_clicked()
                self.back_button_clicked()

    def clear_button_clicked(self):
        self.text_phn.clear()

    def back_button_clicked(self):
        self.close()
