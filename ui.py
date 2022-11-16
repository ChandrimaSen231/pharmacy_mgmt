from tkinter import ttk
import tkinter as tk
import datetime
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from backend import get_table,place_order,change_order_status,addItemtoDB,deleteItemfromDB,search_item
from ui_utils import *
def main(root_main):

    def grid_config(root, rows=8, cols=8):
        i = 0
        while i < cols:
            root.grid_columnconfigure(i, weight=1, minsize=40)
            i += 1


    def next_tab(notebk):
        all_tabs = notebk.tabs()
        sel_tab = notebk.select()

        if sel_tab == all_tabs[-1]:
            pass
        else:
            i = all_tabs.index(sel_tab)
            notebk.select(all_tabs[i + 1])


    def prev_tab(notebk):
        all_tabs = notebk.tabs()
        sel_tab = notebk.select()

        if sel_tab == all_tabs[0]:
            pass
        else:
            i = all_tabs.index(sel_tab)
            notebk.select(all_tabs[i - 1])


    def easy_treeview(master, columns):
        tv = ttk.Treeview(master=master, columns=columns, show="headings")

        for column in columns:
            tv.column(column, width=100, anchor="c", stretch=tk.YES)
            tv.heading(column, text=str(column))

        return tv


    def ins_row_treeview(tv, row_data):
        tv = ttk.Treeview()
        num_rows = len(tv.get_children())
        tv.insert(parent='', index=num_rows, iid=num_rows)

    def ins_rows_treeview(tv, rows):
        tv = ttk.Treeview()
        num_rows = len(tv.get_children())
        i=0
        for row in rows:
            tv.insert(parent='', index=num_rows+i, iid=num_rows+i)
            i+=1

    def new_row_dialog(master, columns):
        pass


    class treeview_toplevel:
        def __init__(self):
            self.main = tk.Toplevel()
            self.main.title("Insert Selected Data")
            self.rootframe = ttk.Frame(self.main)
            self.tv = ttk.Treeview(master=self.rootframe)

            self.search_textvar = tk.StringVar()

            self.search_cont = ttk.Frame(self.rootframe)
            self.search_field = ttk.Entry(
                self.search_cont, textvariable=self.search_textvar, name="search"
            )
            self.search_btn = ttk.Button(self.search_cont, text="Search")
            self.sel_btn = ttk.Button(
                master=self.rootframe, text="Insert Selected Data", style="accent.TButton"
            )
            self.main.withdraw()

        def config_behaviour(self, sel_cmd, search_cmd, search_field_text="Enter name"):
            self.sel_btn.config(command=sel_cmd)
            self.search_btn.config(command=search_cmd)
            self.search_field.config(name=search_field_text)

        def run(self):
            self.rootframe.pack(fill="both", expand=1, ipadx=6, ipady=6)
            self.tv.pack(fill="both", expand=2, padx=6, pady=4)
            self.search_cont.pack(fill="x", expand=1)
            self.search_btn.pack(side="left", padx=6, pady=4)
            self.search_field.pack(side="right", fill="x", expand=1, padx=6, pady=4)
            self.sel_btn.pack(fill="x", expand=1, padx=6, pady=4, anchor="s")
            self.main.deiconify()


    class data_edit:
        def __init__(self, master, row_data_dict):
            self.rootframe = ttk.Frame(master)


    class cust_page:
        def __init__(self, master, root_window):
            self.rootframe = ttk.Frame(master)
            self.note = ttk.Notebook(self.rootframe)

            self.filters = ttk.Frame(self.note)
            self.view = ttk.Frame(self.note)

            grid_config(self.filters)
            grid_config(self.view)

            self.cust_table = easy_treeview(
                self.view, columns=["Name", "Age", "Sex", "Address"]
            )
            self.cust_table.grid(
                row=0,
                column=0,
                padx=10,
                pady=10,
                rowspan=6,
                columnspan=8,
                ipadx=6,
                ipady=4,
                sticky="nswe",
            )

            self.edit_row_btn = ttk.Button(self.view, text='Edit row', style="accent.TButton")
            self.edit_row_btn.grid(row=7, column=0, padx=10,pady=6,sticky='sew')

            self.place_order = ttk.Button(self.view, text='+ Add row')
            self.place_order.grid(row=7, column=6, padx=10,pady=6,sticky='w')

            self.delete_row_btn = ttk.Button(self.view, text='- Delete row')
            self.delete_row_btn.grid(row=7, column=7, padx=10,pady=6,sticky='w')

            l1 = ttk.Label(self.filters, text="Customer Name", style="small.TLabel")
            l1.grid(row=0, column=0, padx=6, pady=2, sticky="sw")

            self.name_entry = ttk.Entry(self.filters)
            self.name_entry.grid(row=1, column=0, padx=6, pady=2, columnspan=8, sticky="ew")

            l2 = ttk.Label(self.filters, text="Age", style="small.TLabel")
            l2.grid(row=2, column=0, padx=6, pady=2, sticky="sw")

            self.age_entry = ttk.Entry(self.filters)
            self.age_entry.grid(row=3, column=0, padx=6, pady=2, columnspan=3, sticky="ew")

            l3 = ttk.Label(self.filters, text="Sex", style="small.TLabel")
            l3.grid(row=2, column=4, padx=6, pady=2, sticky="sw")

            self.sex_entry = ttk.Entry(self.filters)
            self.sex_entry.grid(row=3, column=4, padx=6, pady=2, columnspan=4, sticky="ew")

            l4 = ttk.Label(self.filters, text="Address", style="small.TLabel")
            l4.grid(row=4, column=0, padx=6, pady=2, sticky="sw")

            self.addr_entry = ttk.Entry(self.filters)
            self.addr_entry.grid(row=5, column=0, padx=6, pady=2, columnspan=8, sticky="ew")

            self.apply_btn = ttk.Button(
                self.filters, text="Apply Filters", style="accent.TButton"
            )
            self.apply_btn.grid(row=6, column=0, padx=6, pady=10, columnspan=8, sticky="ew")

            self.note.add(self.view, text="Table View")
            self.note.add(self.filters, text="Filters")
            self.note.pack(fill="both", expand=1, padx=10)
            self.note.enable_traversal()

            self.rootframe.pack(fill="both", expand=1)

        def get_cust_data(self):
            data = {}
            data["name"] = self.name_entry.get("1.0", "END")
            data["age"] = self.name_entry.get("1.0", "END")
            data["sex"] = self.name_entry.get("1.0", "END")
            data["addr"] = self.name_entry.get("1.0", "END")
            return data

        def as_tab(self):
            return self.rootframe


    class inventory_order_page:
        def __init__(self, master, root_window):
            self.rootframe = ttk.Frame(master)
            self.note = ttk.Notebook(self.rootframe)

            self.filters = ttk.Frame(self.note)
            self.view = ttk.Frame(self.note)

            grid_config(self.filters)
            grid_config(self.view)

            self.invt_table = easy_treeview(
                self.view, columns=["Order ID", "Order Name","Order Date","Item ID","Quantity","Amount", "Status"]
            )
            self.invt_table.grid(
                row=0,
                column=0,
                padx=10,
                pady=10,
                rowspan=6,
                columnspan=8,
                ipadx=6,
                ipady=4,
                sticky="nswe",
            )
            
            self.order_complete_btn = ttk.Button(self.view, text='Order completed', style="accent.TButton",command= self.orderRecievedBox ,state=tk.DISABLED)
            self.order_complete_btn.grid(row=7, column=0, padx=10,pady=6,sticky='sew')

            self.reset_btn = ttk.Button(self.view, text='Reset', style="accent.TButton",command= self.show_table)
            self.reset_btn.grid(row=7, column=7, padx=10,pady=6,sticky='sew')

            l1 = ttk.Label(self.filters, text="Item Id", style="small.TLabel")
            l1.grid(row=0, column=0, padx=6, pady=2, sticky="sw")

            setattr(self, "item_id", ttk.Entry(self.filters))
            getattr(self, "item_id").grid(row=1,column=0, padx=6,pady=2,sticky="sew",columnspan=8)

            l2 = ttk.Label(self.filters, text="Item Name", style="small.TLabel")
            l2.grid(row=2, column=0, padx=6, pady=2, sticky="sw")

            setattr(self, "item_name", ttk.Entry(self.filters))
            getattr(self, "item_name").grid(row=3,column=0, padx=6,pady=2,sticky="sew",columnspan=8)

            l3 = ttk.Label(self.filters, text="Status", style="small.TLabel")
            l3.grid(row=4, column=0, padx=6, pady=2, sticky="sw")

            setattr(self, "status", ttk.Entry(self.filters))
            getattr(self, "status").grid(row=5,column=0, padx=6,pady=2,sticky="sew",columnspan=8)
            

            self.show_table()
            #self.rootframe.after_idle(lambda : self.show_table(self.invt_table))

            self.invt_table.bind("<<TreeviewSelect>>",self.selected_item)

            self.apply_btn = ttk.Button(self.filters, text="Apply Filters", style="accent.TButton",command=self.select_from_filters)
            self.apply_btn.grid(row=6, column=0, padx=6, pady=10, columnspan=8, sticky="ew")


            self.note.add(self.view, text="Table View")
            self.note.add(self.filters, text="Filters")
            self.note.pack(fill="both", expand=1, padx=10)
            self.note.enable_traversal()

            self.rootframe.pack(fill="both", expand=1)

        def toggle_filters(self):
            if not self.show_filters:
                self.filters.pack(**self.filter_packinfo)
                self.show_filters = True
            else:
                self.filters.pack_forget()
                self.show_filters = False

        def selected_item(self,a):
            selectedItem = self.invt_table.selection()[0]
            status = self.invt_table.item(selectedItem)['values'][6]
            if status == 'Pending':
                self.order_complete_btn.config(state=tk.NORMAL)
            else:
                self.order_complete_btn.config(state=tk.DISABLED)
        
        def show_table(self):
            self.order_complete_btn.config(state=tk.DISABLED)
            getattr(self,"item_id").delete(0,tk.END)
            getattr(self,"item_name").delete(0,tk.END)
            getattr(self,"status").delete(0,tk.END)
            for item in self.invt_table.get_children():
                self.invt_table.delete(item)
            for row in get_table("inventory_order"):
                self.invt_table.insert("",tk.END,values=row)


        def as_tab(self):
            return self.rootframe

        def close_win(self,top):
            top.destroy()
        
        def orderReceived(self,top):
            selectedItem = self.invt_table.selection()[0]
            order_id = self.invt_table.item(selectedItem)['values'][0]
            item_id = self.invt_table.item(selectedItem)['values'][3]
            change_order_status(int(order_id),int(item_id))
            top.destroy()
            self.select_from_filters()
            o.show_table()
            i.show_table()


        def orderRecievedBox(self):
            top= tk.Toplevel(root)
            top.geometry("300x150")
            rootframe = ttk.Frame(top)
            rootframe.pack(fill='both')
            grid_config(rootframe)

            selectedItem = self.invt_table.selection()[0]
            order_id = self.invt_table.item(selectedItem)['values'][0]
            item_name = self.invt_table.item(selectedItem)['values'][1]
            item_id = self.invt_table.item(selectedItem)['values'][3]

            l1 = ttk.Label(rootframe, text=f"Confirm Order {order_id}: {item_id}-{item_name} Received",style='small.TLabel')
            l1.grid(row=0, column=0, padx=6, pady=2, sticky="sw",columnspan=6)

            confirm_row_btn = ttk.Button(rootframe, text='Yes', style="accent.TButton",command= lambda : self.orderReceived(top))
            confirm_row_btn.grid(row=7, column=0, padx=10,pady=6,sticky='sew',columnspan=2)

            cancel_button = ttk.Button(rootframe, text='No', style="accent.TButton",command= lambda : self.close_win(top))
            cancel_button.grid(row=7, column=2, padx=10,pady=6,sticky='sew',columnspan=2)

        def all_filter(self,row):
                d = {"item_id": 3, "item_name": 1,"status": 6}
                filter_list = ["item_id","item_name","status"]
                val = all(str(row[d[f]]) == getattr(self, f).get() or getattr(self, f).get() == '' for f in filter_list)
                return val

        def select_from_filters(self):
            self.invt_table.delete(*self.invt_table.get_children())
            for row in get_table("inventory_order"):
                if self.all_filter(row):
                    self.invt_table.insert("", "end", values=list(row))
            prev_tab(self.note)

    class item_page:
        def __init__(self, master, root_window):
            self.rootframe = ttk.Frame(master)
            self.note = ttk.Notebook(self.rootframe)

            self.filters = ttk.Frame(self.note)
            self.view = ttk.Frame(self.note)

            

            grid_config(self.filters)
            grid_config(self.view)

            self.search_entry = ttk.Entry(self.view)
            self.search_entry.grid(
                row=0, column=1, padx=10, pady=2, columnspan=7, sticky="we"
            )

            self.search_btn = ttk.Button(self.view, text="Search by Item Name")
            self.search_btn.grid(row=0, column=0, padx=10, pady=2, sticky="swe")

            self.search_entry.bind('<KeyRelease>', self.searchItem)

            self.item_table = easy_treeview(
                self.view, columns=["Item Id", "Item Name", "Stock Quantity","Amount","Total Amount", "Description"]
            )
            self.item_table.grid(
                row=2,
                column=0,
                padx=10,
                pady=10,
                rowspan=6,
                columnspan=8,
                ipadx=6,
                ipady=4,
                sticky="nswe",
            )

            self.edit_row_btn = ttk.Button(self.view, text='Edit row', style="accent.TButton")
            self.edit_row_btn.grid(row=7, column=0, padx=10,pady=6,sticky='sew')

            self.place_order = ttk.Button(self.view, text='Place Order', command=self.placeOrderBox, state=tk.DISABLED)
            self.place_order.grid(row=7, column=5, padx=10,pady=6,sticky='w')

            self.add_item = ttk.Button(self.view, text='+ Add item',command=self.addItemBox)
            self.add_item.grid(row=7, column=6, padx=10,pady=6,sticky='w')

            self.delete_row_btn = ttk.Button(self.view, text='- Delete item',command= self.deleteItemBox, state=tk.DISABLED)
            self.delete_row_btn.grid(row=7, column=7, padx=10,pady=6,sticky='w')


            l1 = ttk.Label(self.filters, text="Item Id", style="small.TLabel")
            l1.grid(row=0, column=0, padx=6, pady=2, sticky="sw")

            setattr(self, "item_id", ttk.Entry(self.filters))
            getattr(self, "item_id").grid(row=1,column=0, padx=6,pady=2,sticky="sw",columnspan=8)

            l2 = ttk.Label(self.filters, text="Item Name", style="small.TLabel")
            l2.grid(row=2, column=0, padx=6, pady=2, sticky="sw")

            setattr(self, "item_name", ttk.Entry(self.filters))
            getattr(self, "item_name").grid(row=3,column=0, padx=6,pady=2,sticky="sw",columnspan=8)

            l3 = ttk.Label(self.filters, text="Sex", style="small.TLabel")
            l3.grid(row=4, column=4, padx=6, pady=2, sticky="sw")

            setattr(self, "date", ttk.Entry(self.filters))
            getattr(self, "date").grid(row=3,column=0, padx=6,pady=2,sticky="sw",columnspan=8)

            l4 = ttk.Label(self.filters, text="Address", style="small.TLabel")
            l4.grid(row=4, column=0, padx=6, pady=2, sticky="sw")

            self.show_table()

            self.addr_entry = ttk.Entry(self.filters)
            self.addr_entry.grid(row=5, column=0, padx=6, pady=2, columnspan=8, sticky="ew")

            self.apply_btn = ttk.Button(
                self.filters, text="Apply Filters", style="accent.TButton"
            )
            self.apply_btn.grid(row=6, column=0, padx=6, pady=10, columnspan=8, sticky="ew")

            self.item_table.bind("<<TreeviewSelect>>",self.selected_item)
            

            self.note.add(self.view, text="Table View")
            self.note.add(self.filters, text="Filters")
            self.note.pack(fill="both", expand=1, padx=10)
            self.note.enable_traversal()

            self.rootframe.pack(fill="both", expand=1)
        
            
        def selected_item(self,a):
            self.place_order.config(state=tk.NORMAL)
            self.delete_row_btn.config(state=tk.NORMAL)

        def show_table(self):
            self.place_order.config(state=tk.DISABLED)
            self.delete_row_btn.config(state=tk.DISABLED)
            for item in self.item_table.get_children():
                self.item_table.delete(item)
            for row in get_table("items"):
                self.item_table.insert("",tk.END,values=row)
        
        def searchItem(self,a):
            search_val = self.search_entry.get()
            for item in self.item_table.get_children():
                self.item_table.delete(item)
            for row in search_item(search_val):
                self.item_table.insert("",tk.END,values=row)


        def as_tab(self):
            return self.rootframe

        def close_win(self,top):
            top.destroy()

        def get_order_data(self,e1,e2,e3,top):
            item_num = int(e1.get())
            item_name = e2.get()
            qty = int(e3.get())
            place_order(item_num, item_name, qty)
            self.close_win(top)
            o.show_table()

        def add_item_data(self,e1,e2,e3,e4,e5,top):
            item_num = int(e1.get())
            item_name = e2.get()
            qty = int(e3.get())
            amt = int(e4.get())
            item_desc = e5.get()
            addItemtoDB(item_num, item_name, qty,amt,item_desc)
            self.close_win(top)
            i.show_table()
            
        
        def addItemBox(self):
            top= tk.Toplevel(root)
            top.geometry("750x350")
            rootframe = ttk.Frame(top)
            rootframe.pack(fill='both', expand=1)
            grid_config(rootframe)

            l1 = ttk.Label(rootframe, text="Item Id",style='small.TLabel')
            l1.grid(row=0, column=0, padx=6, pady=2, sticky="sw")

            e1 = ttk.Entry(rootframe)
            e1.grid(row=1, column=0, padx=6, pady=2, sticky="sew",columnspan=8)

            l2 = ttk.Label(rootframe, text=f"Item Name",style='small.TLabel')
            l2.grid(row=2, column=0, padx=6, pady=2, sticky="sw")

            e2 = ttk.Entry(rootframe)
            e2.grid(row=3, column=0, padx=6, pady=2, sticky="sew",columnspan=8)

            l3 = ttk.Label(rootframe, text='Quantity',style='small.TLabel')
            l3.grid(row=4, column=0, padx=6, pady=2, sticky="sw")

            e3 = ttk.Entry(rootframe)
            e3.grid(row=5, column=0, padx=6, pady=2, sticky="sew",columnspan=8)

            l4 = ttk.Label(rootframe, text='Amount',style='small.TLabel')
            l4.grid(row=6, column=0, padx=6, pady=2, sticky="sw")

            e4 = ttk.Entry(rootframe)
            e4.grid(row=7, column=0, padx=6, pady=2, sticky="sew",columnspan=8)

            l5 = ttk.Label(rootframe, text='Item Description',style='small.TLabel')
            l5.grid(row=8, column=0, padx=6, pady=2, sticky="sw")

            e5 = ttk.Entry(rootframe)
            e5.grid(row=9, column=0, padx=6, pady=2, sticky="sew",columnspan=8)

            confirm_row_btn = ttk.Button(rootframe, text='Confirm', style="accent.TButton",command= lambda : self.add_item_data(e1,e2,e3,e4,e5,top))
            confirm_row_btn.grid(row=10, column=0, padx=10,pady=6,sticky='sew')

            cancel_button = ttk.Button(rootframe, text='Cancel', style="accent.TButton",command= lambda : self.close_win(top))
            cancel_button.grid(row=11, column=5, padx=10,pady=6,sticky='sew')

        def delete_item_data(self,item_id,top):
            deleteItemfromDB(item_id)
            self.close_win(top)
            i.show_table()
            o.show_table()

        def deleteItemBox(self):
            top= tk.Toplevel(root)
            top.geometry("750x250")
            rootframe = ttk.Frame(top)
            rootframe.pack(fill='both', expand=1)
            grid_config(rootframe)

            selectedItem = self.item_table.selection()[0]
            item_id = self.item_table.item(selectedItem)['values'][0]

            l1 = ttk.Label(rootframe, text="Do you want to delete item?",style='small.TLabel')
            l1.grid(row=0, column=0, padx=6, pady=2, sticky="sw",columnspan=6)

            confirm_row_btn = ttk.Button(rootframe, text='Yes', style="accent.TButton",command= lambda : self.delete_item_data(item_id,top))
            confirm_row_btn.grid(row=7, column=0, padx=10,pady=6,sticky='sew',columnspan=2)

            cancel_button = ttk.Button(rootframe, text='No', style="accent.TButton",command= lambda : self.close_win(top))
            cancel_button.grid(row=7, column=2, padx=10,pady=6,sticky='sew',columnspan=2)


        def placeOrderBox(self):
            top= tk.Toplevel(root)
            top.geometry("750x250")
            rootframe = ttk.Frame(top)
            rootframe.pack(fill='both', expand=1)
            grid_config(rootframe)

            selectedItem = self.item_table.selection()[0]
            item_id = self.item_table.item(selectedItem)['values'][0]
            item_name = self.item_table.item(selectedItem)['values'][1]

            l1 = ttk.Label(rootframe, text="Item Id",style='small.TLabel')
            l1.grid(row=0, column=0, padx=6, pady=2, sticky="sw")

            e1 = ttk.Entry(rootframe)
            e1.insert(0,item_id)
            e1.grid(row=1, column=0, padx=6, pady=2, sticky="sew",columnspan=8)

            l2 = ttk.Label(rootframe, text=f"Item Name",style='small.TLabel')
            l2.grid(row=2, column=0, padx=6, pady=2, sticky="sw")

            e2 = ttk.Entry(rootframe)
            e2.insert(0,item_name)
            e2.grid(row=3, column=0, padx=6, pady=2, sticky="sew",columnspan=8)

            l3 = ttk.Label(rootframe, text='Quantity',style='small.TLabel')
            l3.grid(row=4, column=0, padx=6, pady=2, sticky="sw")

            e3 = ttk.Entry(rootframe)
            e3.grid(row=5, column=0, padx=6, pady=2, sticky="sew",columnspan=8)

            confirm_row_btn = ttk.Button(rootframe, text='Confirm', style="accent.TButton",command= lambda : self.get_order_data(e1,e2,e3,top))
            confirm_row_btn.grid(row=7, column=0, padx=10,pady=6,sticky='sew')

            cancel_button = ttk.Button(rootframe, text='Cancel', style="accent.TButton",command= lambda : self.close_win(top))
            cancel_button.grid(row=7, column=5, padx=10,pady=6,sticky='sew')


    
    root = tk.Toplevel()
    note = VerticalNavMenu(root, menu_button=True)
    o = inventory_order_page(note.content_frame, root)
    i = item_page(note.content_frame, root)
    note.add(o.as_tab(), text="Inventory Orders")
    note.add(i.as_tab(), text="Items")
    note.pack(fill="both", expand=1)
    root.wm_protocol('WM_DELETE_WINDOW', root_main.destroy)
    root.mainloop()
    