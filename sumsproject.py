import tkinter as tk
from tkinter import ttk, messagebox
import json, os, csv

DATA_DIR = "data"
REPORT_DIR = "reports"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


def load_file(filename, default):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return default
    with open(path, "r") as file:
        return json.load(file)


def save_file(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


class University:
    def __init__(self):
        self.students = load_file("students.json", [])
        self.faculty = load_file("faculty.json", [])
        self.courses = load_file("courses.json", [])
        self.attendance = load_file("attendance.json", [])
        self.results = load_file("results.json", [])
        self.fees = load_file("fees.json", [])
        self.library = load_file("library.json", [])

    def save_all(self):
        save_file("students.json", self.students)
        save_file("faculty.json", self.faculty)
        save_file("courses.json", self.courses)
        save_file("attendance.json", self.attendance)
        save_file("results.json", self.results)
        save_file("fees.json", self.fees)
        save_file("library.json", self.library)


class SUMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart University Management System")
        self.root.geometry("1050x680")
        self.uni = University()
        self.current_role = ""
        self.login_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def title(self, text):
        tk.Label(self.root, text=text, font=("Arial", 20, "bold")).pack(pady=15)

    def login_screen(self):
        self.clear()
        frame = tk.Frame(self.root, padx=40, pady=40)
        frame.pack(expand=True)

        tk.Label(frame, text="SMART UNIVERSITY MANAGEMENT SYSTEM",
                 font=("Arial", 20, "bold")).pack(pady=15)

        tk.Label(frame, text="Username").pack()
        self.username = tk.Entry(frame, width=35)
        self.username.pack(pady=5)

        tk.Label(frame, text="Password").pack()
        self.password = tk.Entry(frame, width=35, show="*")
        self.password.pack(pady=5)

        tk.Label(frame, text="Role").pack()
        self.role = ttk.Combobox(frame, values=["Admin", "Faculty", "Student"],
                                 state="readonly", width=32)
        self.role.current(0)
        self.role.pack(pady=5)

        tk.Button(frame, text="Login", width=25, command=self.login).pack(pady=20)

        tk.Label(
            frame,
            text="Admin: admin/Admin@123 | Faculty: faculty/Faculty@123 | Student: student/Student@123",
            fg="gray"
        ).pack()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        role = self.role.get()

        if user == "admin" and pwd == "Admin@123" and role == "Admin":
            self.current_role = "Admin"
            self.admin_dashboard()

        elif user == "faculty" and pwd == "Faculty@123" and role == "Faculty":
            self.current_role = "Faculty"
            self.faculty_dashboard()

        elif user == "student" and pwd == "Student@123" and role == "Student":
            self.current_role = "Student"
            self.student_dashboard()

        else:
            messagebox.showerror("Error", "Invalid Login Details")

    def back_button(self):
        if self.current_role == "Admin":
            cmd = self.admin_dashboard
        elif self.current_role == "Faculty":
            cmd = self.faculty_dashboard
        else:
            cmd = self.student_dashboard

        tk.Button(self.root, text="Back", command=cmd).pack(pady=10)

    def create_table(self, columns, data):
        table = ttk.Treeview(self.root, columns=columns, show="headings", height=12)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=140)

        for row in data:
            table.insert("", "end", values=[row.get(col, "") for col in columns])

        table.pack(pady=10)
        return table

    def admin_dashboard(self):
        self.clear()
        self.title("Admin Dashboard")

        buttons = [
            ("Student Management", self.student_module),
            ("Faculty Management", self.faculty_module),
            ("Course Management", self.course_module),
            ("Attendance Management", self.attendance_module),
            ("Examination Management", self.exam_module),
            ("Fee Management", self.fee_module),
            ("Library Management", self.library_module),
            ("Generate Report", self.generate_report),
            ("Logout", self.login_screen)
        ]

        for text, cmd in buttons:
            tk.Button(self.root, text=text, width=30, height=2, command=cmd).pack(pady=4)

    def faculty_dashboard(self):
        self.clear()
        self.title("Faculty Dashboard")

        buttons = [
            ("Mark Attendance", self.attendance_module),
            ("Enter Examination Marks", self.exam_module),
            ("View Students", self.view_students),
            ("Generate Report", self.generate_report),
            ("Logout", self.login_screen)
        ]

        for text, cmd in buttons:
            tk.Button(self.root, text=text, width=30, height=2, command=cmd).pack(pady=5)

    def student_dashboard(self):
        self.clear()
        self.title("Student Dashboard")

        buttons = [
            ("View Attendance", self.view_attendance),
            ("View Result", self.view_result),
            ("View Fee Status", self.fee_module),
            ("View Courses", self.view_courses),
            ("Logout", self.login_screen)
        ]

        for text, cmd in buttons:
            tk.Button(self.root, text=text, width=30, height=2, command=cmd).pack(pady=5)

    def student_module(self):
        self.clear()
        self.title("Student Management")

        fields = ["Roll No", "Name", "Department", "Semester", "Email", "Phone"]
        entries = {}

        form = tk.Frame(self.root)
        form.pack()

        for i, field in enumerate(fields):
            tk.Label(form, text=field).grid(row=i, column=0, padx=5, pady=5)
            entries[field] = tk.Entry(form, width=35)
            entries[field].grid(row=i, column=1, padx=5, pady=5)

        def add_student():
            student = {field: entries[field].get() for field in fields}

            if student["Roll No"] == "" or student["Name"] == "":
                messagebox.showerror("Error", "Roll No and Name required")
                return

            self.uni.students.append(student)
            self.uni.fees.append({
                "Roll No": student["Roll No"],
                "Name": student["Name"],
                "Total Fee": "85000",
                "Paid": "0",
                "Balance": "85000"
            })
            self.uni.save_all()
            messagebox.showinfo("Success", "Student Added")
            self.student_module()

        tk.Button(form, text="Add Student", command=add_student).grid(row=6, column=1, pady=10)

        self.create_table(fields, self.uni.students)
        self.back_button()

    def faculty_module(self):
        self.clear()
        self.title("Faculty Management")

        fields = ["Employee ID", "Name", "Department", "Qualification", "Email", "Phone"]
        entries = {}

        form = tk.Frame(self.root)
        form.pack()

        for i, field in enumerate(fields):
            tk.Label(form, text=field).grid(row=i, column=0, padx=5, pady=5)
            entries[field] = tk.Entry(form, width=35)
            entries[field].grid(row=i, column=1, padx=5, pady=5)

        def add_faculty():
            faculty = {field: entries[field].get() for field in fields}
            self.uni.faculty.append(faculty)
            self.uni.save_all()
            messagebox.showinfo("Success", "Faculty Added")
            self.faculty_module()

        tk.Button(form, text="Add Faculty", command=add_faculty).grid(row=6, column=1, pady=10)

        self.create_table(fields, self.uni.faculty)
        self.back_button()

    def course_module(self):
        self.clear()
        self.title("Course Management")

        fields = ["Course ID", "Course Name", "Credits", "Department", "Semester"]
        entries = {}

        form = tk.Frame(self.root)
        form.pack()

        for i, field in enumerate(fields):
            tk.Label(form, text=field).grid(row=i, column=0, padx=5, pady=5)
            entries[field] = tk.Entry(form, width=35)
            entries[field].grid(row=i, column=1, padx=5, pady=5)

        def add_course():
            course = {field: entries[field].get() for field in fields}
            self.uni.courses.append(course)
            self.uni.save_all()
            messagebox.showinfo("Success", "Course Added")
            self.course_module()

        tk.Button(form, text="Add Course", command=add_course).grid(row=5, column=1, pady=10)

        self.create_table(fields, self.uni.courses)
        self.back_button()

    def attendance_module(self):
        self.clear()
        self.title("Attendance Management")

        fields = ["Roll No", "Course ID", "Total Classes", "Present Classes"]
        entries = {}

        form = tk.Frame(self.root)
        form.pack()

        for i, field in enumerate(fields):
            tk.Label(form, text=field).grid(row=i, column=0, padx=5, pady=5)
            entries[field] = tk.Entry(form, width=35)
            entries[field].grid(row=i, column=1, padx=5, pady=5)

        def add_attendance():
            try:
                total = int(entries["Total Classes"].get())
                present = int(entries["Present Classes"].get())

                if total <= 0 or present < 0 or present > total:
                    messagebox.showerror("Error", "Invalid attendance values")
                    return

                percentage = round((present / total) * 100, 2)

                record = {field: entries[field].get() for field in fields}
                record["Percentage"] = str(percentage)

                self.uni.attendance.append(record)
                self.uni.save_all()
                messagebox.showinfo("Success", "Attendance Added")
                self.attendance_module()

            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers")

        tk.Button(form, text="Add Attendance", command=add_attendance).grid(row=4, column=1, pady=10)

        self.create_table(fields + ["Percentage"], self.uni.attendance)
        self.back_button()

    def exam_module(self):
        self.clear()
        self.title("Examination Management")

        fields = ["Roll No", "Course ID", "Marks"]
        entries = {}

        form = tk.Frame(self.root)
        form.pack()

        for i, field in enumerate(fields):
            tk.Label(form, text=field).grid(row=i, column=0, padx=5, pady=5)
            entries[field] = tk.Entry(form, width=35)
            entries[field].grid(row=i, column=1, padx=5, pady=5)

        def add_result():
            try:
                marks = int(entries["Marks"].get())

                if marks < 0 or marks > 100:
                    messagebox.showerror("Error", "Marks must be 0 to 100")
                    return

                if marks >= 90:
                    grade = "A+"
                elif marks >= 75:
                    grade = "A"
                elif marks >= 60:
                    grade = "B"
                elif marks >= 40:
                    grade = "C"
                else:
                    grade = "Fail"

                record = {field: entries[field].get() for field in fields}
                record["Grade"] = grade

                self.uni.results.append(record)
                self.uni.save_all()
                messagebox.showinfo("Success", "Result Added")
                self.exam_module()

            except ValueError:
                messagebox.showerror("Error", "Enter valid marks")

        tk.Button(form, text="Add Result", command=add_result).grid(row=3, column=1, pady=10)

        self.create_table(fields + ["Grade"], self.uni.results)
        self.back_button()

    def fee_module(self):
        self.clear()
        self.title("Fee Management / Fee Status")

        fields = ["Roll No", "Name", "Total Fee", "Paid", "Balance"]
        self.create_table(fields, self.uni.fees)
        self.back_button()

    def library_module(self):
        self.clear()
        self.title("Library Management")

        fields = ["Book ID", "Book Name", "Author", "Status"]
        entries = {}

        form = tk.Frame(self.root)
        form.pack()

        for i, field in enumerate(fields):
            tk.Label(form, text=field).grid(row=i, column=0, padx=5, pady=5)
            entries[field] = tk.Entry(form, width=35)
            entries[field].grid(row=i, column=1, padx=5, pady=5)

        def add_book():
            book = {field: entries[field].get() for field in fields}
            self.uni.library.append(book)
            self.uni.save_all()
            messagebox.showinfo("Success", "Book Added")
            self.library_module()

        tk.Button(form, text="Add Book", command=add_book).grid(row=4, column=1, pady=10)

        self.create_table(fields, self.uni.library)
        self.back_button()

    def view_students(self):
        self.clear()
        self.title("View Students")
        fields = ["Roll No", "Name", "Department", "Semester", "Email", "Phone"]
        self.create_table(fields, self.uni.students)
        self.back_button()

    def view_attendance(self):
        self.clear()
        self.title("View Attendance")
        fields = ["Roll No", "Course ID", "Total Classes", "Present Classes", "Percentage"]
        self.create_table(fields, self.uni.attendance)
        self.back_button()

    def view_result(self):
        self.clear()
        self.title("View Result")
        fields = ["Roll No", "Course ID", "Marks", "Grade"]
        self.create_table(fields, self.uni.results)
        self.back_button()

    def view_courses(self):
        self.clear()
        self.title("View Courses")
        fields = ["Course ID", "Course Name", "Credits", "Department", "Semester"]
        self.create_table(fields, self.uni.courses)
        self.back_button()

    def generate_report(self):
        path = os.path.join(REPORT_DIR, "student_report.csv")

        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Roll No", "Name", "Department", "Semester", "Email", "Phone"])

            for student in self.uni.students:
                writer.writerow([
                    student.get("Roll No", ""),
                    student.get("Name", ""),
                    student.get("Department", ""),
                    student.get("Semester", ""),
                    student.get("Email", ""),
                    student.get("Phone", "")
                ])

        messagebox.showinfo("Report Generated", "Report saved in reports/student_report.csv")


root = tk.Tk()
app = SUMSApp(root)
root.mainloop()