import tkinter as tk
from tkinter import messagebox
from db.db_utils import register_user

class RegisterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Register - GPA Calculator")
        self.pack()

        self.name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self, text="Name").pack(pady=5)
        tk.Entry(self, textvariable=self.name_var).pack(pady=5)

        tk.Label(self, text="Username").pack(pady=5)
        tk.Entry(self, textvariable=self.username_var).pack(pady=5)

        tk.Label(self, text="Password").pack(pady=5)
        tk.Entry(self, textvariable=self.password_var, show="*").pack(pady=5)

        tk.Button(self, text="Register", command=self.handle_register).pack(pady=5)
        tk.Button(self, text="Back to Login", command=self.go_back).pack(pady=5)

        self.master.deiconify()

    def handle_register(self):
        name = self.name_var.get()
        username = self.username_var.get()
        password = self.password_var.get()

        success = register_user(name, username, password)
        if success:
            messagebox.showinfo("Success", "User registered!")
            from gui.login_page import LoginPage
            self.destroy()
            LoginPage(self.master)
        else:
            messagebox.showerror("Error", "Registration failed (username may exist)")

    def go_back(self):
        from gui.login_page import LoginPage
        self.destroy()
        LoginPage(self.master)
