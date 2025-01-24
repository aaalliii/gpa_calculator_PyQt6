import tkinter as tk
from db.db_utils import fetch_data_low, add_data_low, remove_data_low, recalc_section_gpa


class SectionDetailsPage(tk.Frame):
    def __init__(self, master, user, did):
        super().__init__(master)
        self.master = master
        self.user = user
        self.did = did
        self.pack(fill="both", expand=True)

        # Title
        tk.Button(self, text="← Back", command=self.go_back).pack(side="left", padx=5)

        self.title_label = tk.Label(self, text=f"GPA Section (DID={did})")
        self.title_label.pack(side="left", padx=5)

        self.courses_frame = tk.Frame(self)
        self.courses_frame.pack(pady=10, fill="both", expand=True)

        # Add course form
        self.course_name_var = tk.StringVar()
        self.grade_var = tk.DoubleVar()
        self.credits_var = tk.DoubleVar(value=1.0)

        tk.Entry(self, textvariable=self.course_name_var).pack(pady=5)
        tk.Entry(self, textvariable=self.grade_var).pack(pady=5)
        tk.Entry(self, textvariable=self.credits_var).pack(pady=5)

        tk.Button(self, text="Add", command=self.handle_add).pack(side="left", padx=5)
        tk.Button(self, text="Calculate", command=self.handle_calculate).pack(side="left", padx=5)

        self.refresh_courses()

    def refresh_courses(self):
        for widget in self.courses_frame.winfo_children():
            widget.destroy()

        courses = fetch_data_low(self.did)
        for course in courses:
            f = tk.Frame(self.courses_frame)
            f.pack(fill="x", pady=2)

            tk.Label(f, text=course["courseName"]).pack(side="left", padx=5)
            tk.Label(f, text=str(course["grade"])).pack(side="left", padx=5)
            tk.Label(f, text=str(course["credits"])).pack(side="left", padx=5)

            del_btn = tk.Button(f, text="✕", command=lambda c=course: self.delete_course(c["didl"]))
            del_btn.pack(side="right", padx=5)

    def handle_add(self):
        cn = self.course_name_var.get()
        gr = self.grade_var.get()
        cr = self.credits_var.get()
        if cn:
            add_data_low(self.did, cn, gr, cr)
            self.refresh_courses()

    def handle_calculate(self):
        recalc_section_gpa(self.did)  # updates the section’s gpa in DB
        tk.messagebox.showinfo("Done", "Section GPA recalculated!")

    def delete_course(self, didl):
        remove_data_low(didl)
        self.refresh_courses()

    def go_back(self):
        from gui.main_page import MainPage
        self.destroy()
        MainPage(self.master, self.user)
