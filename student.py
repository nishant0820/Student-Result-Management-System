from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "rms.db")

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x520+200+200")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_a_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        self.var_search = StringVar()

        # Fetch available courses to populate dropdown
        self.course_list = []
        self.fetch_course_list()

        # UI Title
        title = Label(self.root, text="Manage Student Details", font=("goudy old style", 20, "bold"),
                      bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # Form - left side
        Label(self.root, text="Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        self.txt_roll = Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_roll.place(x=150, y=60, width=200)

        Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=100, width=200)

        Label(self.root, text="Email", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=140, width=200)

        Label(self.root, text="Gender", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)
        self.txt_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"),
                                       font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_gender.place(x=150, y=180, width=200)
        self.txt_gender.current(0)

        Label(self.root, text="D.O.B.", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=60)
        Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=480, y=60, width=200)

        Label(self.root, text="Contact", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=100)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=480, y=100, width=200)

        Label(self.root, text="Admission", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=140)
        Entry(self.root, textvariable=self.var_a_date, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=480, y=140, width=200)

        Label(self.root, text="State", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=220)
        Entry(self.root, textvariable=self.var_state, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=220, width=150)

        Label(self.root, text="City", font=("goudy old style", 15, "bold"), bg="white").place(x=310, y=220)
        Entry(self.root, textvariable=self.var_city, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=380, y=220, width=100)

        Label(self.root, text="Pin", font=("goudy old style", 15, "bold"), bg="white").place(x=500, y=220)
        Entry(self.root, textvariable=self.var_pin, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=560, y=220, width=120)

        Label(self.root, text="Address", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=260)
        self.txt_address = Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_address.place(x=150, y=260, width=540, height=120)

        # Buttons
        Button(self.root, text="Save", command=self.add, font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white").place(x=150, y=400, width=110, height=40)
        Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white").place(x=270, y=400, width=110, height=40)
        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), bg="#f44336", fg="white").place(x=390, y=400, width=110, height=40)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white").place(x=510, y=400, width=110, height=40)

        # ---------- Right panel: search + enrolled courses ----------
        Label(self.root, text="Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=720, y=60)
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=870, y=60, width=180)
        Button(self.root, text="Search", command=self.search, font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white").place(x=1070, y=60, width=120, height=28)

        # Course selection & enrolled list
        Label(self.root, text="Available Courses", font=("goudy old style", 12, "bold"), bg="white").place(x=720, y=100)
        self.cmb_course = ttk.Combobox(self.root, values=self.course_list, font=("goudy old style", 12), state='readonly')
        self.cmb_course.place(x=720, y=130, width=240)
        if self.course_list:
            try:
                self.cmb_course.current(0)
            except:
                pass

        Button(self.root, text="Add Course →", command=self.add_enrollment, font=("goudy old style", 12), bg="#2196f3", fg="white").place(x=980, y=128, width=120, height=28)
        Button(self.root, text="← Remove", command=self.remove_enrollment, font=("goudy old style", 12), bg="#f44336", fg="white").place(x=980, y=168, width=120, height=28)

        Label(self.root, text="Enrolled Courses", font=("goudy old style", 12, "bold"), bg="white").place(x=720, y=200)
        self.lst_enrolled = Listbox(self.root, selectmode=SINGLE, font=("goudy old style", 12), bd=2, relief=RIDGE)
        self.lst_enrolled.place(x=720, y=230, width=380, height=200)

        # Student table (below)
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=440, width=460, height=120)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.StudentTable = ttk.Treeview(self.C_Frame, columns=("roll", "name", "course", "state", "city"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)
        self.StudentTable.heading("roll", text="Roll No.")
        self.StudentTable.heading("name", text="Name")
        self.StudentTable.heading("course", text="Course(s)")
        self.StudentTable.heading("state", text="State")
        self.StudentTable.heading("city", text="City")
        self.StudentTable["show"] = 'headings'
        self.StudentTable.column("roll", width=80)
        self.StudentTable.column("name", width=150)
        self.StudentTable.column("course", width=200)
        self.StudentTable.column("state", width=100)
        self.StudentTable.column("city", width=100)
        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # -------------------------
    def fetch_course_list(self):
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute("SELECT name FROM course ORDER BY name")
                rows = cur.fetchall()
                self.course_list = [r[0] for r in rows] if rows else []
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching courses: {ex}", parent=self.root)

    def add_enrollment(self):
        course_name = self.cmb_course.get().strip()
        if not course_name:
            messagebox.showerror("Error", "Select a course to add", parent=self.root)
            return
        # prevent duplicates in listbox
        existing = self.lst_enrolled.get(0, END)
        if course_name in existing:
            messagebox.showwarning("Warning", "Course already in enrolled list", parent=self.root)
            return
        self.lst_enrolled.insert(END, course_name)

    def remove_enrollment(self):
        sel = self.lst_enrolled.curselection()
        if not sel:
            messagebox.showerror("Error", "Select an enrolled course to remove", parent=self.root)
            return
        self.lst_enrolled.delete(sel[0])

    # -------------------------
    def add(self):
        # Save student and enrollments
        if self.var_roll.get().strip() == "":
            messagebox.showerror("Error", "Roll Number should be required", parent=self.root)
            return
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                # check duplicate roll
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                if cur.fetchone() is not None:
                    messagebox.showerror("Error", "Roll Number already present", parent=self.root)
                    return
                cur.execute("""INSERT INTO student (roll, name, email, gender, dob, contact, admission, course, state, city, pin, address)
                               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                            (self.var_roll.get(), self.var_name.get(), self.var_email.get(), self.var_gender.get(),
                             self.var_dob.get(), self.var_contact.get(), self.var_a_date.get(), "", self.var_state.get(),
                             self.var_city.get(), self.var_pin.get(), self.txt_address.get("1.0", END).strip()))
                con.commit()

                # Insert enrollments
                enrolled = self.lst_enrolled.get(0, END)
                # get cid for each course and insert into enrollment
                for cname in enrolled:
                    cur.execute("SELECT cid FROM course WHERE name=?", (cname,))
                    r = cur.fetchone()
                    if r:
                        cid = r[0]
                        cur.execute("INSERT OR IGNORE INTO enrollment (roll, cid) VALUES (?, ?)", (self.var_roll.get(), cid))
                con.commit()
            messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self):
        r = self.var_search.get().strip()
        if r == "":
            messagebox.showerror("Error", "Enter roll to search", parent=self.root)
            return
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM student WHERE roll=?", (r,))
                row = cur.fetchone()
                if row:
                    # populate fields
                    self.var_roll.set(row[0])
                    self.var_name.set(row[1])
                    self.var_email.set(row[2])
                    self.var_gender.set(row[3] if row[3] else "Select")
                    self.var_dob.set(row[4] if row[4] else "")
                    self.var_contact.set(row[5] if row[5] else "")
                    self.var_a_date.set(row[6] if row[6] else "")
                    self.var_state.set(row[8] if row[8] else "")
                    self.var_city.set(row[9] if row[9] else "")
                    self.var_pin.set(row[10] if row[10] else "")
                    self.txt_address.delete("1.0", END)
                    self.txt_address.insert(END, row[11] if row[11] else "")

                    # load enrolled courses for this roll
                    self.lst_enrolled.delete(0, END)
                    cur.execute("""SELECT c.name FROM enrollment e
                                   JOIN course c ON e.cid = c.cid
                                   WHERE e.roll = ? ORDER BY c.name""", (r,))
                    enrolled = cur.fetchall()
                    for e in enrolled:
                        self.lst_enrolled.insert(END, e[0])
                else:
                    messagebox.showerror("Error", "No student found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show(self):
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute("SELECT roll, name FROM student")
                rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for r in rows:
                roll = r[0]
                name = r[1]
                # get enrolled courses as comma separated
                with sqlite3.connect(DB_PATH) as con:
                    cur = con.cursor()
                    cur.execute("""SELECT GROUP_CONCAT(c.name, ', ') FROM enrollment e
                                   JOIN course c ON e.cid = c.cid WHERE e.roll = ?""", (roll,))
                    res = cur.fetchone()
                    courses = res[0] if res and res[0] else ""
                self.StudentTable.insert('', END, values=(roll, name, courses, "", ""))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        item = self.StudentTable.focus()
        if not item:
            return
        vals = self.StudentTable.item(item, "values")
        roll = vals[0]
        self.var_roll.set(roll)
        # reuse search to fill form and enrolled list
        self.var_search.set(roll)
        self.search()
        self.txt_roll.config(state='readonly')

    def update(self):
        if self.var_roll.get().strip() == "":
            messagebox.showerror("Error", "Roll No. should be required", parent=self.root)
            return
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if not row:
                    messagebox.showerror("Error", "Select Student from list", parent=self.root)
                    return
                # update student fields
                cur.execute("""UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, admission=?, state=?, city=?, pin=?, address=?
                               WHERE roll=?""",
                            (self.var_name.get(), self.var_email.get(), self.var_gender.get(), self.var_dob.get(),
                             self.var_contact.get(), self.var_a_date.get(), self.var_state.get(), self.var_city.get(),
                             self.var_pin.get(), self.txt_address.get("1.0", END).strip(), self.var_roll.get()))
                con.commit()

                # update enrollments: remove existing and insert from listbox
                cur.execute("DELETE FROM enrollment WHERE roll=?", (self.var_roll.get(),))
                for i in range(self.lst_enrolled.size()):
                    cname = self.lst_enrolled.get(i)
                    cur.execute("SELECT cid FROM course WHERE name=?", (cname,))
                    r = cur.fetchone()
                    if r:
                        cid = r[0]
                        cur.execute("INSERT OR IGNORE INTO enrollment (roll, cid) VALUES (?, ?)", (self.var_roll.get(), cid))
                con.commit()
            messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        if self.var_roll.get().strip() == "":
            messagebox.showerror("Error", "Roll No should be required", parent=self.root)
            return
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if not row:
                    messagebox.showerror("Error", "Please select student from the list", parent=self.root)
                    return
                op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if op:
                    # delete enrollments first, then student, and optionally results
                    cur.execute("DELETE FROM enrollment WHERE roll=?", (self.var_roll.get(),))
                    cur.execute("DELETE FROM result WHERE roll=?", (self.var_roll.get(),))
                    cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Student Deleted Successfully", parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.show()
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_a_date.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.var_search.set("")
        self.txt_address.delete("1.0", END)
        self.txt_roll.config(state=NORMAL)
        # clear enrolled list
        self.lst_enrolled.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
