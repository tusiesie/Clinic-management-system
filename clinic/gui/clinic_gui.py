import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from clinic.controller import Controller
from clinic.gui.login_window_gui import LoginWindowGUI
from clinic.gui.main_gui import MainGUI

class ClinicGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clinic Management System")
        # set window size
        self.resize(400, 200)
        self.controller = Controller(True)

        # add sub windows
        self.login_window_gui = LoginWindowGUI(self.controller)
        self.main_gui = MainGUI(self.controller)

        # setup vertical layout for widgets
        layout = QVBoxLayout()

        # create the "log in" and "quit" buttons
        self.login_button = QPushButton("Log in")
        self.quit_button = QPushButton("Quit")

        # set button width size constant
        button_width = self.width() // 3
        self.login_button.setFixedWidth(button_width)
        self.quit_button.setFixedWidth(button_width)

        # add buttons to middle of layout
        layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.quit_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Create a QWidget to act as a container for the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # login button clicked
        self.login_button.clicked.connect(self.login_button_clicked)
        # quit button clicked
        self.quit_button.clicked.connect(self.quit_button_clicked)

    def login_button_clicked(self):
       '''Goes to the login window'''
       # if login window gives login_successful signal, start main window
       self.login_window_gui.login_successful.connect(self.start_main_window)
       # open the login window
       self.login_window_gui.show()

    def start_main_window(self):
        '''Opens the main clinic window while closing all other windows'''
        # if main window gives logout_signal, show again
        self.main_gui.logout_signal.connect(self.show_again)
        # show clinic main menu
        self.main_gui.show()
        # hides the current window
        self.hide()

    def show_again(self):
        # shows the current window
        self.show()

    def quit_button_clicked(self):
        # terminate the application
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
