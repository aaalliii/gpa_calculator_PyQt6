from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from db.db_utils import register_user


class RegisterPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register - GPA Calculator")

        self.name_edit = QLineEdit()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        register_btn = QPushButton("Register")
        back_btn = QPushButton("Back to Login")

        register_btn.clicked.connect(self.handle_register)
        back_btn.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)
        layout.addWidget(register_btn)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def handle_register(self):
        name = self.name_edit.text().strip()
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        success = register_user(name, username, password)
        if success:
            QMessageBox.information(self, "Success", "User registered!")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Registration failed (username may exist)")

    def go_back(self):
        self.close()
