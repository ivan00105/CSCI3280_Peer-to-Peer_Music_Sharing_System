import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt


class LoginScreen(QDialog):
    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Login Screen")
        self.resize(971, 514)

        # set window background color
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(0,0,32))
        self.setPalette(palette)

        # create widgets
        label_signin = QLabel("Sign In")
        label_signin.setStyleSheet("font-size: 32px; color: white; margin-bottom: 20px; font-weight: bold;")
        label_username = QLabel("Username:")
        label_username.setStyleSheet("font-size: 15px; color: white; margin-bottom: 20px;")
        self.edit_username = QLineEdit()
        self.edit_username.setStyleSheet("font-size:15px; margin-bottom: 20px;")
        self.edit_username.setPlaceholderText("Enter your username")
        label_password = QLabel("Password:")
        label_password.setStyleSheet("font-size: 15px; color: white; margin-bottom: 20px;")
        self.edit_password = QLineEdit()
        self.edit_password.setStyleSheet("font-size:15px; margin-bottom: 20px;")
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setPlaceholderText("Enter your password")
        button_login = QPushButton("Login")
        button_login.setStyleSheet("background-color: #1ABC9C; margin-bottom: 140px; font-weight: bold; color: rgb(0,0,32); border-radius: 10px; padding: 10px;")
        font = QFont()
        font.setPointSize(16)
        self.edit_username.setFont(font)
        self.edit_password.setFont(font)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(label_signin, 0, alignment=Qt.AlignTop|Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # create horizontal layout for labels and text fields
        form_layout = QHBoxLayout()
        form_layout.addStretch()
        form_layout.addWidget(label_username)
        form_layout.addWidget(self.edit_username)
        form_layout.addStretch()

        form_layout_2 = QHBoxLayout()
        form_layout_2.addStretch()
        form_layout_2.addWidget(label_password)
        form_layout_2.addWidget(self.edit_password)
        form_layout_2.addStretch()

        layout.addLayout(form_layout)
        layout.addLayout(form_layout_2)

        # create horizontal layout for button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button_login)
        button_layout.addStretch()

        # add button layout to main layout
        layout.addLayout(button_layout)

        # set dialog layout
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_screen = LoginScreen()
    login_screen.show()
    sys.exit(app.exec_())
