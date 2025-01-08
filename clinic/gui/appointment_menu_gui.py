import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from clinic.gui.add_note_gui import AddNoteGUI
from clinic.gui.retrieve_notes_gui import RetrieveNotesGUI
from clinic.gui.update_note_gui import UpdateNoteGUI
from clinic.gui.delete_note_gui import DeleteNoteGUI
from clinic.gui.list_all_notes_gui import ListAllNotesGUI

class AppointmentMenuGUI(QMainWindow):
    # signal to notiy appointment finished
    app_finished = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Appointment Menu")
        self.resize(500, 400)
        self.controller = controller

        # set layout type
        layout = QVBoxLayout()

        # add sub windows
        self.add_note_gui = AddNoteGUI(self.controller)
        self.retrieve_notes_gui = RetrieveNotesGUI(self.controller)
        self.update_note_gui = UpdateNoteGUI(self.controller)
        self.delete_note_gui = DeleteNoteGUI(self.controller)
        self.list_all_notes_gui = ListAllNotesGUI(self.controller)

        # create buttons
        self.button_add_note = QPushButton("Add Note to Patient Record")
        self.button_retrieve_notes = QPushButton("Retrieve note from Patient Record by Test")
        self.button_update_note = QPushButton("Change Note from Patient Record")
        self.button_remove_note = QPushButton("Remove Note from Patient Record")
        self.button_list_all_notes = QPushButton("List Full Patient Record")
        self.button_end_appointment = QPushButton("Finish Appointment")

        # set button width size
        button_width = self.width() // 1.5
        self.button_add_note.setFixedWidth(button_width)
        self.button_retrieve_notes.setFixedWidth(button_width)
        self.button_update_note.setFixedWidth(button_width)
        self.button_remove_note.setFixedWidth(button_width)
        self.button_list_all_notes.setFixedWidth(button_width)
        self.button_end_appointment.setFixedWidth(button_width)

        # add buttons to layout
        layout.addWidget(self.button_add_note)
        layout.addWidget(self.button_retrieve_notes)
        layout.addWidget(self.button_update_note)
        layout.addWidget(self.button_remove_note)
        layout.addWidget(self.button_list_all_notes)
        layout.addWidget(self.button_end_appointment)

        # create a QWidget to act as a continer for the layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # connect the buttons' clicked to the slots below
        self.button_add_note.clicked.connect(self.add_note)
        self.button_retrieve_notes.clicked.connect(self.retrieve_notes)
        self.button_update_note.clicked.connect(self.update_note)
        self.button_remove_note.clicked.connect(self.delete_note)
        self.button_list_all_notes.clicked.connect(self.list_all)
        self.button_end_appointment.clicked.connect(self.end_appointment)

    def add_note(self):
        self.add_note_gui.show()

    def retrieve_notes(self):
        self.retrieve_notes_gui.show()

    def update_note(self):
        self.update_note_gui.show()

    def delete_note(self):
        self.delete_note_gui.show()

    def list_all(self):
        self.list_all_notes_gui.show()

    def end_appointment(self):
        # appointment ended signal to main menu
        self.app_finished.emit()
        # unset current patient
        self.controller.unset_current_patient()
        self.close()
