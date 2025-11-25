from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
from fpdf import FPDF
from course import Course
from student import Student
from report import Report
from result import Result
from datetime import datetime
import sqlite3, os
from math import sin, cos, radians

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+110+80")
        self.root.config(bg="white")
        self.dark_mode = False

        # ---------- Base Directory ----------
        self.base_dir = os.path.dirname(__file__)

        # ---------- Icons ----------
        self.logo_dash = ImageTk.PhotoImage(
            file=os.path.join(self.base_dir, "images", "logo_p.png")
        )

        # ---------- Title ----------
        title = Label(
            self.root,
            text="Student Result Management System",
            compound=LEFT,
            padx=10,
            image=self.logo_dash,
            font=("goudy old style", 20, "bold"),
            bg="#033054",
            fg="white",
        ).place(x=0, y=0, relwidth=1, height=50)

        # ---------- Menu Frame ----------
        M_Frame = LabelFrame(
            self.root, text="Menu", font=("times new roman", 15), bg="white"
        )
        M_Frame.place(x=10, y=70, width=1330, height=80)

        Button(M_Frame, text="Course", command=self.add_course, font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2").place(x=20, y=5, width=210, height=40)
        Button(M_Frame, text="Student", command=self.add_student, font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2").place(x=240, y=5, width=210, height=40)
        Button(M_Frame, text="Result", command=self.add_result, font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2").place(x=460, y=5, width=210, height=40)
        Button(M_Frame, text="View Result", command=self.add_report, font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2").place(x=680, y=5, width=210, height=40)
        # Button(M_Frame, text="PDF Report", command=self.generate_pdf_report, font=("goudy old style", 15, "bold"),
        #        bg="#0b5377", fg="white", cursor="hand2").place(x=900, y=5, width=210, height=40)
        Button(M_Frame, text="Dark Mode 🌙", command=self.toggle_theme, font=("goudy old style", 15, "bold"),
                bg="#0b5377", fg="white", cursor="hand2").place(x=900, y=5, width=210, height=40)
        Button(
                M_Frame,
                text="Exit",
                command=self.exit_app,
                font=("goudy old style", 15, "bold"),
                bg="#0b5377",
                fg="white",
                cursor="hand2"
            ).place(x=1120, y=5, width=190, height=40)


        # ---------- Background ----------
        bg_path = os.path.join(self.base_dir, "images", "bg.png")
        self.bg_img = Image.open(bg_path).resize((920, 350))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        Label(self.root, image=self.bg_img).place(x=400, y=180, width=920, height=350)

        # ---------- Dashboard Counters ----------
        self.lbl_course = Label(self.root, text="Total Courses\n[ 0 ]",
                                font=("goudy old style", 20), bd=10, relief=RIDGE,
                                bg="#e43b06", fg="white")
        self.lbl_course.place(x=400, y=540, width=300, height=100)

        self.lbl_student = Label(self.root, text="Total Students\n[ 0 ]",
                                 font=("goudy old style", 20), bd=10, relief=RIDGE,
                                 bg="#0676ad", fg="white")
        self.lbl_student.place(x=710, y=540, width=300, height=100)

        self.lbl_result = Label(self.root, text="Total Results\n[ 0 ]",
                                font=("goudy old style", 20), bd=10, relief=RIDGE,
                                bg="#038074", fg="white")
        self.lbl_result.place(x=1020, y=540, width=300, height=100)

        # ---------- Clock ----------
        self.lbl = Label(self.root, text="\nClock", font=("Book Antiqua", 25, "bold"),
                         fg="white", compound=BOTTOM, bg="#081923", bd=0)
        self.lbl.place(x=10, y=180, height=450, width=350)
        self.working()

        # ---------- Footer ----------
        Label(self.root, text="Student Result Management System | Contact: 9899459288",
              font=("goudy old style", 12), bg="#262626", fg="white").pack(side=BOTTOM, fill=X)

        # ---------- Auto Update ----------
        self.update_details()

    # ======================================================
    #              BASIC FUNCTIONALITY
    # ======================================================
    def add_course(self):
        self.new_win = Toplevel(self.root)
        Course(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        Student(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        Result(self.new_win)

    def add_report(self):
        self.new_win = Toplevel(self.root)
        Report(self.new_win)

    def exit_app(self):
        if messagebox.askyesno("Confirm", "Do you really want to exit?", parent=self.root):
            self.root.destroy()

    # ======================================================
    #              CLOCK FUNCTION
    # ======================================================
    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock)
        bg = Image.open(os.path.join(self.base_dir, "images", "c.png")).resize((300, 300))
        clock.paste(bg, (50, 50))

        ox, oy = 200, 200
        draw.line((ox, oy, ox + 50 * sin(radians(hr)), oy - 50 * cos(radians(hr))), fill="#DF005E", width=4)
        draw.line((ox, oy, ox + 80 * sin(radians(min_)), oy - 80 * cos(radians(min_))), fill="white", width=3)
        draw.line((ox, oy, ox + 100 * sin(radians(sec_)), oy - 100 * cos(radians(sec_))), fill="yellow", width=2)
        draw.ellipse((195, 195, 210, 210), fill="#1AD5D5")
        clock.save(os.path.join(self.base_dir, "images", "clock_new.png"))

    def working(self):
        now = datetime.now()
        hr = (now.hour / 12) * 360
        min_ = (now.minute / 60) * 360
        sec_ = (now.second / 60) * 360
        self.clock_image(hr, min_, sec_)
        img_path = os.path.join(self.base_dir, "images", "clock_new.png")
        self.img = ImageTk.PhotoImage(file=img_path)
        self.lbl.config(image=self.img)
        self.lbl.after(1000, self.working)

    # ======================================================
    #              AUTO UPDATE COUNTERS
    # ======================================================
    def update_details(self):
        try:
            with sqlite3.connect(os.path.join(self.base_dir, "rms.db")) as con:
                cur = con.cursor()
                cur.execute("SELECT COUNT(*) FROM course")
                cr = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM student")
                st = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM result")
                rs = cur.fetchone()[0]
            self.lbl_course.config(text=f"Total Courses\n[{cr}]")
            self.lbl_student.config(text=f"Total Students\n[{st}]")
            self.lbl_result.config(text=f"Total Results\n[{rs}]")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")
        self.root.after(1500, self.update_details)

    # ======================================================
    #              DARK MODE FEATURE
    # ======================================================
    def toggle_theme(self):
        if not self.dark_mode:
            self.root.config(bg="#1e1e1e")
            self.lbl.config(bg="#0f0f0f", fg="white")
            self.lbl_course.config(bg="#444444")
            self.lbl_student.config(bg="#555555")
            self.lbl_result.config(bg="#666666")
            self.dark_mode = True
        else:
            self.root.config(bg="white")
            self.lbl.config(bg="#081923", fg="white")
            self.lbl_course.config(bg="#e43b06")
            self.lbl_student.config(bg="#0676ad")
            self.lbl_result.config(bg="#038074")
            self.dark_mode = False

    # ======================================================
    #              PDF REPORT GENERATION
    # ======================================================
    def generate_pdf_report(self):
        try:
            with sqlite3.connect(os.path.join(self.base_dir, "rms.db")) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM result")
                data = cur.fetchall()
                if not data:
                    messagebox.showinfo("Info", "No results to export.", parent=self.root)
                    return

            reports_path = os.path.join(self.base_dir, "reports")
            os.makedirs(reports_path, exist_ok=True)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, "Student Results Report", ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            for row in data:
                pdf.cell(200, 10, f"Roll: {row[1]} | Name: {row[2]} | Course: {row[3]} | Marks: {row[4]}/{row[5]} | %: {row[6]}", ln=True)
            pdf.output(os.path.join(reports_path, "All_Results.pdf"))
            messagebox.showinfo("Success", f"PDF report saved in: {reports_path}", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error generating PDF: {str(ex)}")


# =========================================================
if __name__ == "__main__":
    root = Tk()
    RMS(root)
    root.mainloop()
