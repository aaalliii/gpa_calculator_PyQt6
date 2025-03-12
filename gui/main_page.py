from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from db.db_utils import fetch_sections, create_section, delete_section
from gui.section_details_page import SectionDetailsDialog
from gui.profile_page import ProfileDialog


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("GPA Calculator")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)


        top_row = QHBoxLayout()

        self.pfp_label = QLabel()
        self.load_pfp_image()
        top_row.addWidget(self.pfp_label, alignment=Qt.AlignmentFlag.AlignLeft)

        top_row.addStretch(1)

        self.gpa_label = QLabel("Your GPA is 0.0")
        self.gpa_label.setStyleSheet("font-size: 14pt;")
        top_row.addWidget(self.gpa_label, alignment=Qt.AlignmentFlag.AlignCenter)

        top_row.addStretch(1)

        main_layout.addLayout(top_row)


        self.sections_list = QListWidget()
        self.sections_list.itemDoubleClicked.connect(self.open_section_details)
        main_layout.addWidget(self.sections_list)


        buttons_row = QHBoxLayout()

        self.profile_btn = QPushButton(f"Profile: {self.user['name']}")
        self.profile_btn.clicked.connect(self.open_profile)
        buttons_row.addWidget(self.profile_btn)

        self.add_section_btn = QPushButton("Add Section")
        self.add_section_btn.clicked.connect(self.add_section)
        buttons_row.addWidget(self.add_section_btn)

        self.delete_section_btn = QPushButton("Delete Selection")
        self.delete_section_btn.clicked.connect(self.delete_selected_section)
        buttons_row.addWidget(self.delete_section_btn)

        main_layout.addLayout(buttons_row)

        self.refresh_sections()


    def load_pfp_image(self):
        pfp_path = self.user.get("pfp", "")
        if pfp_path:
            pix = QPixmap(pfp_path)
            if not pix.isNull():
                pix = pix.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.pfp_label.setPixmap(pix)
                self.pfp_label.setFixedSize(50, 50)
                self.pfp_label.setStyleSheet("""
                    QLabel {
                        border-radius: 25px; /* half of 50 */
                        overflow: hidden;
                    }
                """)
            else:
                self.pfp_label.setText("No PFP")
        else:
            self.pfp_label.setText("No PFP")


    def refresh_sections(self):

        self.sections_list.clear()
        sections = fetch_sections(self.user["uid"])
        if not sections:
            self.gpa_label.setText("Your GPA is 0.0 (no sections yet)")
            return

        total_gpa = 0
        count = 0
        for sec in sections:
            item_text = f"{sec['name']} | GPA: {sec['gpa']:.2f}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, sec)
            self.sections_list.addItem(item)

            total_gpa += sec["gpa"]
            count += 1

        avg_gpa = total_gpa / count if count else 0.0
        self.gpa_label.setText(f"Your GPA is {avg_gpa:.2f}")


    def add_section(self):

        create_section(self.user["uid"], "New GPA Section")
        self.refresh_sections()

    def delete_selected_section(self):

        item = self.sections_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Please select a section to delete.")
            return

        sec_data = item.data(Qt.ItemDataRole.UserRole)
        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{sec_data['name']}'?"
        )
        if answer == QMessageBox.StandardButton.Yes:
            delete_section(sec_data["did"])
            self.refresh_sections()

    def open_section_details(self, item):

        sec_data = item.data(Qt.ItemDataRole.UserRole)
        dialog = SectionDetailsDialog(sec_data, self)
        dialog.exec()
        self.refresh_sections()

    def open_profile(self):

        dialog = ProfileDialog(self.user, parent=self)
        dialog.exec()

        self.profile_btn.setText(f"Profile: {self.user['name']}")
        self.load_pfp_image()
        self.refresh_sections()
