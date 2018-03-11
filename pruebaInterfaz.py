from tkinter import *

def xyz():
    global a
    print(a.get())

root=Tk()
Label(root,text="Enter your name").grid(row=0,column=0) #Creating label
a=Entry(root)           #creating entry box
a.grid(row=7,column=8)
Button(root,text="OK",command=xyz).grid(row=1,column=1)
root.mainloop()           #important for closing th root=Tk()
