import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QPlainTextEdit

class UpdateNoteGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Change Note from Clinic Record")
        self.resize(400, 300)
        self.controller = controller
        self.code = None

        # create all components
        label_search_code = QLabel("Enter code:")
        self.text_search_code = QLineEdit()
        self.button_search = QPushButton("Search")
        self.text_old_message = QPlainTextEdit()
        self.text_new_message = QPlainTextEdit()
        self.button_update = QPushButton("Update")
        self.button_clear = QPushButton("Clear")
        self.button_back = QPushButton("Back")

        # set placeholder text for text boxes
        self.text_old_message.setPlaceholderText("Note will appear here...")
        self.text_new_message.setPlaceholderText("Type new text for note here...")

        # disable text editing and update
        self.text_old_message.setReadOnly(True)
        self.text_new_message.setReadOnly(True)
        self.button_update.setEnabled(False)

        # upper layout
        layout1 = QHBoxLayout()
        layout1.addWidget(label_search_code)
        layout1.addWidget(self.text_search_code)
        layout1.addWidget(self.button_search)

        # lower layout
        layout2 = QHBoxLayout()
        layout2.addWidget(self.button_back)
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_update)

        # set sub layouts as widgets
        widget1 = QWidget()
        widget2 = QWidget()
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)

        # main layout
        layout3 = QVBoxLayout()
        layout3.addWidget(widget1)
        layout3.addWidget(self.text_old_message)
        layout3.addWidget(self.text_new_message)
        layout3.addWidget(widget2)

        # create widget to act as a containter for main layout
        widget3 = QWidget()
        widget3.setLayout(layout3)
        self.setCentralWidget(widget3)

        # connect the buttons' clicked to the slots below
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_update.clicked.connect(self.update_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_back.clicked.connect(self.back_button_clicked)

    def search_button_clicked(self):
        code = self.text_search_code.text().strip()
        
        if not code:
            QMessageBox.warning(self, "Invalid Input", "Please input a code to search")
            self.clear_button_clicked()
        else:
            self.code = int(code)
            note = self.controller.search_note(self.code)

            if not note:
                self.clear_button_clicked()
                QMessageBox.warning(self, "Invalid Code", "There is no note registered with this number")
            else:
                message = note.text
                self.text_old_message.setPlainText(message)
                self.text_new_message.setReadOnly(False)
                self.button_update.setEnabled(True)

    def update_button_clicked(self):
        reply = QMessageBox.question(self, "Update Note", "Are you sure you want to change note #%d?" % self.code, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if not self.code:
                QMessageBox.warning(self, "Update Note Error", "Please choose a note you want to update")
                self.clear_button_clicked()
            else:
                message = self.text_new_message.toPlainText().strip()
                if message == "":
                    QMessageBox.warning(self, "Update Failed", "Please provide the text you would like to update to")
                else:
                    self.controller.update_note(self.code, message)
                    self.clear_button_clicked()
                    self.back_button_clicked()

    def clear_button_clicked(self):
        self.text_search_code.clear()
        self.text_old_message.clear()
        self.text_new_message.clear()
        self.text_new_message.setReadOnly(True)
        self.button_update.setEnabled(False)
        self.code = None

    def back_button_clicked(self):
        self.clear_button_clicked()
        self.close()
