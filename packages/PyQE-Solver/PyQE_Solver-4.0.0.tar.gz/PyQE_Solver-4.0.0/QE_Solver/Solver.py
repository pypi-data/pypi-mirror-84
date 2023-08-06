import tkinter as tk
from tkinter import Label as l
from tkinter import Button as b
from tkinter import Canvas as c
from tkinter import Entry as e
import math
def start_Solving():
    r=tk.Tk()
    r.geometry("300x250")
    r.title("QUADRATIC EQUATION SOLVER")
    l1 = l(r,text="a = ")
    l2 = l(r,text="b = ")
    l3 = l(r,text="c = ")
    l4 = l(r,text="ROOT_1 will be here")
    l5 = l(r,text="ROOT_2 will be here")
    l1.grid(column=0,row=0)
    l2.grid(column=0,row=1)
    l3.grid(column=0,row=2)
    l4.grid(column=0,row=6)
    l5.grid(column=1,row=6)

    t1=tk.IntVar()
    t1.set(1)
    t2=tk.IntVar()
    t2.set(2)
    t3=tk.IntVar()
    t3.set(1)

    e1=e(r,textvariable=t1)
    e2=e(r,textvariable=t2)
    e3=e(r,textvariable=t3)
    e1.grid(column=1,row=0)
    e2.grid(column=1,row=1)
    e3.grid(column=1,row=2)
    def  calc():
        a=int(e1.get())
        b=int(e2.get())
        c=int(e3.get())
        if a!=0:
            if ((4*a*c)<=(b*b)):
                d=math.sqrt((b*b)-4*a*c)
                if d<0:
                    sol1=((-b)+d)/2*a
                    sol2=((-b)-d)/2*a
                    l4.config(text=sol1)
                    l5.config(text=sol2)
                elif d==0:
                    sol1=((-b)+d/2*a)
                    sol2=sol1
                    l4.config(text=sol1)
                    l5.config(text=sol2)
                else:
                    l4.config(text="COMPLEX")
                    l5.config(text="COMPLEX")
            else:
                l4.config(text="COMPLEX")
                l5.config(text="COMPLEX")
        else:
            l4.config(text="Not Possible.")
            l5.config(text="a can't be zero.")
    def bye():
        r.destroy()
        print("COMMAND SUCCESSFULL!!!")
    def contact():
        l8=l(r,text="somanip409@gmail.com")
        l8.grid(column=0,row=10)
    b1=b(r,text="SUBMIT",command=calc)
    b1.grid(column=0,row=4)
    b2=b(r,text="EXIT",command=bye)
    b2.grid(column=1,row=4)
    l6=l(r,text="Author = ").grid(column=0,row=8)
    l7=l(r,text="Piyush").grid(column=1,row=8)
    b3=b(r,text="Contact",command=contact)
    b3.grid(column=0,row=9)
    r.mainloop()
