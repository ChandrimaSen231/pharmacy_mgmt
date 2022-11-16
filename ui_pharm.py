from tkinter import ttk
import tkinter as tk
import datetime
from pharmacy_backend import *
from theme import style
from ui_utils import *

def main(root_main):
    


    class pos_page:
        def __init__(self, master, root_window):
            self.rootframe = ttk.Frame(master)
            self.rootframe.pack(fill="both", expand=1)

            self.menu = HorizontalNavMenu(self.rootframe)

            # customer details
            self.customer_details_page = ttk.Frame(self.menu.content_frame)
            grid_config(self.customer_details_page)

            self.cust_reg_lbl = ttk.Label(
                self.customer_details_page, text="Customer Details", style="big.TLabel"
            )
            self.cust_reg_lbl.grid(
                row=0, column=0, columnspan=8, padx=10, pady=6, sticky="nswe"
            )

            l2 = ttk.Label(
                self.customer_details_page, text="Phone Number", style="small.TLabel"
            )
            l2.grid(row=1, column=0, padx=10, pady=4, sticky="sw")

            self.cust_phone_number_entry = ttk.Entry(self.customer_details_page, style='Table.TEntry')
            self.cust_phone_number_entry.grid(
                row=2, column=0, padx=10, pady=4, columnspan=6, sticky="nswe"
            )
            self.cust_search_btn = ttk.Button(
                self.customer_details_page,
                text="Search",
                command=self.search_by_ph_no
            )
            self.cust_search_btn.grid(
                row=2, column=6, columnspan=2, padx=10, pady=4, sticky="swe"
            )
            l1 = ttk.Label(
                self.customer_details_page, text="Customer Name", style="small.TLabel"
            )
            l1.grid(row=3, column=0, padx=10, pady=4, sticky="sw")

            self.cust_name_entry = ttk.Entry(self.customer_details_page)
            self.cust_name_entry.grid(
                row=4, column=0, padx=10, pady=4, columnspan=8, sticky="nswe"
            )

            l3 = ttk.Label(self.customer_details_page, text="Age", style="small.TLabel")
            l3.grid(row=5, column=0, padx=10, pady=4, sticky="sw")

            self.cust_age_entry = ttk.Entry(self.customer_details_page)
            self.cust_age_entry.grid(
                row=6, column=0, padx=10, pady=4, columnspan=3, sticky="nswe"
            )

            l4 = ttk.Label(self.customer_details_page, text="Sex", style="small.TLabel")
            l4.grid(row=5, column=4, padx=10, pady=4, sticky="sw")

            self.cust_sex_entry = ttk.Entry(self.customer_details_page)
            self.cust_sex_entry.grid(
                row=6, column=4, padx=10, pady=4, columnspan=4, sticky="nswe"
            )

            l5 = ttk.Label(self.customer_details_page, text="Address", style="small.TLabel")
            l5.grid(row=7, column=0, padx=10, pady=4, sticky="sw")

            self.cust_addr_entry = ttk.Entry(self.customer_details_page)
            self.cust_addr_entry.grid(
                row=8, column=0, padx=10, pady=4, columnspan=8, sticky="nswe"
            )

            self.new_cust_reg_btn = ttk.Button(
                self.customer_details_page,
                text="Register New Customer",
                style="accent.TButton",
                command=self.reg_new_cust,
                state=tk.DISABLED,
            )
            self.new_cust_reg_btn.grid(
                row=9, column=0, columnspan=4, padx=10, pady=6, sticky="swe"
            )

            self.new_cust_warn_label = ttk.Label(
                self.customer_details_page,
                text="Customer not found! Register new customer",
                style="accent.TLabel",
            )
            self.new_cust_reg_btn.grid(
                row=9,
                column=0,
                columnspan=4,
                ipadx=6,
                ipady=6,
                padx=10,
                pady=6,
                sticky="swe",
            )
            hide_grid_widget(self.new_cust_warn_label)

            #########################
            # Medicine Details Page #
            #########################
            self.medicine_details_page = ttk.Frame(self.menu.content_frame)
            grid_config(self.medicine_details_page)

            l1 = ttk.Label(
                self.medicine_details_page, text="Medicine Name", style="small.TLabel"
            )
            l1.grid(row=0, column=0, padx=10, pady=4, sticky="sw")

            self.med_name_combo = ttk.Combobox(self.medicine_details_page)
            self.med_name_combo.grid(
                row=1, column=0, padx=10, pady=4, columnspan=7, sticky="ew"
            )
            rows = search_med_by_name()
            self.combo_lst = [val[0] for val in rows]
            self.med_name_combo['values'] = self.combo_lst
            self.med_name_combo.bind('<KeyRelease>', self.check_input)

            
            l2 = ttk.Label(
                self.medicine_details_page, text="Quantity", style="small.TLabel"
            )
            l2.grid(row=2, column=0, padx=10, pady=4, sticky="sw")

            self.qty_entry = ttk.Entry(self.medicine_details_page)
            self.qty_entry.grid(
                row=3, column=0, padx=10, pady=4, columnspan=6, sticky="sew"
            )
            self.med_search_btn = ttk.Button(
                self.medicine_details_page,
                text="Check availability",
                command = lambda : self.check_availability(self.med_name_combo,self.qty_entry)
            )

            self.med_search_btn.grid(row=3, column=6, padx=10, pady=4, sticky="ne")


            self.add_sel_btn = ttk.Button(
                self.medicine_details_page, text="Add Selected", style="accent.TButton",state=tk.DISABLED,
                command = lambda : self.add_item(self.med_name_combo,self.qty_entry)
            )
            self.add_sel_btn.grid(
                row=4, column=0, padx=10, pady=8, columnspan=8, sticky="ew"
            )

            self.qty_entry.bind('<FocusIn>',self.disable)

            self.med_table = easy_treeview(
                self.medicine_details_page, columns=["Medicine", "Quantity"]
            )
            self.med_table.grid(
                row=5,
                column=0,
                padx=10,
                pady=10,
                columnspan=8,
                ipadx=6,
                ipady=4,
                sticky="nswe",
            )
            self.med_table.bind("<<TreeviewSelect>>",self.selected_item)

            self.delete_row_btn = ttk.Button(self.medicine_details_page, text='- Delete item',command= self.delete_item, state=tk.DISABLED)
            self.delete_row_btn.grid(row=7, column=0, padx=10,pady=6,sticky='w')

            #########################
            # Payment Details Page #
            #########################
            self.payment_details_page = ttk.Frame(self.menu.content_frame)
            grid_config(self.payment_details_page)

            l1 = ttk.Label(
                self.payment_details_page, text="Payment Date", style="small.TLabel"
            )
            l1.grid(row=0, column=0, padx=10, pady=4, sticky="sw")

            self.datetime_entry = ttk.Entry(self.payment_details_page)
            self.datetime_entry.grid(
                row=1, column=0, padx=10, pady=4, columnspan=5, sticky="ew"
            )

            self.ct_btn = ttk.Button(
                self.payment_details_page,
                text="Insert Current Date",
                command=lambda: self.datetime_entry.insert(
                    "0", str(datetime.datetime.now().date())
                ),
            )
            self.ct_btn.grid(row=1, column=6, columnspan=3, padx=10, pady=4, sticky="new")

            self.gen_recpt = ttk.Button(
                self.payment_details_page, text="Generate Receipt", style="accent.TButton",command=self.generate_reciept
            )
            self.gen_recpt.grid(row=3, column=0, padx=10, pady=8, columnspan=8, sticky="ew")

            var = tk.StringVar()
            self.payment_method_menu = ttk.OptionMenu(
                self.payment_details_page, var, *["Cash", "Credit/Debit Card", "UPI"]
            )
            # self.payment_method_menu.config()
            self.payment_method_menu.grid(
                row=2, column=0, padx=10, pady=8, columnspan=8, sticky="ew"
            )

            self.menu.add(self.customer_details_page, text="Customer Details")
            self.menu.add(self.medicine_details_page, text="Medicines")
            self.menu.add(self.payment_details_page, text="Payment")
            self.menu.pack(fill="both", expand=1, padx=10)

            # Pagination
            self.n_btn = ttk.Button(
                master=self.rootframe,
                text="Next >",
                command=self.menu.next_page,
                style="borderless.TButton",
            )
            self.n_btn.pack(side="right", anchor="se", padx=24, pady=10)

            self.b_btn = ttk.Button(
                master=self.rootframe,
                text="< Back",
                command=self.menu.prev_page,
                style="borderless.TButton",
            )
            self.b_btn.pack(side="left", anchor="sw", padx=24, pady=10)

        def disable(self,a):
            self.add_sel_btn.config(state=tk.DISABLED)

        def selected_item(self,a):
            self.delete_row_btn.config(state=tk.NORMAL)

        def check_input(self,event):
            value = event.widget.get()

            if value == '':
                self.med_name_combo['values'] = self.combo_lst
            else:
                data = []
                for item in self.combo_lst:
                    if value.lower() in item.lower():
                        data.append(item)

                self.med_name_combo['values'] = data

        def check_availability(self,e1,e2):
            med_name = e1.get()
            qty = int(e2.get())
            if check_med_availability(med_name,qty):
                self.add_sel_btn.config(state=tk.NORMAL)
            else:
                self.add_sel_btn.config(state=tk.DISABLED)

        def add_item(self,e1,e2):
            row = [e1.get(),e2.get()]
            self.med_table.insert("",tk.END,values=row)
            self.add_sel_btn.config(state=tk.DISABLED)
            self.show_amt()

        def delete_item(self):
            selected_items = self.med_table.selection()        
            for selected_item in selected_items:          
                self.med_table.delete(selected_item)
            self.show_amt()

        def display_cust_data(self, data):
            self.cust_name_entry.insert(tk.END, data[1])
            self.cust_age_entry.insert(tk.END, data[2])
            self.cust_sex_entry.insert(tk.END, data[3])
            self.cust_addr_entry.insert(tk.END, data[4])

        def show_error_dialog(self):
            tk.messagebox.showinfo("Error","Fields cannot be blank")

        def reg_new_cust(self):
            data = {}
            if self.cust_name_entry.get() == "" or self.cust_age_entry.get() == "" or self.cust_sex_entry.get() == ""or self.cust_addr_entry.get() == "":
                self.show_error_dialog()
            else:
                data["name"] = self.cust_name_entry.get()
                data["age"] = self.cust_age_entry.get()
                data["sex"] = self.cust_sex_entry.get()
                data["address"] = self.cust_addr_entry.get()
                data["phone_no"] = self.cust_phone_number_entry.get()
                insert_from_dict(customers, data)
                self.cust_name_entry.delete(0,tk.END)
                self.cust_age_entry.delete(0,tk.END)
                self.cust_sex_entry.delete(0,tk.END)
                self.cust_addr_entry.delete(0,tk.END)
                self.cust_phone_number_entry.delete(0,tk.END)
                self.new_cust_reg_btn.config(state=tk.DISABLED)

        def customer_notfound(self):
            tk.messagebox.showinfo("Error","Customer Not Found")

        def search_by_ph_no(self):
            self.cust_name_entry.delete(0,tk.END)
            self.cust_age_entry.delete(0,tk.END)
            self.cust_sex_entry.delete(0,tk.END)
            self.cust_addr_entry.delete(0,tk.END)
            ph_no = int(self.cust_phone_number_entry.get())
            data = search_cust_by_phone_no(ph_no)
            if data == None:
                self.customer_notfound()
                self.new_cust_reg_btn.config(state=tk.NORMAL)
                
            else:
                self.display_cust_data(data)

        def show_amt(self):
            med_list = []
            
            for row in self.med_table.get_children():
                med_list.append((self.med_table.item(row)['values'][0],self.med_table.item(row)['values'][1]))

            amt,_ = get_amount(med_list)
            amt_lbl = ttk.Label(self.medicine_details_page, text=f"Total amount: {amt}", style="small.TLabel"
            )
            amt_lbl.grid(row=7, column=6, padx=10, pady=4, sticky="sw")
        
        def generate_reciept(self):
            med_list = []
            
            for row in self.med_table.get_children():
                med_list.append((self.med_table.item(row)['values'][0],self.med_table.item(row)['values'][1]))
            purchase_med(med_list)
            get_reciept(self.cust_name_entry.get(),self.cust_age_entry.get(),self.cust_sex_entry.get(),self.datetime_entry.get(),med_list)
            self.cust_name_entry.delete(0,tk.END)
            self.cust_age_entry.delete(0,tk.END)
            self.cust_sex_entry.delete(0,tk.END)
            self.cust_addr_entry.delete(0,tk.END)
            self.cust_phone_number_entry.delete(0,tk.END)
            self.customer_details_page.pack(fill='both',expand=1)
            self.payment_details_page.pack_forget()

        def as_tab(self):
            return self.rootframe


    class about_page:
        def __init__(self, master, root_window):
            self.root_window = root_window
            self.rootframe = ttk.Frame(master)
            l0 = ttk.Label(self.rootframe, text="About", style="big.TLabel")
            l0.pack(padx=20, pady=15, anchor="n", expand=1)
            l1 = ttk.Label(
                self.rootframe,
                text="Made by Subhrojyoti Sen.",
            )
            l1.pack(padx=20, pady=5, anchor="n", expand=1)
            l2 = ttk.Label(
                self.rootframe, text="drugs are illegal.", style="small.TLabel"
            )
            l2.pack(padx=20, pady=5, anchor="n", expand=1)
            quit_btn = ttk.Button(self.rootframe, text="Quit", command=self.quit_app)
            quit_btn.pack(padx=20, pady=10, anchor="center")

        def quit_app(self):
            close()
            self.root_window.destroy()
            exit()

        def as_tab(self):
            return self.rootframe

    
    


    
    root = tk.Toplevel(root_main)
    note = VerticalNavMenu(root, menu_button=True)
    p = pos_page(note.content_frame, root_window=root)
    abt = about_page(master=note.content_frame, root_window=root)
    note.add(p.as_tab(), text="Point-Of-Sale")
    note.add(abt.as_tab(), text="About")
    note.add(ttk.Frame(), text="Quit", custom_cmd=abt.quit_app)
    note.pack(fill="both", expand=1)
    root.wm_protocol('WM_DELETE_WINDOW', root_main.destroy)
    root.mainloop()
    
