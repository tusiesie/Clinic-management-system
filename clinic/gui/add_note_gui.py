import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPlainTextEdit

class AddNoteGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Add Note to Patient Record")
        self.resize(400, 300)
        self.controller = controller

        # create all components
        label_message = QLabel("Enter message below:")
        self.text_message = QPlainTextEdit()
        self.button_create = QPushButton("Create")
        self.button_clear = QPushButton("Clear")
        self.button_back = QPushButton("Back")

        # lower layout
        layout1 = QHBoxLayout()
        layout1.addWidget(self.button_back)
        layout1.addWidget(self.button_clear)
        layout1.addWidget(self.button_create)

        # set layout layout as widget
        widget1 = QWidget()
        widget1.setLayout(layout1)

        # main layout
        layout2 = QVBoxLayout()
        layout2.addWidget(label_message)
        layout2.addWidget(self.text_message)
        layout2.addWidget(widget1)

        # create widget to act as container for main layout
        widget2 = QWidget()
        widget2.setLayout(layout2)
        self.setCentralWidget(widget2)

        # connect the buttons' clicked to the slots below
        self.button_create.clicked.connect(self.create_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_back.clicked.connect(self.back_button_clicked)

    def create_button_clicked(self):
        message = self.text_message.toPlainText().strip()
        self.clear_button_clicked()

        self.controller.create_note(message)

        self.back_button_clicked()

    def clear_button_clicked(self):
        self.text_message.clear()

    def back_button_clicked(self):
        self.clear_button_clicked()
        self.close()
