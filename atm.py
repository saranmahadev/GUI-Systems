from tkinter import *

class User:
    def __init__(self):
        pass 
    
    def adminaccess(self):
        if self.username.get() == 'admin' and self.password.get() == 'admin':
            self.admin = Toplevel(self.root)
            self.admin.title("Logged In")
            self.admin.resizable(False,False)
            self.admin.geometry("400x400")            

            self.admin.mainloop()

    def atm(self):
        self.atm = Toplevel(self.root)
        self.atm.geometry("300x300")
        self.atm.resizable(False,False)
        self.atm.title("ATM")

        acclabel = Label(self.atm,text = "Account Number")
        acclabel.place(relx = 0.1 , rely = 0.1)

        self.accountno = Entry(self.atm, width = 40)
        self.accountno.place(relx = 0.1 , rely = 0.16)

        pinlabel = Label(self.atm,text = "PIN Number")
        pinlabel.place(relx = 0.1 , rely = 0.22)

        self.pin = Entry(self.atm , width = 40)
        self.pin.place(relx=0.1,rely = 0.28)
        
        amountlabel = Label(self.atm,text = "Amount")
        amountlabel.place(relx = 0.1 , rely = 0.34)

        self.amount = Entry(self.atm , width = 40)
        self.amount.place(relx = 0.1, rely = 0.40)
        
        withdraw = Button(self.atm,text = "Withdraw")
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

        self.password = Entry(self.root, width = 50)
        self.password.place(relx = 0.1, rely = 0.28)

        submit = Button(self.root,text = "Submit",command = self.adminaccess)
        submit.place(relx = 0.4 , rely = 0.34)

        atm = Button(self.root,width = 40,text = "ATM", command = self.atm)
        atm.place(relx = 0.1,rely = 0.45)

        self.root.mainloop()   


User().run()