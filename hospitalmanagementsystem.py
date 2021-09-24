from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import random

class Hospital:
    def __init__(self):
        self.db = sqlite3.connect("hospital.db")
        self.cursor = self.db.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS patients(
                id INTEGER PRIMARY KEY,name TEXT,age INTEGER,gender TEXT,
                bloodgrp TEXT,description TEXT,address TEXT,mobileno TEXT
            )
            """
        )

        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS employees(
                    id INTEGER PRIMARY KEY,name TEXT,age INTEGER,gender TEXT,
                    jobtype TEXT, address TEXT, salary INTEGER
                )
            """
        )

        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS account(
                    id INTEGER, pid TEXT, pname TEXT, bloodgrp TEXT, surgeryamount INTEGER,
                    scanamount INTEGER, medicine TEXT, totalamount INTEGER
                ) 
            """
        )

        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS pharmacy(
                    id INTEGER PRIMARY KEY,name TEXT,description TEXT,price INTEGER
                )
            """
        )

        self.main()

    def open_pharmacy(self):
        pass

    def add_employee_submit(self):
        eid = random.randint(10000,999999999)
        self.cursor.execute("""INSERT INTO employees(id,name,age,gender,jobtype,address,salary) VALUES(?,?,?,?,?,?,?)""",(
            eid,
            self.ename.get(),
            int(self.eage.get()),
            self.egender.get(),
            self.jobtype.get(),
            self.eaddress.get(),
            int(self.esalary.get())
        ))
        self.db.commit()
        messagebox.showinfo("Success", "Employee ID: {}\nCopied To Clipboard".format(eid))
        self.root.clipboard_clear()
        self.root.clipboard_append(str(eid))
        self.addemployeewindow.destroy()

    def get_employee(self):
        data = self.cursor.execute("SELECT * FROM employees WHERE id=?",(self.eid.get())).fetchone()
        if data:
            self.ename.insert(0, data[1])
            self.eage.insert(0, data[2])
            self.egender.insert(0, data[3])
            self.jobtype.set(data[4])
            self.eaddress.insert(0, data[5])
            self.esalary.insert(0, data[6])
        else:
            messagebox.showinfo("Error", "Employee ID Not Found")

    def add_employee(self):
        self.addemployeewindow = Toplevel(self.adminhome)
        self.addemployeewindow.title("Add Employee")
        self.addemployeewindow.geometry("400x400+200+200")
        self.addemployeewindow.resizable(False, False)

        Label(self.addemployeewindow, text="Name").place(relx=0.1, rely=0.1)

        self.ename = Entry(self.addemployeewindow, width=30)
        self.ename.place(relx=0.4, rely=0.1)

        Label(self.addemployeewindow, text="Age").place(relx=0.1, rely=0.2)

        self.eage = Entry(self.addemployeewindow, width=30)
        self.eage.place(relx=0.4, rely=0.2)

        Label(self.addemployeewindow, text="Gender").place(relx=0.1, rely=0.3)

        self.egender = Entry(self.addemployeewindow, width=30)
        self.egender.place(relx=0.4, rely=0.3)

        Label(self.addemployeewindow, text="Job Type").place(relx=0.1, rely=0.4)

        self.jobtype = StringVar(self.addemployeewindow)
        self.jobtype.set("Select Job Type")
        self.jobtype_menu = OptionMenu(self.addemployeewindow, self.jobtype, "Part Time", "Full Time", "Contract" , "Intern" , "Temporary")
        self.jobtype_menu.place(relx=0.4, rely=0.4)

        Label(self.addemployeewindow, text="Address").place(relx=0.1, rely=0.5)

        self.eaddress = Entry(self.addemployeewindow, width=30)
        self.eaddress.place(relx=0.4, rely=0.5)

        Label(self.addemployeewindow, text="Salary").place(relx=0.1, rely=0.6)

        self.esalary = Entry(self.addemployeewindow, width=30)
        self.esalary.place(relx=0.4, rely=0.6)

        Button(self.addemployeewindow, text="Add", command=self.add_employee_submit).place(relx=0.4, rely=0.7)
        Button(self.addemployeewindow, text="Update").place(relx=0.55, rely=0.7)
        Button(self.addemployeewindow, text="Delete").place(relx=0.75, rely=0.7)


        Label(self.addemployeewindow, text="ID:").place(relx=0.1, rely=0.8)
        
        self.eid = Entry(self.addemployeewindow, width=30)
        self.eid.place(relx=0.4, rely=0.8)
        
        Button(self.addemployeewindow, text="GET",command=self.get_employee).place(relx=0.4, rely=0.85)

    def view_employee(self):
        pass

    def add_patient_submit(self):
        pid = random.randint(10000,999999999)
        self.cursor.execute(
            """
            INSERT INTO patients(id,name,age,gender,bloodgrp,description,address,mobileno) 
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                pid,      
                self.pname.get(),
                int(self.page.get()),
                self.pgender.get(),
                self.pbloodgrp.get(),
                self.pdescription.get(),
                self.paddress.get(),
                self.pmobileno.get()
            )
        )
        self.db.commit()
        self.pname.delete(0, END)
        self.page.delete(0, END)
        self.pgender.delete(0, END)
        self.pbloodgrp.delete(0, END)
        self.pdescription.delete(0, END)
        self.paddress.delete(0, END)
        self.pmobileno.delete(0, END)
        self.root.clipboard_clear()
        self.root.clipboard_append(str(pid))

        messagebox.showinfo("Success", "Patient ID : " + str(pid) + "\n Copied to Clipboard")

    def update_patient_submit(self):
        if self.pid.get() != "":
            self.cursor.execute(
                """
                UPDATE patients SET name = ?, age = ?,gender = ?,
                bloodgrp = ?, description = ?, address = ?, mobileno = ?
                WHERE id = ?
                """,
                (
                    self.pname.get(),
                    int(self.page.get()),
                    self.pgender.get(),
                    self.pbloodgrp.get(),
                    self.pdescription.get(),
                    self.paddress.get(),
                    self.pmobileno.get(),
                    self.pid.get()
                )
            )
            self.db.commit()
            self.pname.delete(0, END)
            self.page.delete(0, END)
            self.pgender.delete(0, END)
            self.pbloodgrp.delete(0, END)
            self.pdescription.delete(0, END)
            self.paddress.delete(0, END)
            self.pmobileno.delete(0, END)
            messagebox.showinfo("Success", "Patient Updated")        
        else:
            messagebox.showinfo("Error", "Enter Patient ID")
    def delete_patient_submit(self):
        if self.pid.get() != "":
            query = self.cursor.execute(
                """
                DELETE FROM patients WHERE id = ?
                """,
                (
                    self.pid.get(),
                )
            )
            self.db.commit()
            self.pname.delete(0, END)
            self.page.delete(0, END)
            self.pgender.delete(0, END)
            self.pbloodgrp.delete(0, END)
            self.pdescription.delete(0, END)
            self.paddress.delete(0, END)
            self.pmobileno.delete(0, END)
            self.pid.delete(0, END)
            messagebox.showinfo("Success", "Patient Deleted")
        else:            
            messagebox.showinfo("Error", "Enter Patient ID")


    def getpatient(self):
        data = self.cursor.execute(
            """
            SELECT * FROM patients WHERE id = ?
            """,
            (
                self.pid.get(),
            )
        ).fetchall()

        if data == []:
            messagebox.showinfo("Error", "Patient ID not found")
        else:
            self.pname.delete(0, END)
            self.page.delete(0, END)
            self.pgender.delete(0, END)
            self.pbloodgrp.delete(0, END)
            self.pdescription.delete(0, END)
            self.paddress.delete(0, END)
            self.pmobileno.delete(0, END)

            self.pname.insert(0, data[0][1])
            self.page.insert(0, data[0][2])
            self.pgender.insert(0, data[0][3])
            self.pbloodgrp.insert(0, data[0][4])
            self.pdescription.insert(0, data[0][5])
            self.paddress.insert(0, data[0][6])
            self.pmobileno.insert(0, data[0][7])
        

    def add_patient(self):
        self.addpatientwindow = Toplevel(self.adminhome)
        self.addpatientwindow.title("Add Patient")
        self.addpatientwindow.geometry("500x500")
        self.addpatientwindow.resizable(False, False)

        Label(self.addpatientwindow, text="Name:").place(relx=0.1, rely=0.1)
        
        self.pname = Entry(self.addpatientwindow, width=50)
        self.pname.place(relx=0.3, rely=0.1)

        Label(self.addpatientwindow, text="Age:").place(relx=0.1, rely=0.2)

        self.page = Entry(self.addpatientwindow, width=50)
        self.page.place(relx=0.3, rely=0.2)

        Label(self.addpatientwindow, text="Gender").place(relx=0.1,rely=0.3)

        self.pgender = Entry(self.addpatientwindow,width=50)
        self.pgender.place(relx=0.3,rely=0.3)

        Label(self.addpatientwindow, text="Blood Group").place(relx=0.1,rely=0.4)
        
        self.pbloodgrp = Entry(self.addpatientwindow,width=50)
        self.pbloodgrp.place(relx=0.3,rely=0.4)

        Label(self.addpatientwindow, text="Description").place(relx=0.1,rely=0.5)

        self.pdescription = Entry(self.addpatientwindow,width=50)
        self.pdescription.place(relx=0.3,rely=0.5)

        Label(self.addpatientwindow, text="Address").place(relx=0.1,rely=0.6)

        self.paddress = Entry(self.addpatientwindow,width=50)
        self.paddress.place(relx=0.3,rely=0.6)

        Label(self.addpatientwindow, text="Mobile No.").place(relx=0.1,rely=0.7)

        self.pmobileno = Entry(self.addpatientwindow,width=50)
        self.pmobileno.place(relx=0.3,rely=0.7)

        addpatient = Button(self.addpatientwindow, text="Add", width = 10,command=self.add_patient_submit)
        addpatient.place(relx=0.3, rely=0.8)

        updatepatient = Button(self.addpatientwindow, text="Update", width = 10,command=self.update_patient_submit)
        updatepatient.place(relx=0.5, rely=0.8)

        deletepatient = Button(self.addpatientwindow, text="Delete", width = 10,command=self.delete_patient_submit)
        deletepatient.place(relx=0.7, rely=0.8)

        Label(self.addpatientwindow, text="Patient ID:").place(relx=0.1,rely=0.9)

        self.pid = Entry(self.addpatientwindow,width=40)
        self.pid.place(relx=0.3,rely=0.9)

        Button(self.addpatientwindow, text="GET", width = 10,command=self.getpatient).place(relx=0.7, rely=0.89)

    
    def idviewpatient(self,arg):
        self.patiendetails = Toplevel(self.adminhome)
        self.patiendetails.title("Patient Details | {}".format(arg))
        self.patiendetails.geometry("500x500")

        data = self.cursor.execute("""SELECT * FROM patients WHERE id = {}""".format(arg)).fetchall()

        Label(self.patiendetails, text="Patient ID:").place(relx=0.1,rely=0.1)
        Label(self.patiendetails, text=data[0][0]).place(relx=0.3,rely=0.1)

        Label(self.patiendetails, text="Patient Name:").place(relx=0.1,rely=0.2)
        Label(self.patiendetails, text=data[0][1]).place(relx=0.3,rely=0.2)

        Label(self.patiendetails, text="Patient Age:").place(relx=0.1,rely=0.3)
        Label(self.patiendetails, text=data[0][2]).place(relx=0.3,rely=0.3)

        Label(self.patiendetails, text="Patient Gender:").place(relx=0.1,rely=0.4)
        Label(self.patiendetails, text=data[0][3]).place(relx=0.3,rely=0.4)

        Label(self.patiendetails, text="Patient Blood Group:").place(relx=0.1,rely=0.5)
        Label(self.patiendetails, text=data[0][4]).place(relx=0.3,rely=0.5)

        Label(self.patiendetails, text="Patient Description:").place(relx=0.1,rely=0.6)
        Label(self.patiendetails, text=data[0][5]).place(relx=0.3,rely=0.6)

        Label(self.patiendetails, text="Patient Address:").place(relx=0.1,rely=0.7)
        Label(self.patiendetails, text=data[0][6]).place(relx=0.3,rely=0.7)

        Label(self.patiendetails, text="Patient Mobile No.:").place(relx=0.1,rely=0.8)
        Label(self.patiendetails, text=data[0][7]).place(relx=0.3,rely=0.8)

        Button(self.patiendetails, text="Close", width = 10,command=self.patiendetails.destroy).place(relx=0.7, rely=0.89)

    def view_patient(self):
        self.viewpatientwindow = Toplevel(self.adminhome)
        self.viewpatientwindow.title("All Patients")
        self.viewpatientwindow.geometry("500x500")
        self.viewpatientwindow.resizable(False, False)

        Label(self.viewpatientwindow, text="Patient ID:").pack()

        self.pid = Entry(self.viewpatientwindow,width=40)
        self.pid.pack()

        Button(
            self.viewpatientwindow, text="GET", width = 10,
            command= lambda : self.idviewpatient(self.pid.get())
        ).pack()

        allpatienttable = ttk.Treeview(self.viewpatientwindow, columns=("id", "name"),height=20)
        allpatienttable.heading("#0", text="")
        allpatienttable.heading("#1", text="ID")
        allpatienttable.heading("#2", text="Name")

        allpatienttable.column("#0", width=0)
        allpatienttable.column("#1", width=100)
        allpatienttable.column("#2", width=150)
        allpatienttable.pack()

        data = self.cursor.execute(
            """
            SELECT * FROM patients
            """
        ).fetchall()

        for i in data:
            allpatienttable.insert("", END, values=i)
        
        allpatienttable.bind("<Double-1>", lambda event: self.idviewpatient(allpatienttable.item(allpatienttable.focus())["values"][0]))

        yscrollbar = Scrollbar(self.viewpatientwindow, orient="vertical", command=allpatienttable.yview)
        yscrollbar.pack(side=RIGHT, fill=Y)
        allpatienttable.configure(yscrollcommand=yscrollbar.set)


    def open_account(self):
        pass

    def login_submit(self):
        if self.username.get() == "admin" and self.password.get() == "admin":
            self.root.withdraw()

            self.adminhome = Toplevel(self.root)
            self.adminhome.title("Admin Home")
            self.adminhome.geometry("500x500")
            self.adminhome.resizable(False, False)
            
            Label(self.adminhome, text="Patient").place(relx=0.3, rely=0.1)
            Label(self.adminhome, text="Employee").place(relx=0.6, rely=0.1)

            self.addpatient = Button(self.adminhome, text="Patient Registration", width=20, command=self.add_patient)
            self.addpatient.place(relx=0.15, rely=0.2)

            self.viewpatient = Button(self.adminhome, text="Patient Details", width=20, command=self.view_patient)
            self.viewpatient.place(relx=0.15, rely=0.3)

            self.addemployee = Button(self.adminhome, text="Employee Registration", width=20, command=self.add_employee)
            self.addemployee.place(relx=0.56, rely=0.2)

            self.viewemployee = Button(self.adminhome, text="Employee Details", width=20, command=self.view_employee)
            self.viewemployee.place(relx=0.56, rely=0.3)

            self.account = Button(self.adminhome, text="Account", width=50, command=self.open_account)
            self.account.place(relx=0.15, rely=0.45)

            self.pharmacy = Button(self.adminhome, text="Pharmacy", width=50, command=self.open_pharmacy)
            self.pharmacy.place(relx=0.15, rely=0.55)

            self.logoutbtn = Button(self.adminhome, text="Logout", width=50, command= self.logout)
            self.logoutbtn.place(relx=0.15, rely=0.65)

            self.adminhome.protocol("WM_DELETE_WINDOW", lambda: self.logout())


    def logout(self):
        self.root.destroy()
        self.__init__()

    def main(self):
        self.root = Tk()
        self.root.title("Hospital Management System")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg="lightblue")
    
        Label(self.root, text="Username:", bg="lightblue").place(relx=0.1, rely=0.2)
        
        self.username = Entry(self.root , width=50)
        self.username.place(relx=0.3, rely=0.20)

        Label(self.root, text="Password:", bg="lightblue").place(relx=0.1, rely=0.3)

        self.password = Entry(self.root, show="*" , width=50)
        self.password.place(relx=0.3, rely=0.30)

        self.login = Button(self.root, text="Login", width = 15,command=self.login_submit)
        self.login.place(relx=0.3, rely=0.40)

        self.root.mainloop()

Hospital()