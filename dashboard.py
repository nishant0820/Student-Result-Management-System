from tkinter import *
from PIL import Image,ImageTk

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

        btn_course=Button(M_Frame,text="Course",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=20,y=5,width=250,height=40)
        btn_student=Button(M_Frame,text="Student",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=280,y=5,width=250,height=40)
        btn_result=Button(M_Frame,text="Result",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=540,y=5,width=250,height=40)
        btn_view=Button(M_Frame,text="View Result",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=800,y=5,width=250,height=40)
        btn_exit=Button(M_Frame,text="Exit",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2").place(x=1060,y=5,width=250,height=40)

        #------------- footer --------------
        footer=Label(self.root,text="SRMS-",compound=LEFT,padx=10,image=self.logo_dash,font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=50)



if __name__=="__main__":
    root=Tk()
    obj=RMS(root)
    root.mainloop()