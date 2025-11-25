from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os
from fpdf import FPDF
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "rms.db")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

PASS_THRESHOLD = 35.0  # change if needed


class Report:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x520+200+200")
        self.root.config(bg="white")
        self.root.focus_force()

        Label(self.root, text="View Student Results (Subject-wise)", font=("goudy old style", 20, "bold"),
              bg="orange", fg="#262626").place(x=10, y=15, width=1180, height=50)

        self.var_search = StringVar()
        self.selected_rid = ""

        Label(self.root, text="Search By Roll No.", font=("goudy old style", 16, "bold"), bg="white").place(x=200, y=90)
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 16),
              bg="lightyellow").place(x=380, y=90, width=180)
        Button(self.root, text="Search", command=self.search, font=("goudy old style", 14, "bold"),
               bg="#03a9f4", fg="white").place(x=580, y=90, width=100, height=30)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 14, "bold"),
               bg="gray", fg="white").place(x=700, y=90, width=100, height=30)

        # Header Labels
        Label(self.root, text="Roll No", font=("goudy old style", 14, "bold"), bg="white").place(x=50, y=150)
        Label(self.root, text="Name", font=("goudy old style", 14, "bold"), bg="white").place(x=250, y=150)
        Label(self.root, text="Course(s)", font=("goudy old style", 14, "bold"), bg="white").place(x=500, y=150)
        Label(self.root, text="Overall %", font=("goudy old style", 14, "bold"), bg="white").place(x=900, y=150)

        self.lbl_roll = Label(self.root, text="", font=("goudy old style", 14, "bold"), bg="white", bd=2, relief=GROOVE)
        self.lbl_roll.place(x=50, y=190, width=150, height=40)
        self.lbl_name = Label(self.root, text="", font=("goudy old style", 14, "bold"), bg="white", bd=2, relief=GROOVE)
        self.lbl_name.place(x=250, y=190, width=220, height=40)
        self.lbl_course = Label(self.root, text="", font=("goudy old style", 14, "bold"), bg="white", bd=2, relief=GROOVE)
        self.lbl_course.place(x=500, y=190, width=350, height=40)
        self.lbl_overall = Label(self.root, text="", font=("goudy old style", 14, "bold"), bg="white", bd=2, relief=GROOVE)
        self.lbl_overall.place(x=900, y=190, width=150, height=40)

        # Table
        frame_table = Frame(self.root, bd=2, relief=RIDGE)
        frame_table.place(x=50, y=260, width=1100, height=220)

        cols = ("rid", "subject", "marks", "full", "per")
        self.ResultTable = ttk.Treeview(frame_table, columns=cols, show='headings')
        for col, text, w in zip(cols, ["ID", "Subject", "Marks Obtained", "Total Marks", "Percentage"],
                                [40, 400, 150, 150, 150]):
            self.ResultTable.heading(col, text=text)
            self.ResultTable.column(col, width=w)
        self.ResultTable.pack(fill=BOTH, expand=1)
        self.ResultTable.bind("<ButtonRelease-1>", self.on_select)

        # Action buttons
        Button(self.root, text="Delete Selected Subject Result", command=self.delete,
               font=("goudy old style", 14, "bold"), bg="red", fg="white").place(x=50, y=490, width=300, height=35)

        Button(self.root, text="Export Student PDF", command=self.export_student_pdf,
               font=("goudy old style", 14, "bold"), bg="#2196f3", fg="white").place(x=380, y=490, width=260, height=35)

    # ------------------ SEARCH --------------------
    def search(self):
        roll = self.var_search.get().strip()
        if not roll:
            messagebox.showerror("Error", "Roll No Required", parent=self.root)
            return
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM result WHERE roll=?", (roll,))
                rows = cur.fetchall()

                if not rows:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
                    self.clear_summary()
                    return

            self.lbl_roll.config(text=roll)
            self.lbl_name.config(text=rows[0][2])
            courses = sorted({r[3] for r in rows if r[3]})
            self.lbl_course.config(text=", ".join(courses))

            self.ResultTable.delete(*self.ResultTable.get_children())
            total_ob = total_full = 0
            for r in rows:
                total_ob += int(r[5])
                total_full += int(r[6])
                self.ResultTable.insert('', END, values=(r[0], r[4], r[5], r[6], f"{float(r[7]):.2f}"))

            overall = (total_ob * 100) / total_full if total_full else 0
            self.lbl_overall.config(text=f"{overall:.2f}%")

        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=self.root)

    def on_select(self, event):
        try:
            self.selected_rid = self.ResultTable.item(self.ResultTable.focus(), "values")[0]
        except:
            self.selected_rid = ""

    # ------------------ DELETE --------------------
    def delete(self):
        if not self.selected_rid:
            messagebox.showerror("Error", "Select a row to delete!", parent=self.root)
            return
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM result WHERE rid=?", (self.selected_rid,))
            con.commit()
        messagebox.showinfo("Success", "Subject Result Deleted", parent=self.root)
        self.search()

    # ------------------ CLEAR ---------------------
    def clear_summary(self):
        self.lbl_roll.config(text="")
        self.lbl_name.config(text="")
        self.lbl_course.config(text="")
        self.lbl_overall.config(text="")
        self.ResultTable.delete(*self.ResultTable.get_children())

    def clear(self):
        self.var_search.set("")
        self.clear_summary()

    # ----------------- EXPORT PDF -----------------
    def export_student_pdf(self):
        roll = self.lbl_roll.cget("text").strip()
        if not roll:
            messagebox.showerror("Error", "Search student first!", parent=self.root)
            return

        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE roll=? ORDER BY rid", (roll,))
            rows = cur.fetchall()
            if not rows:
                messagebox.showerror("Error", "No results found", parent=self.root)
                return

        total_ob = sum(int(r[5]) for r in rows)
        total_full = sum(int(r[6]) for r in rows)
        overall = (total_ob * 100) / total_full if total_full else 0
        status = "PASS" if overall >= PASS_THRESHOLD else "FAIL"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "STUDENT RESULT MARKSHEET", ln=True, align='C')
        pdf.ln(5)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Roll No : {roll}", ln=True)
        pdf.cell(0, 8, f"Name    : {rows[0][2]}", ln=True)
        pdf.cell(0, 8, f"Courses : {', '.join(sorted({r[3] for r in rows}))}", ln=True)
        pdf.cell(0, 8, f"Date    : {datetime.now().strftime('%Y-%m-%d')}", ln=True)
        pdf.ln(4)

        pdf.set_font("Arial", "B", 11)
        pdf.cell(15, 10, "SN", 1, 0, "C")
        pdf.cell(95, 10, "SUBJECT", 1, 0, "C")
        pdf.cell(40, 10, "MAX MARKS", 1, 0, "C")
        pdf.cell(40, 10, "OBTAINED", 1, 1, "C")

        pdf.set_font("Arial", "", 11)
        for i, r in enumerate(rows, start=1):
            pdf.cell(15, 8, str(i), 1, 0, "C")
            pdf.cell(95, 8, str(r[4]), 1)
            pdf.cell(40, 8, str(r[6]), 1, 0, "C")
            pdf.cell(40, 8, str(r[5]), 1, 1, "C")

        pdf.ln(4)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Total Marks : {total_ob} / {total_full}", ln=True)
        pdf.cell(0, 8, f"Percentage  : {overall:.2f}%", ln=True)
        pdf.cell(0, 8, f"Result      : {status}", ln=True)

        filename = os.path.join(REPORTS_DIR, f"{roll}_marksheet.pdf")
        pdf.output(filename)

        messagebox.showinfo("Success", f"PDF Saved:\n{filename}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    Report(root)
    root.mainloop()
