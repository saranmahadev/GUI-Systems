from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class Conference:
    def __init__(self):
        self.db = sqlite3.connect("conference.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS participant(confid TEXT , name TEXT,clgname TEXT,clgaddress TEXT, dept TEXT, gender TEXT,mobile TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS college(name TEXT, id TEXT, address TEXT, username TEXT, password TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS advertisement(id TEXT,topic TEXT,clgid TEXT,clgname TEXT, clgaddress TEXT, dept TEXT, date TEXT, fees TEXT)""")
        self.run()

    def clgaddconf_submit(self):
        try:
            self.cursor.execute(
                """INSERT INTO advertisement(id,topic,clgid,clgname,clgaddress,dept,date,fees) VALUES(?,?,?,?,?,?,?,?)""",(
                    self.confid.get(), self.conftopic.get(), self.session[0][1], self.session[0][0], self.session[0][2], 
                    self.dept.get(), self.date.get(), self.fees.get()
                )
            )   
            self.db.commit()
            messagebox.showinfo("Success", "Conference Added Successfully")
            self.addconf_window.destroy()            
            self.clgwindow.destroy()
            self.refresh()
        except:
            messagebox.showerror("Error", "Conference Already Added")

    def clgaddconf(self):
        self.addconf_window = Toplevel(self.clgwindow)
        self.addconf_window.title("Add Conference")
        self.addconf_window.resizable(False,False)
        self.addconf_window.geometry("500x500")

        Label(self.addconf_window, text="Conference ID").place(relx = 0.1, rely = 0.1)

        self.confid = Entry(self.addconf_window, width = 53)
        self.confid.place(relx = 0.1, rely = 0.15)

        Label(self.addconf_window, text="Conference Topic").place(relx = 0.1, rely = 0.2)

        self.conftopic = Entry(self.addconf_window, width = 53)
        self.conftopic.place(relx = 0.1, rely = 0.25)

        Label(self.addconf_window, text="Department").place(relx = 0.1, rely = 0.3)

        self.dept = Entry(self.addconf_window, width = 53)
        self.dept.place(relx = 0.1, rely = 0.35)

        Label(self.addconf_window, text="Date").place(relx = 0.1, rely = 0.4)

        self.date = Entry(self.addconf_window, width = 53)
        self.date.place(relx = 0.1, rely = 0.45)

        Label(self.addconf_window, text="Fees").place(relx = 0.1, rely = 0.5)

        self.fees = Entry(self.addconf_window, width = 53)
        self.fees.place(relx = 0.1, rely = 0.55)

        Button(self.addconf_window, text="Add Conference", width = 15, command = self.clgaddconf_submit).place(relx = 0.1, rely = 0.6)

    def partable(self,args):
        self.confid = args[0]             
        table = ttk.Treeview(
            self.clgwindow, 
            height = 10, 
            columns = ("ID","Name", "College Name", "College Address", "Department", "Gender", "Mobile")
        )
        table.heading("ID",text="ID")
        table.heading("Name",text="Name")
        table.heading("College Name", text="College Name")
        table.heading("College Address" , text="College Address")
        table.heading("Department", text="Department")
        table.heading("Gender", text="Gender")
        table.heading("Mobile", text="Mobile")

        table.column('#0',width=0)
        table.column('#1',width=50)
        table.column("#2", width= 100)
        table.column("#3", width= 100)
        table.column("#4", width= 100)
        table.column("#5", width= 100)
        table.column("#6", width= 70)
        table.column("#7", width= 100)

        table.place(relx=0.05,rely=0.2)

        for x in self.cursor.execute("""SELECT * FROM participant WHERE confid = ? """,(self.confid,)):
            table.insert("",END,values=x)
        
        xscroll = ttk.Scrollbar(table, orient=HORIZONTAL, command=table.xview)
        xscroll.place(relx=0.05,rely=0.9,relwidth=0.9)
        table.configure(xscrollcommand=xscroll.set)

        yscroll = ttk.Scrollbar(table, orient=VERTICAL, command=table.yview)
        yscroll.place(relx=0.95,rely=0.2,relheight=0.7)
        table.configure(yscrollcommand=yscroll.set)

        
        

    def clglogin(self):
        data = self.cursor.execute("""SELECT * FROM college WHERE username = ? AND password = ?""", (
            self.clgusername_entry.get(), self.clgpassword_entry.get())
        ).fetchall()

        if data == []:
            messagebox.showerror("Error", "Invalid Username or Password")
        else:
            self.session = data
            self.clgwindow = Toplevel(self.root)
            self.clgwindow.title("{} | Admin".format(data[0][0]))
            self.clgwindow.resizable(False,False)
            self.clgwindow.geometry("700x500")

            Button(self.clgwindow, text="Add Conference", width = 15, command = self.clgaddconf).place(relx = 0.1, rely = 0.1)

            try:
                var = StringVar(self.clgwindow)
                var.set("Select Conference")
                self.conf = OptionMenu(
                    self.clgwindow, 
                    var, 
                    *self.cursor.execute("""SELECT id FROM advertisement WHERE clgid = ?""", (self.session[0][1],)).fetchall(),
                    command=self.partable
                )
                self.conf.place(relx = 0.7, rely = 0.1)
                
            except:
                pass
            

    def participant_registration_submit(self):
        self.cursor.execute(
            """INSERT INTO participant(confid,name,clgname,clgaddress,dept,gender,mobile) VALUES(?,?,?,?,?,?,?)""",(
                self.parconfid,
                self.parname.get(),
                self.parclgname.get(),
                self.parclgaddress.get(),
                self.pardept.get(),
                self.pargender.get(),
                self.parmobile.get()
            )
        )
        self.db.commit()
        messagebox.showinfo("Success", "Participant Registered Successfully")
        self.participantreg_window.destroy()

    def parregmenu(self,args):
        self.parconfid = args[0]

    def participant_registration(self):
        self.participantreg_window = Toplevel(self.root)
        self.participantreg_window.title("Participant Registration")
        self.participantreg_window.resizable(False,False)
        self.participantreg_window.geometry("500x500")
        
        data = self.cursor.execute("""SELECT id FROM advertisement""").fetchall()        
        if data == []:
            Label(self.participantreg_window, text="No Conference Registered").place(relx = 0.1, rely = 0.15)
        else:
            self.var = StringVar(self.participantreg_window)
            self.var.set("Select Conference Id")
            self.confid = OptionMenu(self.participantreg_window, self.var,*data , command = self.parregmenu)
            self.confid.place(relx = 0.1, rely = 0.12)
        
        Label(self.participantreg_window, text="Name").place(relx = 0.1, rely = 0.2)

        self.parname = Entry(self.participantreg_window, width = 53)
        self.parname.place(relx = 0.1, rely = 0.25)

        Label(self.participantreg_window, text="College Name").place(relx = 0.1, rely = 0.3)

        self.parclgname = Entry(self.participantreg_window, width = 53)
        self.parclgname.place(relx = 0.1, rely = 0.35)

        Label(self.participantreg_window, text="College Address").place(relx = 0.1, rely = 0.4)

        self.parclgaddress = Entry(self.participantreg_window, width = 53)
        self.parclgaddress.place(relx = 0.1, rely = 0.45)

        Label(self.participantreg_window, text="Department").place(relx = 0.1, rely = 0.5)

        self.pardept = Entry(self.participantreg_window, width = 53)
        self.pardept.place(relx = 0.1, rely = 0.55)

        Label(self.participantreg_window, text="Gender").place(relx=0.1, rely=0.6)

        self.pargender = Entry(self.participantreg_window, width= 53)
        self.pargender.place(relx = 0.1,rely = 0.65)

        Label(self.participantreg_window, text="Mobile Number").place(relx=0.1, rely=0.7)

        self.parmobile = Entry(self.participantreg_window, width= 53)
        self.parmobile.place(relx = 0.1,rely = 0.75)
        
        if data != []:
            self.participantreg_button = Button(self.participantreg_window, text="Register", width = 15, command = self.participant_registration_submit)
            self.participantreg_button.place(relx = 0.1, rely = 0.8)
        else:
            Button(self.participantreg_window, text="Coming Soon", width = 15).place(relx = 0.1, rely = 0.8)

    def college_registration_submit(self):
        try:
            self.cursor.execute(
                """INSERT INTO college(name, id, address, username, password) VALUES(?,?,?,?,?)""",
                (self.clgname.get(), self.clgid.get(), self.clgaddress.get(), self.clgusername.get(), self.clgpassword.get())
            )
            self.db.commit()
            messagebox.showinfo("Success", "College Registered Successfully")
            self.clgreg_window.destroy()
        except:
            messagebox.showerror("Error", "College Already Registered")

        
    
    def college_registration(self):
        self.clgreg_window = Toplevel(self.root)
        self.clgreg_window.title("College Registration")
        self.clgreg_window.resizable(False,False)
        self.clgreg_window.geometry("500x500")

        Label(self.clgreg_window, text="College ID").place(relx = 0.1, rely = 0.1)

        self.clgid = Entry(self.clgreg_window, width = 53)
        self.clgid.place(relx = 0.1, rely = 0.15)

        Label(self.clgreg_window, text="College Name").place(relx = 0.1, rely = 0.2)

        self.clgname = Entry(self.clgreg_window, width = 53)
        self.clgname.place(relx = 0.1, rely = 0.25)

        Label(self.clgreg_window, text="College Address").place(relx = 0.1, rely = 0.3)

        self.clgaddress = Entry(self.clgreg_window, width = 53)
        self.clgaddress.place(relx = 0.1, rely = 0.35)

        Label(self.clgreg_window, text="Username").place(relx = 0.1, rely = 0.4)

        self.clgusername = Entry(self.clgreg_window, width = 53)
        self.clgusername.place(relx = 0.1, rely = 0.45)

        Label(self.clgreg_window, text="Password").place(relx = 0.1, rely = 0.5)

        self.clgpassword = Entry(self.clgreg_window, show="*", width = 53)
        self.clgpassword.place(relx = 0.1, rely = 0.55)

        self.clgreg_button = Button(self.clgreg_window, text="Register", width = 15, command = self.college_registration_submit)
        self.clgreg_button.place(relx = 0.1, rely = 0.65)

        self.clgreg_window.mainloop()

    def refresh(self):
        self.root.destroy()
        self.__init__()


    def run(self):
        self.root = Tk()
        self.root.title("Advertisements")        
        self.root.resizable(False,False)
        self.root.geometry("1000x400")

        
        tree = ttk.Treeview(self.root)
        tree["columns"] = ("ConferenceID", "Topic", "College Id","College Name", "College Address", "Department", "Date", "Fees")
        tree.heading("ConferenceID", text="Conference ID")
        tree.heading("Topic", text="Topic")
        tree.heading("College Id", text="College Id")
        tree.heading("College Name", text="College Name")
        tree.heading("College Address", text="College Address")
        tree.heading("Department", text="Department")
        tree.heading("Date", text="Date")
        tree.heading("Fees", text="Fees")
        tree.pack()

        tree.bind("<Double-1>", lambda event: self.participant_registration())

        for x in self.cursor.execute("SELECT * FROM advertisement"):
            tree.insert("", "end", values=x)

        xscrollbar = Scrollbar(self.root, orient=HORIZONTAL, command=tree.xview)
        xscrollbar.pack(side=BOTTOM, fill=X)
        tree.configure(xscrollcommand=xscrollbar.set)

        yscrollbar = Scrollbar(self.root, orient=VERTICAL, command=tree.yview)
        yscrollbar.pack(side=RIGHT, fill=Y)
        tree.configure(yscrollcommand=yscrollbar.set)


        self.participant = Button(self.root, text="Participant", width=15, command = self.participant_registration)
        self.participant.pack(side = LEFT)

        self.college = Button(self.root, text="College", width = 15 , command= self.college_registration)
        self.college.pack(side = LEFT)

        Button(self.root, text="🔃", command = self.refresh).pack(side = RIGHT)            

        login = Button(self.root, text="Login", width = 15 , command = self.clglogin)
        login.pack(side = RIGHT)

        self.clgpassword_entry = Entry(self.root, show="*")
        self.clgpassword_entry.pack(side = RIGHT)

        password = Label(self.root, text="Password:")
        password.pack(side = RIGHT)

        self.clgusername_entry = Entry(self.root)
        self.clgusername_entry.pack(side = RIGHT)

        username = Label(self.root, text="Username:")
        username.pack(side = RIGHT )

        self.root.mainloop()

Conference()