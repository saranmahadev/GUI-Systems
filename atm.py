from tkinter import messagebox
from tkinter import *
import sqlite3

class User:
    def __init__(self):
        self.db = sqlite3.connect('atm.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, cardtype TEXT, amount TEXT, acc_no TEXT)")
        self.run()        

    def withdraw(self):
        data = self.cursor.execute("SELECT * FROM users WHERE acc_no='{}'".format(self.atmaccountno.get())).fetchall()
        totamt = int(data[0][3])
        wamt = int(self.atmamount.get())
        if self.atmpin.get() == data[0][1]:
            if totamt < wamt:
                messagebox.showerror("Error","Insufficient Balance")
            else:
                query = "UPDATE users SET amount='{}' WHERE acc_no='{}'".format(totamt-wamt,self.atmaccountno.get())
                self.cursor.execute(query)
                self.db.commit()
                messagebox.showinfo("Success","Withdrawal Successful")            
        else:
            messagebox.showerror("Error","Incorrect PIN")
        self.atmaccountno.delete(0,END)
        self.atmpin.delete(0,END)
        self.atmamount.delete(0,END)
        self.atm.focus()            

    def add(self):
        self.cursor.execute("INSERT INTO users(username,password,cardtype,amount,acc_no) VALUES(?,?,?,?,?)",
        (self.name.get(),self.pin.get(),self.cardtype.get(),self.amount.get(),self.acc_no.get()))
        self.db.commit()
        messagebox.showinfo("Success","Account Created")
        self.admin.destroy()        
        self.adminaccess()
    
    def edit(self):
        query = "UPDATE users SET username='{}', password='{}', cardtype='{}', amount='{}' WHERE acc_no='{}'".format(self.editname.get(),self.editpin.get(),self.editcardtype.get(),self.editamount.get(),self.id)
        self.cursor.execute(query)
        self.db.commit()        
        messagebox.showinfo("Success","Account Updated")
        self.admin.focus()

    def delete(self):
        try:
            self.cursor.execute("DELETE FROM users WHERE acc_no ='{}'".format(self.id))
            messagebox.showinfo("Success","Account Deleted")  
            self.admin.destroy()
            self.root.wm_state('normal')
        except:
            messagebox.showerror("Error","Please select an account to delete")
    
    def menu_ops(self,args):                
        data = self.cursor.execute("SELECT * FROM users WHERE acc_no = ?",(args[0],)).fetchall()        
        try:
            print(self.id)
        except:
            self.id = args[0]

        if self.id == args[0]:
            if len(self.editname.get()) == 0:
                self.id = self.id
                self.editname.insert(0,data[0][0])
                self.editpin.insert(0,data[0][1])
                self.editcardtype.insert(0,data[0][2])
                self.editamount.insert(0,data[0][3])
        else:
            self.editname.delete(0,END)
            self.editpin.delete(0,END)
            self.editcardtype.delete(0,END)
            self.editamount.delete(0,END)
            self.editname.insert(0,data[0][0])
            self.editpin.insert(0,data[0][1])
            self.editcardtype.insert(0,data[0][2])
            self.editamount.insert(0,data[0][3])
            self.id = args[0]
    
    def allusers(self):
        self.allusers = Toplevel(self.root)
        self.allusers.resizable(False,False)
        self.allusers.title("All Users")

        self.table = Label(self.allusers, text="Username")
        self.table.grid(row=1, column=0)

        self.table = Label(self.allusers, text="Password")
        self.table.grid(row=1, column=1)

        self.table = Label(self.allusers, text="Card Type")
        self.table.grid(row=1, column=2)

        self.table = Label(self.allusers, text="Amount")
        self.table.grid(row=1, column=3)

        self.table = Label(self.allusers, text="Account Number")
        self.table.grid(row=1, column=4)

        self.cursor.execute("SELECT * FROM users")
        self.data = self.cursor.fetchall() 

        for i in range(len(self.data)):
            self.table = Label(self.allusers, text=self.data[i][0])
            self.table.grid(row=i+2, column=0)
        
            self.table = Label(self.allusers, text=self.data[i][1])
            self.table.grid(row=i+2, column=1)

            self.table = Label(self.allusers, text=self.data[i][2])
            self.table.grid(row=i+2, column=2)

            self.table = Label(self.allusers, text=self.data[i][3])
            self.table.grid(row=i+2, column=3)

            self.table = Label(self.allusers, text=self.data[i][4])
            self.table.grid(row=i+2, column=4)

        self.allusers.mainloop()

    def adminaccess(self):        
        if self.username.get() == 'admin' and self.password.get() == 'admin':            
            self.admin = Toplevel(self.root)
            self.admin.title("Admin | Logged In")
            
            self.root.wm_state('iconic')
            
            self.admin.resizable(False,False)
            self.admin.geometry("800x400")            
            
            namelabel = Label(self.admin,text = "Name")
            namelabel.place(relx = 0.1, rely = 0.1)

            self.name = Entry(self.admin, width = 40)
            self.name.place(relx = 0.1, rely = 0.16)

            pinlabel = Label(self.admin,text = "PIN")
            pinlabel.place(relx = 0.1, rely = 0.22)

            self.pin = Entry(self.admin, width = 40)
            self.pin.place(relx = 0.1, rely = 0.28)
            
            cardtype = Label(self.admin,text = "Card Type")
            cardtype.place(relx = 0.1, rely = 0.34)

            self.cardtype = Entry(self.admin, width = 40)
            self.cardtype.place(relx = 0.1, rely = 0.40)

            amountlabel = Label(self.admin,text = "Amount")
            amountlabel.place(relx = 0.1, rely = 0.46)

            self.amount = Entry(self.admin, width = 40)
            self.amount.place(relx = 0.1, rely = 0.52)
            
            acc_nolabel = Label(self.admin,text="Account Number")
            acc_nolabel.place(relx = 0.1, rely = 0.58)

            self.acc_no = Entry(self.admin, width = 40)
            self.acc_no.place(relx = 0.1, rely = 0.64)

            addbtn = Button(self.admin,text = "Add",command = self.add)
            addbtn.place(relx = 0.3, rely = 0.70)

            try:
                acclabel = Label(self.admin,text = "Select Account Number")
                acclabel.place(relx = 0.55, rely = 0.1)
            
                clicked = StringVar()
                clicked.set("SELCECT ACCOUNT NUMBER")
                
                data = self.cursor.execute("SELECT acc_no FROM users").fetchall()
                
                self.acclist = OptionMenu(self.admin,clicked, *data , command = self.menu_ops)            
                self.acclist.place(relx = 0.55, rely = 0.16)            

                editnamelabel = Label(self.admin , text="Name")
                editnamelabel.place(relx = 0.55, rely = 0.30)

                self.editname = Entry(self.admin, width = 40)
                self.editname.place(relx = 0.55, rely = 0.36)

                editpinlabel = Label(self.admin, text="PIN")
                editpinlabel.place(relx = 0.55, rely = 0.42)

                self.editpin = Entry(self.admin, width = 40)
                self.editpin.place(relx = 0.55, rely = 0.48)

                editcardtype = Label(self.admin, text="Card Type")
                editcardtype.place(relx = 0.55, rely = 0.54)

                self.editcardtype = Entry(self.admin, width = 40)
                self.editcardtype.place(relx = 0.55, rely = 0.60)

                editamountlabel = Label(self.admin, text="Amount")
                editamountlabel.place(relx = 0.55, rely = 0.66)
                
                self.editamount = Entry(self.admin, width = 40)
                self.editamount.place(relx = 0.55, rely = 0.72)

                editbtn = Button(self.admin, text="Update", command = self.edit)
                editbtn.place(relx = 0.55, rely = 0.78)

                deletebtn = Button(self.admin, text="Delete", command = self.delete)
                deletebtn.place(relx = 0.65, rely = 0.78)

                allusersbtn = Button(self.admin, text="All Users", command = self.allusers)
                allusersbtn.place(relx = 0.75, rely = 0.78)
            except:
                noaccountlabel = Label(self.admin, text="No Accounts Available")
                noaccountlabel.place(relx = 0.55, rely = 0.1)
            self.admin.mainloop()


    def atm(self):
        self.atm = Toplevel(self.root)
        self.atm.geometry("300x300")
        self.atm.resizable(False,False)
        self.atm.title("ATM")

        acclabel = Label(self.atm,text = "Account Number")
        acclabel.place(relx = 0.1 , rely = 0.1)

        self.atmaccountno = Entry(self.atm, width = 40)
        self.atmaccountno.place(relx = 0.1 , rely = 0.16)

        pinlabel = Label(self.atm,text = "PIN Number")
        pinlabel.place(relx = 0.1 , rely = 0.22)

        self.atmpin = Entry(self.atm , width = 40 , show='*')
        self.atmpin.place(relx=0.1,rely = 0.28)
        
        amountlabel = Label(self.atm,text = "Amount")
        amountlabel.place(relx = 0.1 , rely = 0.34)

        self.atmamount = Entry(self.atm , width = 40)
        self.atmamount.place(relx = 0.1, rely = 0.40)
        
        withdraw = Button(self.atm,text = "Withdraw" ,command= self.withdraw )
        withdraw.place(relx = 0.4,rely=0.46)

        self.atm.mainloop()

    def run(self):
        self.root = Tk()
        self.root.title("ADMIN LOGIN")
        self.root.geometry("400x400")
        self.root.resizable(False,False)

        usernamelabel = Label(self.root, text = "Username:")
        usernamelabel.place(relx = 0.1,rely = 0.1)

        self.username = Entry(self.root , width = 50)
        self.username.place(relx = 0.1,rely=0.16)

        passwordlabel = Label(self.root , text = "Password:")
        passwordlabel.place(relx = 0.1, rely = 0.22)

        self.password = Entry(self.root, width = 50, show='*')
        self.password.place(relx = 0.1, rely = 0.28)

        submit = Button(self.root,text = "Submit",command = self.adminaccess)
        submit.place(relx = 0.4 , rely = 0.34)

        atmbtn = Button(self.root,width = 40,text = "ATM", command = self.atm)
        atmbtn.place(relx = 0.1,rely = 0.45)

        self.root.mainloop()   
User()