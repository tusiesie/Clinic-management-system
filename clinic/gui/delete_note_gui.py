import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QHBoxLayout, QLineEdit

class DeleteNoteGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Remove Note from Patient Record")
        self.resize(300, 100)
        self.controller = controller

        # create all components
        label_code = QLabel("Note Number:")
        self.text_code = QLineEdit()
        self.button_delete = QPushButton("Delete")
        self.button_clear = QPushButton("Clear")
        self.button_back = QPushButton("Back")

        # set upper layout
        layout1 = QHBoxLayout()
        layout1.addWidget(label_code)
        layout1.addWidget(self.text_code)

        # set lower layout
        layout2 = QHBoxLayout()
        layout2.addWidget(self.button_back)
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_delete)

        # set sub layouts as widgets
        widget1 = QWidget()
        widget2 = QWidget()
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)

        # set main layout
        layout3 = QVBoxLayout()
        layout3.addWidget(widget1)
        layout3.addWidget(widget2)

        # create widget to act as container for main layout
        widget3 = QWidget()
        widget3.setLayout(layout3)
        self.setCentralWidget(widget3)

        # connect buttons' clicked to the slots below
        self.button_delete.clicked.connect(self.delete_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_back.clicked.connect(self.back_button_clicked)

    def delete_button_clicked(self):
        code = int(self.text_code.text().strip())

        deleted = self.controller.delete_note(code)

        reply = QMessageBox.question(self, "Delete Note", "Are you sure you want to remove note #%s?" % code, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if deleted:
                QMessageBox.information(self, "Note Deleted", "Successfully deleted the note")
                self.back_button_clicked()
            else:
                QMessageBox.warning(self, "Error Removing Note", "There is no note registered with this number")
                self.clear_button_clicked()


    def clear_button_clicked(self):
        self.text_code.clear()

    def back_button_clicked(self):
        self.clear_button_clicked()
        self.close()
