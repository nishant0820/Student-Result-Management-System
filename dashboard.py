from tkinter import *
from PIL import Image,ImageTk
from course import Course
from student import Student

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
        btn_result=Button(M_Frame,text="Result",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=540,y=5,width=250,height=40)
        btn_view=Button(M_Frame,text="View Result",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=800,y=5,width=250,height=40)
        btn_exit=Button(M_Frame,text="Exit",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=1060,y=5,width=250,height=40)

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

        #------------- footer --------------
        footer=Label(self.root,text="Student Result Management System\nContact Us for any Technical Issue: 9899459288",font=("goudy old style",12),bg="#262626",fg="white").pack(side=BOTTOM,fill=X)

#----------------------------------------------------------------------------------------------------
    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Course(self.new_win)

    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Student(self.new_win)


if __name__=="__main__":
    root=Tk()
    obj=RMS(root)
    root.mainloop()