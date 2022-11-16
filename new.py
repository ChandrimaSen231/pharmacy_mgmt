from tkinter import *
from tkinter import ttk

inp = [{'Currency': 'EUR', 'Volume': '100', 'Country': 'SE'},
       {'Currency': 'GBR', 'Volume': '200', 'Country': 'SE'},
       {'Currency': 'CAD', 'Volume': '300', 'Country': 'SE'},
       {'Currency': 'EUR', 'Volume': '400', 'Country': 'SE'},
       {'Currency': 'EUR', 'Volume': '100', 'Country': 'DK'},
       {'Currency': 'GBR', 'Volume': '200', 'Country': 'DK'},
       {'Currency': 'CAD', 'Volume': '300', 'Country': 'DK'},
       {'Currency': 'EUR', 'Volume': '400', 'Country': 'DK'},
       ]


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Volume")

        self.combofr = Frame(self)
        self.combofr.pack(expand=True, fill=X)
        self.tree = ttk.Treeview(self, show='headings')
        columns = list(inp[0].keys())

        self.filters = ["combo_Currency","combo_Country"]

       
        

        self.tree["columns"] = columns
        self.tree.pack(expand=TRUE, fill=BOTH)

        btn = ttk.Button(self.combofr,text='CLick me',command=self.new_win)
        btn.pack(expand=True)

        for i in columns:
            self.tree.column(i, anchor="w")
            self.tree.heading(i, text=i, anchor="w")

        for i, row in enumerate(inp):
            self.tree.insert("", "end", text=i, values=list(row.values()))

    def close_win(self,top):
        top.destroy()

    def new_win(self):
        top= Toplevel(root)
        top.geometry("300x150")
        rootframe = ttk.Frame(top)
        rootframe.pack(fill='both')
         
        

        l1 = ttk.Label(rootframe, text="Item Id",style='small.TLabel')
        l1.grid(row=0, column=0, padx=6, pady=2, sticky="sw")

        setattr(self, "combo_Currency", ttk.Entry(rootframe))
        getattr(self, "combo_Currency").grid(row=1)
        #getattr(self, "combo_Currency").bind('<KeyRelease>', self.select_from_filters)
        l2 = ttk.Label(rootframe, text=f"Item Name",style='small.TLabel')
        l2.grid(row=2, column=0, padx=6, pady=2, sticky="sw")

        setattr(self, "combo_Country", ttk.Entry(rootframe))
        getattr(self, "combo_Country").grid(row=3)
        #getattr(self, "combo_Country").bind('<KeyRelease>', self.select_from_filters)

        confirm_row_btn = ttk.Button(rootframe, text='Confirm', style="accent.TButton",command= lambda: self.select_from_filters(top))
        confirm_row_btn.grid(row=4, column=0, padx=10,pady=6,sticky='sew')

        cancel_button = ttk.Button(rootframe, text='Cancel', style="accent.TButton",command= lambda : self.close_win(top))
        cancel_button.grid(row=4, column=5, padx=10,pady=6,sticky='sew')


    def select_from_filters(self, top):
        self.tree.delete(*self.tree.get_children())

        all_filter = lambda x: all(x[f.split('_')[-1]] == getattr(self, f).get() or getattr(self, f).get() == '' for f in self.filters)
        for row in inp:
            if all_filter(row):
                self.tree.insert("", "end", values=list(row.values()))
        self.close_win(top)


root = Application()
root.mainloop()