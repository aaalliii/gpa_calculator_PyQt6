import tkinter as tk
from tkinter import messagebox
from db.db_utils import rename_section, delete_section

class EditSectionPage(tk.Toplevel):
    def __init__(self, master, section, refresh_callback):
        super().__init__(master)
        self.section = section
        self.refresh_callback = refresh_callback

        self.title("Edit Section")
        self.name_var = tk.StringVar(value=section['name'])
        self.delete_var = tk.BooleanVar(value=False)

        tk.Label(self, text="Section Name").pack(pady=5)
        tk.Entry(self, textvariable=self.name_var).pack(pady=5)

        tk.Checkbutton(self, text="Delete this section", variable=self.delete_var).pack(pady=5)

        tk.Button(self, text="Cancel", command=self.cancel).pack(side="left", padx=5, pady=5)
        tk.Button(self, text="Save", command=self.save_changes).pack(side="right", padx=5, pady=5)

    def cancel(self):
        self.destroy()

    def save_changes(self):
        if self.delete_var.get():
            delete_section(self.section['did'])
        else:
            new_name = self.name_var.get()
            rename_section(self.section['did'], new_name)

        self.refresh_callback()
        self.destroy()
