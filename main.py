import tkinter as tk
from db.db_init import init_db
from gui.login_page import LoginPage
from db.db_utils import check_remembered_user, get_user_by_id
# ... other imports

def main():
    init_db()
    root = tk.Tk()
    root.withdraw()

    remembered_user_id = check_remembered_user()
    if remembered_user_id:
        user_data = get_user_by_id(remembered_user_id)
        # Possibly open MainPage directly with that user_data
    else:
        # Show the Login Page
        LoginPage(root)

    root.mainloop()

if __name__ == "__main__":
    main()
