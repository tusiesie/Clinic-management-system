import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QMessageBox, QVBoxLayout, QPlainTextEdit

class ListAllNotesGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("List Full Patient Record")
        self.resize(500, 400)
        self.controller = controller

        # create all components
        self.all_notes = QPlainTextEdit()
        self.all_notes.setPlaceholderText("Notes will appear here...")
        self.all_notes.setReadOnly(True)
        self.button_back = QPushButton("Back")

        # main layout
        layout = QVBoxLayout()
        layout.addWidget(self.all_notes)
        layout.addWidget(self.button_back)

        # create widget to act as container for main layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # connect buttons' clicked with slots below)
        self.button_back.clicked.connect(self.back_button_clicked)

    def showEvent(self, event):
        '''Called when the window is shown'''
        super().showEvent(event)  # Ensure the parent class's showEvent is called
        self.on_window_opened()  # Call the custom method

    def on_window_opened(self):
        '''Custom method triggered when the window is opened'''
        self.show_notes()

    def show_notes(self):
        all_notes = self.controller.list_notes()

        if not all_notes:
            QMessageBox.warning(self, "Error Getting Notes", "Patient record is empty")
            self.close()
        else:
            self.all_notes.clear()
            all_notes_str = []

            for note in all_notes:
                temp_str = "Note #%d, from %s \n %s" % (note.code, note.timestamp, note.text)
                all_notes_str.append(temp_str)

            all_notes_final = "\n\n".join(all_notes_str)
            self.all_notes.setPlainText(all_notes_final)

    def back_button_clicked(self):
        self.all_notes.clear()
        self.close()
