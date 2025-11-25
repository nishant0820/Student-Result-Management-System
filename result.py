from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "rms.db")

class Result:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+200+250")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_name = StringVar()
        self.var_roll = StringVar()
        self.var_course = StringVar()
        self.var_subject = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list = []
        self.fetch_roll()

        # Title
        Label(self.root, text="Manage Results (Subject-wise)", font=("goudy old style", 20, "bold"),
              bg="orange", fg="#262626").place(x=10, y=15, width=1180, height=50)

        # Widgets
        Label(self.root, text="Select Student", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=100)
        Label(self.root, text="Name", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=160)
        Label(self.root, text="Course", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=220)
        Label(self.root, text="Subject", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=280)
        Label(self.root, text="Marks Obtained", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=340)
        Label(self.root, text="Full Marks", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=400)

        # Student combobox (roll)
        self.txt_student = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list,
                                        font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_student.place(x=260, y=100, width=200)
        self.txt_student.set("Select")
        Button(self.root, text="Search", command=self.search_student, font=("goudy old style", 15, "bold"),
               bg="#03a9f4", fg="white", cursor="hand2").place(x=480, y=100, width=100, height=28)

        # Display name/course
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 20, "bold"),
              bg="lightyellow", state='readonly').place(x=260, y=160, width=320)
        # Course combobox will be populated with this student's enrolled courses
        self.txt_course = ttk.Combobox(self.root, textvariable=self.var_course, values=[],
                                      font=("goudy old style", 20, "bold"), state='readonly', justify=CENTER)
        self.txt_course.place(x=260, y=220, width=320)

        # Subject (free text) and marks
        Entry(self.root, textvariable=self.var_subject, font=("goudy old style", 20, "bold"),
              bg="lightyellow").place(x=260, y=280, width=320)
        Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 20, "bold"),
              bg="lightyellow").place(x=260, y=340, width=320)
        Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 20, "bold"),
              bg="lightyellow").place(x=260, y=400, width=320)

        # Buttons
        Button(self.root, text="Submit", command=self.add, font=("goudy old style", 15),
               bg="lightgreen", activebackground="lightgreen", cursor="hand2").place(x=300, y=450, width=120, height=35)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15),
               bg="lightgray", activebackground="lightgray", cursor="hand2").place(x=430, y=450, width=120, height=35)

        # Right side image
        self.bg_img = Image.open(os.path.join(BASE_DIR, "images", "result.jpg")).resize((400, 300))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        Label(self.root, image=self.bg_img).place(x=740, y=100)

    def fetch_roll(self):
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute("SELECT roll FROM student ORDER BY roll")
                rows = cur.fetchall()
                self.roll_list = [str(r[0]) for r in rows] if rows else []
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching rolls: {ex}", parent=self.root)

    def search_student(self):
        roll = self.var_roll.get()
        if roll in ("", "Select"):
            messagebox.showerror("Error", "Select a student roll", parent=self.root)
            return
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute("SELECT name FROM student WHERE roll=?", (roll,))
                row = cur.fetchone()
                if row:
                    self.var_name.set(row[0])
                else:
                    messagebox.showerror("Error", "Student not found", parent=self.root)
                    return

                # fetch enrolled courses for this student (join enrollment -> course)
                cur.execute("""SELECT c.name FROM enrollment e
                               JOIN course c ON e.cid = c.cid
                               WHERE e.roll = ? ORDER BY c.name""", (roll,))
                courses = [r[0] for r in cur.fetchall()]
                if not courses:
                    messagebox.showinfo("Info", "This student is not enrolled in any course. Add enrollment first.", parent=self.root)
                    self.txt_course.config(values=[])
                    self.var_course.set("")
                else:
                    self.txt_course.config(values=courses)
                    self.txt_course.set(courses[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error while searching: {ex}", parent=self.root)

    def add(self):
        roll = self.var_roll.get()
        if roll in ("", "Select"):
            messagebox.showerror("Error", "Select a student roll first", parent=self.root)
            return
        if self.var_name.get() == "":
            messagebox.showerror("Error", "Search the student first", parent=self.root)
            return
        course = self.var_course.get().strip()
        subject = self.var_subject.get().strip()
        marks = self.var_marks.get().strip()
        full = self.var_full_marks.get().strip()

        if course == "":
            messagebox.showerror("Error", "Select course for which you are adding result", parent=self.root)
            return
        if subject == "":
            messagebox.showerror("Error", "Subject is required", parent=self.root)
            return
        try:
            marks_i = int(marks)
            full_i = int(full)
            if full_i <= 0:
                raise ValueError("Full marks must be > 0")
        except Exception as ex:
            messagebox.showerror("Error", f"Invalid marks/full marks: {ex}", parent=self.root)
            return

        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                # ensure student is enrolled in this course
                cur.execute("SELECT cid FROM course WHERE name=?", (course,))
                c = cur.fetchone()
                if not c:
                    messagebox.showerror("Error", "Selected course not found", parent=self.root)
                    return
                cid = c[0]
                cur.execute("SELECT * FROM enrollment WHERE roll=? AND cid=?", (roll, cid))
                if cur.fetchone() is None:
                    messagebox.showerror("Error", "Student is not enrolled in this course. Add enrollment first.", parent=self.root)
                    return

                # prevent duplicate subject for same roll+course+subject
                cur.execute("SELECT * FROM result WHERE roll=? AND course=? AND subject=?", (roll, course, subject))
                if cur.fetchone() is not None:
                    messagebox.showerror("Error", "Result for this subject already present for this student", parent=self.root)
                    return

                percent = (marks_i * 100.0) / full_i
                cur.execute("""INSERT INTO result (roll, name, course, subject, marks_ob, full_marks, per)
                               VALUES (?, ?, ?, ?, ?, ?, ?)""",
                            (roll, self.var_name.get(), course, subject, marks_i, full_i, percent))
                con.commit()
            messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
            # optionally clear subject/marks fields
            self.var_subject.set("")
            self.var_marks.set("")
            self.var_full_marks.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_subject.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")

if __name__ == "__main__":
    root = Tk()
    obj = Result(root)
    root.mainloop()
