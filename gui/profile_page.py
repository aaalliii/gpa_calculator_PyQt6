import tkinter as tk
from tkinter import messagebox
from db.db_utils import update_user_info, set_is_remembered


class ProfilePage(tk.Toplevel):
    def __init__(self, master, user, refresh_callback):
        super().__init__(master)
        self.user = user
        self.refresh_callback = refresh_callback

        self.title("User Profile")

        self.new_name_var = tk.StringVar(value=user['name'])
        self.theme_var = tk.StringVar(value=user['theme'])

        tk.Label(self, text="Profile Picture (URL)").pack(pady=5)
        # For changing pfp, you might just use an entry or a file dialog
        self.pfp_var = tk.StringVar(value=user['pfp'] if user['pfp'] else "")
        tk.Entry(self, textvariable=self.pfp_var).pack(pady=5)

        tk.Label(self, text="Name").pack(pady=5)
        tk.Entry(self, textvariable=self.new_name_var).pack(pady=5)

        # Theme toggle
        self.theme_button = tk.Button(self, text=f"Toggle Theme (Current: {self.theme_var.get()})",
                                      command=self.toggle_theme)
        self.theme_button.pack(pady=5)

        tk.Button(self, text="Save Changes", command=self.save_changes).pack(pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).pack(pady=5)
        tk.Button(self, text="Log Out", command=self.log_out).pack(pady=5)

    def toggle_theme(self):
        if self.theme_var.get() == "light":
            self.theme_var.set("dark")
        else:
            self.theme_var.set("light")
        self.theme_button.config(text=f"Toggle Theme (Current: {self.theme_var.get()})")

    def save_changes(self):
        update_user_info(
            self.user['uid'],
            self.new_name_var.get(),
            self.pfp_var.get(),
            self.theme_var.get()
        )
        self.refresh_callback({**self.user,
                               'name': self.new_name_var.get(),
                               'pfp': self.pfp_var.get(),
                               'theme': self.theme_var.get()
                               })
        self.destroy()

    def cancel(self):
        self.destroy()

    def log_out(self):
        # Set isRemembered = false for this user
        set_is_remembered(self.user['uid'], False)
        # Return to login page
        from gui.login_page import LoginPage
        self.master.destroy()  # close main window
        root = tk.Tk()
        LoginPage(root)
        self.destroy()
