import tkinter as tk
from tkinter import messagebox
from gui.register_page import RegisterPage
from db.db_utils import authenticate_user, set_is_remembered


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Login - GPA Calculator")
        self.pack()

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_var = tk.BooleanVar(value=False)

        # Build the UI
        tk.Label(self, text="Username").pack(pady=5)
        tk.Entry(self, textvariable=self.username_var).pack(pady=5)

        tk.Label(self, text="Password").pack(pady=5)
        tk.Entry(self, textvariable=self.password_var, show="*").pack(pady=5)

        tk.Checkbutton(self, text="Remember me next time", variable=self.remember_var).pack()

        tk.Button(self, text="Sign In", command=self.handle_login).pack(pady=5)
        tk.Button(self, text="Register New User", command=self.go_to_register).pack(pady=5)

        self.master.deiconify()  # Show the window

    def handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        user = authenticate_user(username, password)
        if user:
            uid = user[0]  # or however you structure your DB returns
            if self.remember_var.get():
                set_is_remembered(uid, True)
            else:
                set_is_remembered(uid, False)
            # Go to main page
            from gui.main_page import MainPage
            self.destroy()
            MainPage(self.master, user)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def go_to_register(self):
        self.destroy()
        RegisterPage(self.master)
