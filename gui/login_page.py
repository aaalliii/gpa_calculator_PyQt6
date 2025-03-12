from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox,
    QPushButton, QMessageBox
)
from db.db_utils import authenticate_user, set_is_remembered
from gui.register_page import RegisterPage
from gui.main_page import MainWindow


class LoginPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - GPA Calculator")

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.remember_box = QCheckBox("Remember me next time")

        sign_in_btn = QPushButton("Sign In")
        register_btn = QPushButton("Register New User")

        sign_in_btn.clicked.connect(self.handle_login)
        register_btn.clicked.connect(self.go_to_register)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)
        layout.addWidget(self.remember_box)
        layout.addWidget(sign_in_btn)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        user = authenticate_user(username, password)
        if user:
            if self.remember_box.isChecked():
                set_is_remembered(user["uid"], True)
            else:
                set_is_remembered(user["uid"], False)

            self.main_win = MainWindow(user)
            self.main_win.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password")

    def go_to_register(self):
        self.register_dialog = RegisterPage(self)
        self.register_dialog.exec()
