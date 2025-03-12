from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from db.db_utils import (fetch_data_low, add_data_low, remove_data_low,
                         recalc_section_gpa, rename_section)


class SectionDetailsDialog(QDialog):
    def __init__(self, section, parent=None):
        super().__init__(parent)
        self.section = section
        self.setWindowTitle(f"Section Details - {self.section['name']}")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Section Name:"))
        self.section_name_edit = QLineEdit(self.section["name"])
        layout.addWidget(self.section_name_edit)

        layout.addWidget(QLabel("Courses:"))
        self.course_list = QListWidget()
        self.course_list.itemDoubleClicked.connect(self.delete_item)
        layout.addWidget(self.course_list)

        self.course_edit = QLineEdit()
        self.grade_edit = QLineEdit()
        self.credits_edit = QLineEdit()

        layout.addWidget(QLabel("Course Name:"))
        layout.addWidget(self.course_edit)
        layout.addWidget(QLabel("Grade:"))
        layout.addWidget(self.grade_edit)
        layout.addWidget(QLabel("Credits:"))
        layout.addWidget(self.credits_edit)

        add_btn = QPushButton("Add Course")
        calc_btn = QPushButton("Calculate GPA")
        save_btn = QPushButton("Save Section Name")

        add_btn.clicked.connect(self.handle_add)
        calc_btn.clicked.connect(self.handle_calculate)
        save_btn.clicked.connect(self.save_section_name)

        layout.addWidget(add_btn)
        layout.addWidget(calc_btn)
        layout.addWidget(save_btn)

        self.refresh_courses()

    def refresh_courses(self):
        self.course_list.clear()
        rows = fetch_data_low(self.section["did"])
        for row in rows:
            txt = f"{row['courseName']} | grade={row['grade']} | cr={row['credits']}"
            item = QListWidgetItem(txt)
            item.setData(Qt.ItemDataRole.UserRole, row)
            self.course_list.addItem(item)

    def handle_add(self):
        course = self.course_edit.text().strip()
        try:
            grade = float(self.grade_edit.text())
            credits = float(self.credits_edit.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid", "Grade/Credits must be numeric.")
            return

        if course:
            add_data_low(self.section["did"], course, grade, credits)
            self.refresh_courses()

    def handle_calculate(self):
        recalc_section_gpa(self.section["did"])
        QMessageBox.information(self, "Done", "Section GPA recalculated!")

    def delete_item(self, item):
        course_data = item.data(Qt.ItemDataRole.UserRole)
        didl = course_data["didl"]
        ans = QMessageBox.question(self, "Confirm", f"Delete {course_data['courseName']}?")
        if ans == QMessageBox.StandardButton.Yes:
            remove_data_low(didl)
            self.refresh_courses()

    def save_section_name(self):
        new_name = self.section_name_edit.text().strip()
        rename_section(self.section["did"], new_name)
        self.section["name"] = new_name
        self.setWindowTitle(f"Section Details - {new_name}")
        QMessageBox.information(self, "Saved", f"Section name changed to '{new_name}'.")
