from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime

import sqlite3

class StockManagement:
    def __init__(self):
        self.db = sqlite3.connect('stock.db')
        self.cursor = self.db.cursor()        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock
                            (id PRIMARY KEY,
                            name TEXT,
                            quantity TEXT,
                            price TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales
                            (id PRIMARY KEY,
                            name TEXT,
                            quantity TEXT,
                            price TEXT,
                            total TEXT)''')        
        self.run()
    
    def add_stock_submit(self):
        self.cursor.execute("INSERT INTO stock (id, name, quantity, price) VALUES ('{}','{}','{}','{}')".format(
            self.add_stock_id_entry.get(),
            self.add_stock_name_entry.get(),
            self.add_stock_quantity_entry.get(), 
            self.add_stock_price_entry.get()))
        self.db.commit()
        self.add_stock.destroy()
        messagebox.showinfo("Success", "Stock added successfully")

    def add_stock_window(self):
        self.add_stock = Toplevel(self.root)
        self.add_stock.title("Add Stock")
        self.add_stock.geometry("500x500")
        self.add_stock.resizable(False, False)

        add_stock_name = Label(self.add_stock, text="Name: ")
        add_stock_name.place(relx=0.1, rely=0.1)

        self.add_stock_name_entry = Entry(self.add_stock, width=45)
        self.add_stock_name_entry.place(relx=0.1, rely=0.15)

        add_stock_quantity = Label(self.add_stock, text="Quantity: ")
        add_stock_quantity.place(relx=0.1, rely=0.2)

        self.add_stock_quantity_entry = Entry(self.add_stock, width=45)
        self.add_stock_quantity_entry.place(relx=0.1, rely=0.25)

        add_stock_price = Label(self.add_stock, text="Price: ")
        add_stock_price.place(relx=0.1, rely=0.3)

        self.add_stock_price_entry = Entry(self.add_stock, width=45)
        self.add_stock_price_entry.place(relx=0.1, rely=0.35)        

        add_stock_id = Label(self.add_stock, text="ID: ")
        add_stock_id.place(relx=0.1, rely=0.4)
        
        self.add_stock_id_entry = Entry(self.add_stock, width=45 )
        self.add_stock_id_entry.place(relx=0.1, rely=0.45)

        self.add_stock_submit = Button(self.add_stock, text="Submit", command=self.add_stock_submit, width=10, height=1,bg='black',fg='white',font= ('Arial', 9, 'bold'))
        self.add_stock_submit.place(relx=0.1, rely=0.55)
    

    def add_sales_submit(self):
        if int(self.add_sales_quantity_entry.get()) <= int(self.data[0][2]):        
            self.cursor.execute("INSERT INTO sales (id, name, quantity, price, total) VALUES ('{}','{}','{}','{}','{}')".format(
                datetime.datetime.now().strftime("%Y%m%d%H%M%S"), self.add_sales_name_entry.get(),self.add_sales_quantity_entry.get(), self.add_sales_price_entry.get(),
                int(self.add_sales_quantity_entry.get()) * int(self.add_sales_price_entry.get())))
            self.cursor.execute("UPDATE stock SET quantity = quantity - {} WHERE name = '{}'".format(self.add_sales_quantity_entry.get(), self.add_sales_name_entry.get()))
            self.db.commit()
            self.add_sales.destroy()
            messagebox.showinfo("Success", "Sales added successfully")
        else:
            messagebox.showinfo("Error", "Quantity is greater than available stock")
        
        
    def salesidmenu(self,args):
        self.stockid = args
        self.data = self.cursor.execute("SELECT * FROM stock WHERE id='{}'".format(self.stockid)).fetchall()
        
        self.add_sales_name_entry.delete(0, END)
        self.add_sales_price_entry.delete(0 , END)

        self.add_sales_name_entry.insert(0, self.data[0][1])
        self.add_sales_quantity_label.config(text= "Quantity: [{}]".format(self.data[0][2]))
        self.add_sales_price_entry.insert(0, self.data[0][3])
        

    def add_sales_window(self):
        self.add_sales = Toplevel(self.root)
        self.add_sales.title("Add Sales")
        self.add_sales.geometry("500x500")
        self.add_sales.resizable(False, False)

        # Stock OptionMenu
        self.add_sales_id_label = Label(self.add_sales, text="ID: ")
        self.add_sales_id_label.place(relx=0.1, rely=0.1)

        self.stock_id_list = []
        for x in self.cursor.execute("SELECT * FROM stock").fetchall():
            self.stock_id_list.append(x[0])

        self.add_sales_id_entry = StringVar(self.add_sales)
        self.add_sales_id_entry.set("Select")

        self.add_sales_id_option_menu = OptionMenu(self.add_sales, self.add_sales_id_entry, *self.stock_id_list , command=self.salesidmenu)
        self.add_sales_id_option_menu.place(relx=0.1, rely=0.15)

        self.add_sales_name_label = Label(self.add_sales, text="Name: ")
        self.add_sales_name_label.place(relx=0.1, rely=0.2)

        self.add_sales_name_entry = Entry(self.add_sales, width=45)
        self.add_sales_name_entry.place(relx=0.1, rely=0.25)

        self.add_sales_quantity_label = Label(self.add_sales, text="Quantity: ")
        self.add_sales_quantity_label.place(relx=0.1, rely=0.3)

        self.add_sales_quantity_entry = Entry(self.add_sales, width=45)
        self.add_sales_quantity_entry.place(relx=0.1, rely=0.35)

        self.add_sales_price_label = Label(self.add_sales, text="Price: ")
        self.add_sales_price_label.place(relx=0.1, rely=0.4)

        self.add_sales_price_entry = Entry(self.add_sales, width=45)
        self.add_sales_price_entry.place(relx=0.1, rely=0.45)

    
        self.add_sales_submit = Button(self.add_sales, text="Submit", command=self.add_sales_submit, width=10, height=1,bg='black',fg='white',font= ('Arial', 9, 'bold'))
        self.add_sales_submit.place(relx=0.1, rely=0.55)
        

    def view_sales_window(self):        
        self.view_sales = Toplevel(self.root)
        self.view_sales.title("View Sales")
        self.view_sales.resizable(False, False)

        self.view_sales_tree = ttk.Treeview(self.view_sales, columns=('id', 'name', 'quantity', 'price', 'total'))        
        self.view_sales_tree.heading('id', text='id')
        self.view_sales_tree.heading('name', text='name')
        self.view_sales_tree.heading('quantity', text='quantity')
        self.view_sales_tree.heading('price', text='price')
        self.view_sales_tree.heading('total', text='total')
        
        for x in self.cursor.execute("SELECT * FROM sales").fetchall():
            self.view_sales_tree.insert('', 'end', values=(x[0], x[1], x[2], x[3], x[4]))

        self.view_sales_tree.pack()

        scrollbar = Scrollbar(self.view_sales , orient=HORIZONTAL, command=self.view_sales_tree.xview)
        self.view_sales_tree.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side=BOTTOM, fill=X)

    def view_stock_window(self):
        self.view_stock = Toplevel(self.root)
        self.view_stock.title("View Stock")        
        self.view_stock.resizable(False, False)

        self.view_tree = ttk.Treeview(self.view_stock, columns=('id', 'name', 'quantity', 'price'))
        self.view_tree.heading('id', text='id')
        self.view_tree.heading('name', text='name')
        self.view_tree.heading('quantity', text='quantity')
        self.view_tree.heading('price', text='price')

        data = self.cursor.execute('SELECT * FROM stock').fetchall()
        for x in data:         
            self.view_tree.insert('', 'end', values=(x[0], x[1], x[2], x[3]))
        self.view_tree.pack() 
        scrollbar = ttk.Scrollbar(self.view_stock, orient=HORIZONTAL, command=self.view_tree.xview)
        self.view_tree.configure(xscroll=scrollbar.set)
        scrollbar.pack(side=BOTTOM, fill=X)

        self.view_stock.mainloop()

    
    def menu_window(self):
        if self.username.get() == self.password.get() == 'admin':        
            self.root.wm_state('iconic')
            self.menu = Toplevel(self.root)
            self.menu.title("Menu")
            self.menu.geometry("500x500")
            self.menu.resizable(False, False)

            self.add_stock = Button(self.menu, text="Add Stock", command=self.add_stock_window, width=60, height=6,bg='black',fg='orange',font= ('Arial', 9, 'bold'))
            self.add_stock.place(relx=0.06, rely=0.05)

            self.view_stock = Button(self.menu, text="View Stock", command=self.view_stock_window, width=60, height=6,bg='black',fg='orange',font= ('Arial', 9, 'bold'))
            self.view_stock.place(relx=0.06, rely=0.25)

            self.add_sales = Button(self.menu, text="Add Sales", command=self.add_sales_window, width=60, height=6,bg='black',fg='white',font= ('Arial', 9, 'bold'))
            self.add_sales.place(relx=0.06, rely=0.45)

            self.view_sales = Button(self.menu, text="View Sales", command=self.view_sales_window, width=60, height=6,bg='black',fg='white',font= ('Arial', 9, 'bold'))
            self.view_sales.place(relx=0.06, rely=0.65)
        else:
            messagebox.showerror("Error", "Incorrect username or password")


    def run(self):
        self.root = Tk()
        self.root.title("Stock Management")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        usernamelabel = Label(self.root, text="Username: ")
        usernamelabel.place(relx=0.1, rely=0.1)    

        self.username = Entry(self.root , width=45)
        self.username.place(relx=0.1, rely=0.2)

        passwordlabel = Label(self.root, text="Password: ")
        passwordlabel.place(relx=0.1, rely=0.35)

        self.password = Entry(self.root, show="*", width=45)
        self.password.place(relx=0.1, rely=0.45)

        loginbutton = Button(self.root, text="Login", command=self.menu_window)
        loginbutton.place(relx=0.1, rely=0.6)

        self.root.mainloop()


StockManagement()