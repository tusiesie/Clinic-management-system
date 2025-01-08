import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from clinic.exception.invalid_login_exception import InvalidLoginException

class LoginWindowGUI(QMainWindow):
    # signal to notify successful login
    login_successful = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Login")

        # set layout type of upper half
        layout1 = QGridLayout()

        # create all componenets
        label_username = QLabel("Username")
        self.text_username = QLineEdit()
        label_password = QLabel("Password")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Login")
        self.clear_button = QPushButton("Clear")
        self.back_button = QPushButton("Back")

        # arrange the placements of all componenets
        layout1.addWidget(label_username, 0, 0)
        layout1.addWidget(self.text_username, 0, 1)
        layout1.addWidget(label_password, 1, 0)
        layout1.addWidget(self.text_password, 1, 1)
        layout1.addWidget(self.clear_button, 2, 0)
        layout1.addWidget(self.login_button, 2, 1)

        # set the layout for all
        layout2 = QVBoxLayout()

        # configure main layout
        top_widget = QWidget()
        top_widget.setLayout(layout1)
        layout2.addWidget(top_widget)
        layout2.addWidget(self.back_button)

        # create a QWidget to act as a container for the layout
        widget = QWidget()
        widget.setLayout(layout2)
        self.setCentralWidget(widget)

        # connet the buttons' clicked signals to the slots below
        self.login_button.clicked.connect(self.login_button_clicked)
        self.clear_button.clicked.connect(self.clear_button_clicked)
        self.back_button.clicked.connect(self.back_button_clicked)

    def login_button_clicked(self):
        ''' handles the controller login'''
        # get the inputed username and password
        username = self.text_username.text().strip()
        password = self.text_password.text().strip()

        # try to login
        try:
            logged_in = self.controller.login(username, password)

            if logged_in:
                QMessageBox.information(self, "Login Successful", "Successfully logged in")
                # emit login_successful signal to clinic_gui.py
                self.login_successful.emit()
                # close current window
                self.back_button_clicked()

        # login incorrect
        except InvalidLoginException:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
            self.clear_button_clicked()

    def clear_button_clicked(self):
        '''Clear all fields in this window'''
        self.text_username.clear()
        self.text_password.clear()

    def back_button_clicked(self):
        '''Closes current window and goes back to clnic_gui.py'''
        self.clear_button_clicked()
        self.close()
