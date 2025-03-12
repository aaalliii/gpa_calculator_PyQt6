
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
from db.db_utils import update_user_info, set_is_remembered


class ProfileDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Profile Settings")

        self.name_edit = QLineEdit(self.user["name"])
        self.pfp_edit = QLineEdit(self.user.get("pfp", ""))
        self.choose_pfp_btn = QPushButton("Choose File")

        self.theme_edit = QLineEdit(self.user.get("theme", "light"))

        save_btn = QPushButton("Save Changes")
        cancel_btn = QPushButton("Cancel")
        logout_btn = QPushButton("Log Out")

        save_btn.clicked.connect(self.save_changes)
        cancel_btn.clicked.connect(self.close)
        logout_btn.clicked.connect(self.log_out)
        self.choose_pfp_btn.clicked.connect(self.choose_pfp)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("Profile Pic Path:"))
        pfp_layout = QHBoxLayout()
        pfp_layout.addWidget(self.pfp_edit)
        pfp_layout.addWidget(self.choose_pfp_btn)
        layout.addLayout(pfp_layout)

        layout.addWidget(QLabel("Theme (light/dark/...):"))
        layout.addWidget(self.theme_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(logout_btn)
        layout.addLayout(btn_layout)

    def choose_pfp(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose Profile Picture", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.pfp_edit.setText(file_path)

    def save_changes(self):
        new_name = self.name_edit.text().strip()
        new_pfp = self.pfp_edit.text().strip()
        new_theme = self.theme_edit.text().strip()

        update_user_info(self.user["uid"], new_name, new_pfp, new_theme)
        self.user["name"] = new_name
        self.user["pfp"] = new_pfp
        self.user["theme"] = new_theme

        self.close()

    def log_out(self):
        set_is_remembered(self.user["uid"], False)
        if self.parent():
            self.parent().close()
        self.close()

        from gui.login_page import LoginPage
        login = LoginPage()
        login.exec()
