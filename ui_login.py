import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import ui
from theme import style
from ui_utils import grid_config
from ui_utils import *
from login_backend import  verify_data
import ui_pharm

class sales_login_page:
    def __init__(self, root,root_window):
        self.rootframe = ttk.Frame(root)
        self.note = ttk.Notebook(self.rootframe)
        

        self.rootframe.pack(fill="both", expand=1)
        grid_config(self.rootframe )

        l0 = ttk.Label(self.rootframe,text="Sales Login Page")
        l0.grid(row=0,column=3,padx=6, pady=2, sticky="sw")
        
        l1 = ttk.Label(self.rootframe,text="Enter username: ")
        l1.grid(row=3,column=2,padx=6, pady=2, sticky="sw")

        self.username_entry = ttk.Entry(self.rootframe)
        self.username_entry.grid(row=3,column=4,padx=6,pady=2,sticky="sew")

        l2 = ttk.Label(self.rootframe,text="Password: ")
        l2.grid(row=4,column=2,padx=6, pady=2, sticky="sw")

        self.password_entry = ttk.Entry(self.rootframe,show="*")
        self.password_entry.grid(row=4,column=4,padx=6,pady=2,sticky="sew")

        self.c_v1=IntVar(value=0)
        self.c1 = tk.Checkbutton(self.rootframe,text='Show Password',variable=self.c_v1,
	        onvalue=1,offvalue=0,command=self.my_show)
        self.c1.grid(row=5,column=4) 

        self.submit_btn = ttk.Button(self.rootframe, text='Login',command=lambda : self.verify_login(self.username_entry,self.password_entry), style="accent.TButton")
        self.submit_btn.grid(row=7, column=3, padx=10,pady=6,sticky='sew')
    
    def my_show(self):
        if(self.c_v1.get()==1):
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def verify_login(self,e1,e2):
        if verify_data(e1.get(),e2.get(),"Sales"):
            root.withdraw()
            
            ui_pharm.main(root)
            
        else:
            l3 = ttk.Label(self.rootframe,text="Wrong credentials")
            l3.grid(row=9,column=2,padx=6, pady=2, sticky="sw")   

    def as_tab(self):
        return self.rootframe

    def close_win(self,top):
        top.destroy()

class admin_login_page:
    def __init__(self, root,root_window):
        self.rootframe = ttk.Frame(root)
        self.note = ttk.Notebook(self.rootframe)
        
        self.rootframe.pack(fill="both", expand=1)
        grid_config(self.rootframe)

        l0 = ttk.Label(self.rootframe,text="Inventory Login Page")
        l0.grid(row=0,column=3,padx=6, pady=2, sticky="sw")

        l1 = ttk.Label(self.rootframe,text="Enter username: ")
        l1.grid(row=3,column=2,padx=6, pady=2, sticky="sw")

        self.username_entry = ttk.Entry(self.rootframe)
        self.username_entry.grid(row=3,column=4,padx=6,pady=2,sticky="sew")

        l2 = ttk.Label(self.rootframe,text="Password: ")
        l2.grid(row=4,column=2,padx=6, pady=2, sticky="sw")

        self.password_entry = ttk.Entry(self.rootframe,show="*")
        self.password_entry.grid(row=4,column=4,padx=6,pady=2,sticky="sew")

        self.submit_btn = ttk.Button(self.rootframe, text='Login',command=lambda : self.verify_login(self.username_entry,self.password_entry), style="accent.TButton")
        self.submit_btn.grid(row=7, column=3, padx=10,pady=6,sticky='sew')

        self.c_v1=IntVar(value=0)
        self.c1 = tk.Checkbutton(self.rootframe,text='Show Password',variable=self.c_v1,
	        onvalue=1,offvalue=0,command=self.my_show)
        self.c1.grid(row=5,column=4) 

        self.submit_btn = ttk.Button(self.rootframe, text='Login',command=lambda : self.verify_login(self.username_entry,self.password_entry), style="accent.TButton")
        self.submit_btn.grid(row=7, column=3, padx=10,pady=6,sticky='sew')
    
    def my_show(self):
        if(self.c_v1.get()==1):
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def verify_login(self,e1,e2):
        if verify_data(e1.get(),e2.get(),"Admin"):
            root.withdraw()
            ui.main(root)
            
        else:
            l3 = ttk.Label(self.rootframe,text="Wrong credentials")
            l3.grid(row=9,column=2,padx=6, pady=2, sticky="sw")

    def as_tab(self):
        return self.rootframe

    def close_win(self,top):
        top.destroy()

    
if __name__ == "__main__":
    root = tk.Tk()
    
    a = style(root)
    note = VerticalNavMenu(root)
    s = sales_login_page(note.content_frame,root)
    ad = admin_login_page(note.content_frame,root)
    note.add(s.as_tab(), text="Sales Login")
    note.add(ad.as_tab(), text="Inventory Login")
    note.pack(fill="both", expand=1)
    root.mainloop()