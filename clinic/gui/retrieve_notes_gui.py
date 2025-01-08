import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QMessageBox, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QPlainTextEdit

class RetrieveNotesGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Retrieve Notes by Text")
        self.resize(400, 300)
        self.controller = controller

        # create all components
        label_message = QLabel("Search for:")
        self.text_search_message = QLineEdit()
        self.retrieved_notes = QPlainTextEdit()
        self.retrieved_notes.setPlaceholderText("Notes will appear here...")
        self.retrieved_notes.setReadOnly(True)
        self.button_search = QPushButton("Search")
        self.button_clear = QPushButton("Clear")
        self.button_back = QPushButton("Back")

        # upper layout
        layout1 = QHBoxLayout()
        layout1.addWidget(label_message)
        layout1.addWidget(self.text_search_message)
        layout1.addWidget(self.button_search)

        # lower layout
        layout2 = QHBoxLayout()
        layout2.addWidget(self.button_back)
        layout2.addWidget(self.button_clear)

        # set sub layouts as widgets
        widget1 = QWidget()
        widget2 = QWidget()
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)

        # main layout
        layout3 = QVBoxLayout()
        layout3.addWidget(widget1)
        layout3.addWidget(self.retrieved_notes)
        layout3.addWidget(widget2)

        # create widget to act as container for main layout
        widget3 = QWidget()
        widget3.setLayout(layout3)
        self.setCentralWidget(widget3)

        # connect buttons' clicked with slots below
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_back.clicked.connect(self.back_button_clicked)

    def search_button_clicked(self):
        message = self.text_search_message.text().strip()

        retrieved_notes = self.controller.retrieve_notes(message)

        if not retrieved_notes:
            self.clear_button_clicked()
            QMessageBox.warning(self, "Error Getting Notes", "No notes found for %s" % message)
        else:
            self.clear_button_clicked()
            retrieved_notes_str = []

            for note in retrieved_notes:
                temp_str = "Note #%d, from %s \n %s" % (note.code, note.timestamp, note.text)
                retrieved_notes_str.append(temp_str)

            retrieved_notes_final = "\n\n".join(retrieved_notes_str)
            self.retrieved_notes.setPlainText(retrieved_notes_final)

    def clear_button_clicked(self):
        self.text_search_message.clear()
        self.retrieved_notes.clear()

    def back_button_clicked(self):
        self.clear_button_clicked()
        self.close()
