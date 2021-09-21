from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class Conference:
    def __init__(self):
        self.db = sqlite3.connect("conference.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS participant(confid TEXT , name TEXT,clgname TEXT,clgaddress TEXT, dept TEXT , mobile TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS college(name TEXT, id TEXT, address TEXT, username TEXT, password TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS advertisement(id TEXT,topic TEXT,clgname TEXT, clgaddress TEXT, dept TEXT, date TEXT, fees TEXT)""")
        self.run()

    def par_submit(self):
        self.cursor.execute("""INSERT INTO participant(confid,name,clgname,clgaddress,dept,mobile) VALUES('{}','{}','{}','{}','{}','{}')""".format(
            self.confid,
            self.par_name_entry.get(),
            self.par_clg_entry.get(),
            self.par_clgadd_entry.get(),
            self.par_dept_entry.get(),
            self.par_mob_entry.get()
        ))
        self.db.commit()
        self.par_window.destroy()
        messagebox.showinfo("Success","Participant Registered Successfully")
    
    def parmenu(self,args):
        self.confid = args[0]
        data = self.cursor.execute("SELECT * FROM advertisement WHERE id='{}'".format(args[0])).fetchall()
        self.conf_name_entry.config(state=NORMAL)
        self.conf_topic_entry.config(state=NORMAL)
        self.conf_name_entry.delete(0,END)
        self.conf_topic_entry.delete(0,END)
        self.conf_name_entry.insert(0,data[0][1])
        self.conf_topic_entry.insert(0,data[0][2])
        print(self.parvariable)

    def participant(self):
        self.par_window = Toplevel()
        self.par_window.title("Participant Registration")
        self.par_window.geometry("500x500")
        self.par_window.resizable(False,False)

        self.parvariable = StringVar(self.par_window)
        self.parvariable.set("Select Conferenece ID")
        self.par_confmenu = OptionMenu(self.par_window, self.parvariable, *self.cursor.execute("SELECT id FROM advertisement").fetchall(),command = self.parmenu)        
        self.par_confmenu.place(relx=0.1 , rely=0.1)

        self.conf_name = Label(self.par_window, text="Conference Name:")
        self.conf_name.place(relx=0.1, rely=0.2)

        self.conf_name_entry = Entry(self.par_window , state=DISABLED)
        self.conf_name_entry.place(relx=0.35, rely=0.2)

        self.conf_topic = Label(self.par_window, text="Conference Topic:")
        self.conf_topic.place(relx=0.1, rely=0.3)

        self.conf_topic_entry = Entry(self.par_window , state=DISABLED)
        self.conf_topic_entry.place(relx=0.35, rely=0.3)

        parname = Label(self.par_window, text="Participant Name:")
        parname.place(relx=0.1, rely=0.4)

        self.par_name_entry = Entry(self.par_window)
        self.par_name_entry.place(relx=0.35, rely=0.4)

        parclg = Label(self.par_window, text="College Name:")
        parclg.place(relx=0.1, rely=0.5)

        self.par_clg_entry = Entry(self.par_window)
        self.par_clg_entry.place(relx=0.35, rely=0.5)

        parclgadd = Label(self.par_window, text="College Address:")
        parclgadd.place(relx=0.1, rely=0.6)

        self.par_clgadd_entry = Entry(self.par_window)
        self.par_clgadd_entry.place(relx=0.35, rely=0.6)

        pardept = Label(self.par_window, text="Department:")
        pardept.place(relx=0.1, rely=0.7)

        self.par_dept_entry = Entry(self.par_window)
        self.par_dept_entry.place(relx=0.35, rely=0.7)

        parmob = Label(self.par_window, text="Mobile Number:")
        parmob.place(relx=0.1, rely=0.8)

        self.par_mob_entry = Entry(self.par_window)
        self.par_mob_entry.place(relx=0.35, rely=0.8)

        self.par_submit = Button(self.par_window, text="Register", command=self.par_submit)
        self.par_submit.place(relx=0.35, rely=0.9)
    
    def select_advertisement(self,args):        
        data = self.cursor.execute("SELECT * FROM advertisement WHERE id='{}'".format(args[0])).fetchall()
        
        self.id_entry.delete(0,END)
        self.topic_entry.delete(0,END)
        self.clgname_entry.delete(0,END)
        self.clgaddress_entry.delete(0,END)
        self.dept_entry.delete(0,END)
        self.date_entry.delete(0,END)
        self.fees_entry.delete(0,END)

        self.id_entry.insert(0,data[0][0])
        self.topic_entry.insert(0,data[0][1])
        self.clgname_entry.insert(0,data[0][2])
        self.clgaddress_entry.insert(0,data[0][3])
        self.dept_entry.insert(0,data[0][4])
        self.date_entry.insert(0,data[0][5])
        self.fees_entry.insert(0,data[0][6])
        
    def reg_update(self):
        self.cursor.execute("""UPDATE advertisement SET id='{}', topic='{}', clgname='{}', clgaddress='{}', dept='{}', date='{}', fees='{}' WHERE id='{}'""".format(
            self.id_entry.get(),
            self.topic_entry.get(),
            self.clgname_entry.get(),
            self.clgaddress_entry.get(),
            self.dept_entry.get(),
            self.date_entry.get(),
            self.fees_entry.get(),
            self.id_entry.get()
        ))
        self.db.commit()
        messagebox.showinfo("Success","Record Updated")


    def advreg_submit(self):
        self.cursor.execute("""INSERT INTO advertisement(id,topic,clgname, clgaddress, dept, date, fees) VALUES(?,?,?,?,?,?,?)""",(
            self.id_entry.get(),self.topic_entry.get(),self.clgname_entry.get(),self.clgaddress_entry.get(),self.dept_entry.get(),self.date_entry.get(),self.fees_entry.get()
            )
        )
        self.db.commit()
        self.advreg.destroy()        
        messagebox.showinfo("Success", "Advertisement Registration Successful")

    def advertisement_registration(self):
        self.advreg = Toplevel(self.root)
        self.advreg.title("Advertisement Registration")
        self.advreg.resizable(False,False)
        self.advreg.geometry("500x500")
        
        try:
            self.variable = StringVar(self.advreg)
            self.variable.set("Select Advertisement")
            self.idoption = OptionMenu(self.advreg, self.variable , *self.cursor.execute("SELECT id FROM advertisement").fetchall() , command=self.select_advertisement)        
            self.idoption.place(relx = 0.65 , rely = 0.09)

            self.updatebtn = Button(self.advreg, text="Update", command = self.reg_update)
            self.updatebtn.place(relx = 0.65 , rely = 0.16)
        except:
            pass

        self.id = Label(self.advreg, text="ID:")
        self.id.place(relx = 0.1 , rely = 0.1)

        self.id_entry = Entry(self.advreg)
        self.id_entry.place(relx = 0.35 , rely = 0.1)

        self.topic = Label(self.advreg, text="Topic:")
        self.topic.place(relx = 0.1 , rely = 0.2)

        self.topic_entry = Entry(self.advreg)
        self.topic_entry.place(relx = 0.35 , rely = 0.2)

        self.clgname = Label(self.advreg, text="College Name:")
        self.clgname.place(relx = 0.1 , rely = 0.3)

        self.clgname_entry = Entry(self.advreg)
        self.clgname_entry.place(relx = 0.35 , rely = 0.3)

        self.clgaddress = Label(self.advreg, text="College Address:")
        self.clgaddress.place(relx = 0.1 , rely = 0.4)

        self.clgaddress_entry = Entry(self.advreg)
        self.clgaddress_entry.place(relx = 0.35 , rely = 0.4)

        self.dept = Label(self.advreg, text="Department:")
        self.dept.place(relx = 0.1 , rely = 0.5)

        self.dept_entry = Entry(self.advreg)
        self.dept_entry.place(relx = 0.35 , rely = 0.5)

        self.date = Label(self.advreg, text="Date:")
        self.date.place(relx = 0.1 , rely = 0.6)

        self.date_entry = Entry(self.advreg)
        self.date_entry.place(relx = 0.35 , rely = 0.6)

        self.fees = Label(self.advreg, text="Fees:")
        self.fees.place(relx = 0.1 , rely = 0.7)

        self.fees_entry = Entry(self.advreg)
        self.fees_entry.place(relx = 0.35 , rely = 0.7)

        self.submit = Button(self.advreg, text="Register" , width = 15 , command = self.advreg_submit)
        self.submit.place(relx = 0.35 , rely = 0.75)

    def clgreg_submit(self):
        self.cursor.execute("""INSERT INTO college(name, id, address, username, password) VALUES(?,?,?,?,?)""",(
                self.clg_name_entry.get(),self.clg_code_entry.get(),self.clg_address_entry.get(),self.clg_username_entry.get(),self.clg_password_entry.get()
            )
        )
        self.db.commit()
        self.clg_window.destroy()
        messagebox.showinfo("Success", "College Registration Successful")


    def college(self):
        self.clg_window = Toplevel(self.root)
        self.clg_window.title("College Registration")
        self.clg_window.resizable(False,False)
        self.clg_window.geometry("500x500")

        self.clg_code = Label(self.clg_window, text="College Code:")
        self.clg_code.place(relx = 0.1 , rely = 0.1)

        self.clg_code_entry = Entry(self.clg_window)
        self.clg_code_entry.place(relx = 0.35 , rely = 0.1)

        self.clg_name = Label(self.clg_window, text="College Name:")
        self.clg_name.place(relx = 0.1 , rely = 0.2)

        self.clg_name_entry = Entry(self.clg_window)
        self.clg_name_entry.place(relx = 0.35 , rely = 0.2)

        self.clg_address = Label(self.clg_window, text="College Address:")
        self.clg_address.place(relx = 0.1 , rely = 0.3)

        self.clg_address_entry = Entry(self.clg_window)
        self.clg_address_entry.place(relx = 0.35 , rely = 0.3)

        self.clg_username = Label(self.clg_window, text="College Username:")
        self.clg_username.place(relx = 0.1 , rely = 0.4)

        self.clg_username_entry = Entry(self.clg_window)
        self.clg_username_entry.place(relx = 0.35 , rely = 0.4)

        self.clg_password = Label(self.clg_window, text="College Password:")
        self.clg_password.place(relx = 0.1 , rely = 0.5)

        self.clg_password_entry = Entry(self.clg_window)
        self.clg_password_entry.place(relx = 0.35 , rely = 0.5)

        self.clg_submit = Button(self.clg_window, text="Submit" , command=self.clgreg_submit)
        self.clg_submit.place(relx = 0.35 , rely = 0.6)

        self.advertisement = Button(self.clg_window, text="Advertisement Registration" , command=self.advertisement_registration)
        self.advertisement.place(relx = 0.1 , rely = 0.7)

    def participant_list(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.cursor.execute("""SELECT * FROM college WHERE username = ? AND password = ?""",(username,password))
        result = self.cursor.fetchone()
        if result is None:
            messagebox.showinfo("Error", "Invalid Username or Password")
        else:
            self.participant_list_window = Toplevel(self.root)
            self.participant_list_window.title("Participant List")
            self.participant_list_window.resizable(False,False)
            self.participant_list_window.geometry("500x500")

            self.parlistvar = StringVar(self.participant_list_window)
            self.parlistvar.set("Select")
             
            allid = [x[0] for x in self.cursor.execute("SELECT * FROM advertisement WHERE clgname='{}'".format(result[0])).fetchall()]
            self.parlist = OptionMenu(self.participant_list_window, self.parlistvar, *allid)
            self.parlist.place(relx = 0.1 , rely = 0.1)
            
            self.parlisttree = Treeview(self.participant_list_window)
            self.parlisttree["columns"]=("Conferenece ID","Participant Name", "Phone Number", "Email", "College Name", "College Address")
            self.parlisttree.column("#0", width=1)
            self.parlisttree.column("Conference ID", width=100)
            self.parlisttree.column("Participant Name", width=100)
            self.parlisttree.column("Phone Number", width=100)
            self.parlisttree.column("Email", width=100)
            self.parlisttree.column("College Name", width=100)
            self.parlisttree.column("College Address", width=100)
            self.parlisttree.heading("Conference ID", text="Conference ID")
            self.parlisttree.heading("Participant Name", text="Participant Name")
            self.parlisttree.heading("Phone Number", text="Phone Number")
            self.parlisttree.heading("Email", text="Email")
            self.parlisttree.heading("College Name", text="College Name")
            self.parlisttree.heading("College Address", text="College Address")
            self.parlisttree.place(relx = 0.1 , rely = 0.2)

            
            


    def run(self):
        self.root = Tk()
        self.root.title("Advertisements")        
        self.root.resizable(False,False)
        self.root.geometry("1000x400")
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("ConferenceID", "Topic", "College Name", "College Address", "Department", "Date", "Fees")
        self.tree.heading("ConferenceID", text="Conference ID")
        self.tree.heading("Topic", text="Topic")
        self.tree.heading("College Name", text="College Name")
        self.tree.heading("College Address", text="College Address")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Fees", text="Fees")
        self.tree.pack()

        for x in self.cursor.execute("SELECT * FROM advertisement"):
            self.tree.insert("", "end", values=x)

        self.scrollbar = Scrollbar(self.root, orient=HORIZONTAL, command=self.tree.xview)
        self.scrollbar.pack(side=BOTTOM, fill=X)
        self.tree.configure(xscrollcommand=self.scrollbar.set)

        self.participant = Button(self.root, text="Participant", command=self.participant)
        self.participant.pack(side = LEFT)

        self.college = Button(self.root, text="College", command=self.college , width = 15)
        self.college.pack(side = LEFT)

        login = Button(self.root, text="Login" , command = self.participant_list)
        login.pack(side = RIGHT)

        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack(side = RIGHT)

        password = Label(self.root, text="Password:")
        password.pack(side = RIGHT)

        self.username_entry = Entry(self.root)
        self.username_entry.pack(side = RIGHT)

        username = Label(self.root, text="Username:")
        username.pack(side = RIGHT )

        self.root.mainloop()
Conference()
