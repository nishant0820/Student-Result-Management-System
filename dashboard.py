from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk,ImageDraw
from course import Course
from student import Student
from report import Report
from result import Result
from datetime import *
import sqlite3
from math import *
import time
import os

class RMS:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+110+80")
        self.root.config(bg="white")

        #------------ icons --------------
        self.logo_dash=ImageTk.PhotoImage(file="Student-Result-Management-System/images/logo_p.png")

        #------------- title --------------
        title=Label(self.root,text="Student Result Management System",compound=LEFT,padx=10,image=self.logo_dash,font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=50)

        #---------------- menu -------------
        M_Frame=LabelFrame(self.root,text="Menu",font=("times new roman",15),bg="white")
        M_Frame.place(x=10,y=70,width=1330,height=80)

        btn_course=Button(M_Frame,text="Course",command=self.add_course,font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=20,y=5,width=250,height=40)
        btn_student=Button(M_Frame,text="Student",command=self.add_student,font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=280,y=5,width=250,height=40)
        btn_result=Button(M_Frame,text="Result",command=self.add_result,font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=540,y=5,width=250,height=40)
        btn_view=Button(M_Frame,text="View Result",command=self.add_report,font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=800,y=5,width=250,height=40)
        btn_exit=Button(M_Frame,text="Exit",command=self.exit,font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=1060,y=5,width=250,height=40)

        #---------- content window ----------------
        self.bg_img=Image.open("Student-Result-Management-System/images/bg.png")
        self.bg_img=self.bg_img.resize((920,350))
        self.bg_img=ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg=Label(self.root,image=self.bg_img).place(x=400,y=180,width=920,height=350)

        #-------------- update details ----------------
        self.lbl_course=Label(self.root,text="Total Courses\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#e43b06",fg="white")
        self.lbl_course.place(x=400,y=540,width=300,height=100)
        self.lbl_student=Label(self.root,text="Total Students\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#0676ad",fg="white")
        self.lbl_student.place(x=710,y=540,width=300,height=100)
        self.lbl_result=Label(self.root,text="Total Results\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#038074",fg="white")
        self.lbl_result.place(x=1020,y=540,width=300,height=100)

        #----------- clock -------------
        self.lbl=Label(self.root,text="\nClock",font=("Book Antiqua",25,"bold"),fg="white",compound=BOTTOM,bg="#081923",bd=0)
        self.lbl.place(x=10,y=180,height=450,width=350)
        self.working()

        #------------- footer --------------
        footer=Label(self.root,text="Student Result Management System\nContact Us for any Technical Issue: 9899459288",font=("goudy old style",12),bg="#262626",fg="white").pack(side=BOTTOM,fill=X)

        self.update_details()
#----------------------------------------------------------------------------------------------------
    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Course(self.new_win)

    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Student(self.new_win)

    def add_result(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Result(self.new_win)

    def add_report(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Report(self.new_win)

    def exit(self):
        op=messagebox.askyesno("Confirm","Do you really want to exit?",parent=self.root)
        if op==True:
            self.root.destroy()

    def clock_image(self,hr,min_,sec_):
        clock=Image.new("RGB",(400,400),(8,25,35))
        draw=ImageDraw.Draw(clock)
        #---------- For Clock Image ------------
        bg=Image.open("Student-Result-Management-System/images/c.png")
        bg=bg.resize((300,300))
        clock.paste(bg,(50,50))

        #---------- Hour Line Image ---------------
        origin=200,200
        draw.line((origin,200+50*sin(radians(hr)),200-50*cos(radians(hr))),fill="#DF005E",width=4)
        #---------- Min Line Image --------------
        draw.line((origin,200+80*sin(radians(min_)),200-80*cos(radians(min_))),fill="white",width=3)
        #---------- Sec Line Image --------------
        draw.line((origin,200+100*sin(radians(sec_)),200-100*cos(radians(sec_))),fill="yellow",width=2)
        draw.ellipse((195,195,210,210),fill="#1AD5D5")
        clock.save("Student-Result-Management-System/images/clock_new.png")

    def working(self):
        h=datetime.now().time().hour
        m=datetime.now().time().minute
        s=datetime.now().time().second

        hr=(h/12)*360
        min_=(m/60)*360
        sec_=(s/60)*360

        self.clock_image(hr,min_,sec_)
        self.img=ImageTk.PhotoImage(file="Student-Result-Management-System/images/clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200,self.working)

    def update_details(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from course")
            cr=cur.fetchall()
            self.lbl_course.config(text=f"Total Courses\n[{str(len(cr))}]")

            cur.execute("select * from student")
            st=cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[{str(len(st))}]")

            cur.execute("select * from result")
            rs=cur.fetchall()
            self.lbl_result.config(text=f"Total Results\n[{str(len(rs))}]")

            self.lbl_course.after(200,self.update_details)
            self.lbl_student.after(200,self.update_details)
            self.lbl_result.after(200,self.update_details)
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=RMS(root)
    root.mainloop()