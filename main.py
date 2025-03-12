import sys
from PyQt6.QtWidgets import QApplication

from db.db_init import init_db
from db.db_utils import check_remembered_user, get_user_by_id
from gui.login_page import LoginPage
from gui.main_page import MainWindow


def main():
    app = QApplication(sys.argv)

    init_db()

    remembered_uid = check_remembered_user()
    if remembered_uid:
        user_data = get_user_by_id(remembered_uid)
        if user_data:
            window = MainWindow(user_data)
            window.show()
        else:
            login = LoginPage()
            login.show()
    else:
        login = LoginPage()
        login.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
