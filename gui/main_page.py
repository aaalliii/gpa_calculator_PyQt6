import tkinter as tk
from tkinter import messagebox
from db.db_utils import fetch_sections, create_section


class MainPage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user  # user info from DB (UID, name, theme, etc.)
        self.master.title("GPA Calculator - Main")
        self.pack(fill="both", expand=True)

        self.sections_frame = tk.Frame(self)
        self.sections_frame.pack(pady=10, fill="both", expand=True)

        # A label to show total average GPA (you can dynamically recalc if needed)
        self.gpa_label = tk.Label(self, text="Your GPA is 0.0")
        self.gpa_label.pack()

        # Buttons
        tk.Button(self, text="Settings", command=self.open_settings).pack(side="left", padx=5)
        tk.Button(self, text=f"{self.user['name']}", command=self.open_profile).pack(side="right", padx=5)

        # Section list
        self.refresh_sections()

        # + Button to add a new Section
        tk.Button(self, text="+ Add Section", command=self.add_section).pack(pady=5)

        self.master.deiconify()

    def refresh_sections(self):
        # Clear old frame
        for widget in self.sections_frame.winfo_children():
            widget.destroy()

        # Fetch sections from DB
        uid = self.user['uid']
        sections = fetch_sections(uid)

        # Calculate overall average
        total_gpa = 0
        count = 0

        for sec in sections:
            # Each sec might be a dict: { 'did':X, 'name':..., 'gpa':... }
            frame = tk.Frame(self.sections_frame)
            frame.pack(fill="x", pady=5)

            tk.Label(frame, text=sec['name']).pack(side="left", padx=5)
            tk.Label(frame, text=str(sec['gpa'])).pack(side="left", padx=5)

            # Edit button
            edit_btn = tk.Button(frame, text="✎", command=lambda s=sec: self.edit_section(s))
            edit_btn.pack(side="right", padx=5)

            # Click on frame to open detail
            frame.bind("<Button-1>", lambda e, s=sec: self.open_section_details(s))

            total_gpa += sec['gpa']
            count += 1

        avg_gpa = round(total_gpa / count, 2) if count else 0.0
        self.gpa_label.config(text=f"Your GPA is {avg_gpa}")

    def add_section(self):
        # Create a new section in DB
        did = create_section(self.user['uid'], "New GPA Section")
        # Possibly open it directly in the “details” page
        from gui.section_details_page import SectionDetailsPage
        self.destroy()
        SectionDetailsPage(self.master, self.user, did)

    def edit_section(self, section):
        # Open a small popup to rename or delete the section
        from gui.edit_section_page import EditSectionPage
        EditSectionPage(self.master, section, self.refresh_sections)

    def open_section_details(self, section):
        from gui.section_details_page import SectionDetailsPage
        self.destroy()
        SectionDetailsPage(self.master, self.user, section['did'])

    def open_settings(self):
        messagebox.showinfo("Settings", "Show settings popup or new page here...")

    def open_profile(self):
        from gui.profile_page import ProfilePage
        ProfilePage(self.master, self.user, self.update_profile_callback)

    def update_profile_callback(self, updated_user):
        self.user = updated_user
        self.refresh_sections()
