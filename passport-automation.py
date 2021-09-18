from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from uuid import uuid4
import sqlite3

class Passport:
    def __init__(self):
        self.db = sqlite3.connect('passport.db')
        self.cursor = self.db.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passport
                    (id TEXT PRIMARY KEY,
                    name TEXT,
                    dob TEXT,
                    paddress TEXT,
                    taddress TEXT,
                    email TEXT,
                    phone TEXT,
                    proof TEXT,
                    proofno TEXT,
                    admin_ver TEXT,
                    police_ver TEXT,
                    regionaladmin_ver TEXT)''')
        self.run()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def add_passport(self, name, dob, paddress, taddress, email, phone, proof , proofno):
        id = str(uuid4().hex)
        self.cursor.execute('''INSERT INTO passport (id, name, dob, paddress, taddress, email, phone, proof, proofno,admin_ver, police_ver, regionaladmin_ver)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (id, name, dob, paddress, taddress, email, phone, proof, proofno, '0', '0', '0'))
        self.db.commit()
        return id

    def get_passport(self, id):
        return self.cursor.execute('''SELECT * FROM passport WHERE id = ?''', (id,)).fetchone()

    def get_passports(self):
        return self.cursor.execute('''SELECT * FROM passport''').fetchall()

    def add_verification(self, id ,verifier):
        self.cursor.execute('''UPDATE passport SET {}='1'  WHERE id ='{}' '''.format(verifier, id))
        self.db.commit()

    def application_submit(self):
        applicant_id = self.add_passport(
            self.applicant_name_entry.get(),
            self.applicant_dob_entry.get(),
            self.applicant_paddress_entry.get(),
            self.applicant_taddress_entry.get(),
            self.applicant_email_entry.get(),
            self.applicant_phone_entry.get(),
            self.proof,
            self.applicant_proof_number_entry.get()
        )
        self.root.clipboard_clear()
        self.root.clipboard_append(applicant_id)
        self.root.update()
        messagebox.showinfo('Verification Started', ' Your Passport ID: {} - Copied to clipboard'.format(applicant_id))
        self.applicant.destroy()

    def application_proof_select(self,args):
        self.proof = args
        

    def applicant_window(self):
        self.applicant = Toplevel(self.root)
        self.applicant.title('Applicant')
        self.applicant.geometry('500x500')
        self.applicant.resizable(width=False, height=False)

        applicant_name = Label(self.applicant, text='Name:')
        applicant_name.place(relx = 0.1 , rely =0.1)

        self.applicant_name_entry = Entry(self.applicant , width= 55)
        self.applicant_name_entry.place(relx = 0.25 , rely =0.1)

        applicant_dob = Label(self.applicant, text='Date of Birth:')
        applicant_dob.place(relx = 0.1 , rely =0.2)

        self.applicant_dob_entry = Entry(self.applicant , width= 55)
        self.applicant_dob_entry.place(relx = 0.25 , rely =0.2)

        applicant_taddress = Label(self.applicant, text='Temporary\nAddress:')
        applicant_taddress.place(relx = 0.1 , rely =0.27)

        self.applicant_taddress_entry = Entry(self.applicant , width= 55)
        self.applicant_taddress_entry.place(relx = 0.25 , rely =0.3)

        applicant_paddress = Label(self.applicant, text='Permanent\nAddress:')
        applicant_paddress.place(relx = 0.1 , rely =0.37)

        self.applicant_paddress_entry = Entry(self.applicant , width= 55)
        self.applicant_paddress_entry.place(relx = 0.25 , rely =0.4)

        applicant_email = Label(self.applicant, text='Email:')
        applicant_email.place(relx = 0.1 , rely =0.5)

        self.applicant_email_entry = Entry(self.applicant , width= 55)
        self.applicant_email_entry.place(relx = 0.25 , rely =0.5)

        applicant_phone = Label(self.applicant, text='Phone:')
        applicant_phone.place(relx = 0.1 , rely =0.6)

        self.applicant_phone_entry = Entry(self.applicant , width= 55)
        self.applicant_phone_entry.place(relx = 0.25 , rely =0.6)

        applicant_proof = Label(self.applicant, text='Proof:')
        applicant_proof.place(relx = 0.1 , rely =0.7)

        self.applicant_proof_entry = StringVar()
        self.applicant_proof_entry.set('Select')
        self.applicant_proof_menu = OptionMenu(self.applicant, self.applicant_proof_entry, 'Driving License', 'Aadhar Card', 'Voter ID', 'Pan Card', 'Ration Card',
                                                command = self.application_proof_select)
        self.applicant_proof_menu.place(relx = 0.25 , rely =0.7)

        applicant_proof_number = Label(self.applicant, text='Proof\nNumber:')
        applicant_proof_number.place(relx = 0.1 , rely =0.77)
        
        self.applicant_proof_number_entry = Entry(self.applicant , width= 55)
        self.applicant_proof_number_entry.place(relx = 0.25 , rely =0.8)

        applybtn = Button(self.applicant, text='Apply', width=12 , command=self.application_submit)
        applybtn.place(relx = 0.75 , rely =0.9)

        self.applicant.mainloop()

    def status_submit(self):
        self.viewstatus = Toplevel(self.root)
        self.viewstatus.title('Status | {}'.format(self.applicant_no_entry.get()))
        self.viewstatus.geometry('500x500')
        self.viewstatus.resizable(width=False, height=False)

        data = self.get_passport(self.applicant_no_entry.get())

        if data:        
            admin_status = Label(self.viewstatus, text='Admin:')
            admin_status.place(relx = 0.1 , rely =0.2)        

            if data[-3] == '0':
                adminver = Label(self.viewstatus, text='Not Verified', fg='red')
                adminver.place(relx = 0.5 , rely =0.2)
            else:
                adminver = Label(self.viewstatus, text='Verified', fg='green')
                adminver.place(relx = 0.5 , rely =0.2)            

            police_status = Label(self.viewstatus, text='Police:')
            police_status.place(relx = 0.1 , rely =0.3)

            if data[-2] == '0':
                policever = Label(self.viewstatus, text='Not Verified', fg='red')
                policever.place(relx = 0.5 , rely =0.3)
            else:
                policever = Label(self.viewstatus, text='Verified', fg='green')
                policever.place(relx = 0.5 , rely =0.3)                    
            
            regionaladmin_status = Label(self.viewstatus, text='Regional Admin:')
            regionaladmin_status.place(relx = 0.1 , rely =0.4)

            if data[-1] == '0':
                regionaladminver = Label(self.viewstatus, text='Not Verified', fg='red')
                regionaladminver.place(relx = 0.5 , rely =0.4)
            else:
                regionaladminver = Label(self.viewstatus, text='Verified', fg='green')
                regionaladminver.place(relx = 0.5 , rely =0.4)

            if data[-3] == data[-2] == data[-1] == '1':
                applicant_status = Label(self.viewstatus, text='Passport Issued', fg='green',font=('Arial', 20, 'bold'))
                applicant_status.place(relx = 0.3 , rely =0.7)
            else:
                applicant_status = Label(self.viewstatus, text='Verification Pending', fg='red',font=('Arial', 20, 'bold'))
                applicant_status.place(relx = 0.3 , rely =0.7)

        else:
            messagebox.showerror('Error', 'No such passport')
            self.viewstatus.destroy()

    def status_window(self):
        self.status = Toplevel(self.root)
        self.status.title('Status') 
        self.status.geometry('300x200') 
        self.status.resizable(width=False, height=False)

        applicant_no = Label(self.status, text='Applicant No:')
        applicant_no.place(relx = 0.1 , rely =0.3)

        self.applicant_no_entry = Entry(self.status , width= 40)
        self.applicant_no_entry.place(relx = 0.1 , rely =0.4)

        checkbtn = Button(self.status, text='Check Status', width=12 , command=self.status_submit)
        checkbtn.place(relx = 0.6 , rely =0.6)

        self.status.mainloop()

    def verification_submit(self):        
        verifyno = self.applicant_table.item(self.applicant_table.focus())['text']
        res = messagebox.askquestion('Verification', 'Are you sure you want to verify {}?'.format(verifyno))
        if res == 'yes':
            self.cursor.execute("UPDATE passport SET {}_ver='1' WHERE id='{}'".format(self.verifier,verifyno))
            self.db.commit()
            messagebox.showinfo('Success', '{} has been verified'.format(verifyno))
            self.verification.destroy()
            self.verification_window()
        
    def verification_window(self):        
        if (
                self.username.get() == 'admin' and self.password.get() == 'admin' and self.login_type == 'Admin'
            ) or (
                self.username.get() =='police' and self.password.get() == 'police' and self.login_type == 'Police'
            ) or (
                self.username.get() == 'regionaladmin' and self.password.get() == 'regionaladmin' and self.login_type == 'Regional Admin'
            ):                
            self.root.wm_state('iconic')
            self.verifier = self.username.get()
            self.verification = Toplevel(self.root)
            self.verification.title('Verification | {}'.format(self.login_type))

            # Table of Applicants
            self.applicant_table = ttk.Treeview(self.verification, columns=('Applicant No', 'Name', 'DOB', 'TAddress','PAddress', 'Phone', 'Email', 'Proof', 'Proof No.','Admin','Police','Regional Admin'))
            self.applicant_table.heading('#0', text='Applicant No')
            self.applicant_table.heading('#1', text='Name')
            self.applicant_table.heading('#2', text='DOB')
            self.applicant_table.heading('#3', text='TAddress')
            self.applicant_table.heading('#4', text='PAddress')
            self.applicant_table.heading('#5', text='Phone')
            self.applicant_table.heading('#6', text='Email')
            self.applicant_table.heading('#7', text='Proof')            
            self.applicant_table.heading('#8', text='Proof No.')
            self.applicant_table.heading('#9', text='Admin')
            self.applicant_table.heading('#10', text='Police')
            self.applicant_table.heading('#11', text='Regional Admin')
            self.applicant_table.pack()            
            
            for x in self.get_passports():            
                if x[9] == '0':
                    admin = 'Not Verified'
                elif x[9] == '1':
                    admin = 'Verified'
                
                if x[10] == '0':
                    police = 'Not Verified'
                elif x[10] == '1':
                    police = 'Verified'
                
                if x[11] == '0':
                    regadmin = 'Not Verified'
                elif x[11] == '1':
                    regadmin = 'Verified'
                self.applicant_table.insert('', 'end', text=x[0], values=(x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8],admin,police,regadmin))            
            


            scrollbar = ttk.Scrollbar(self.verification, orient=HORIZONTAL, command=self.applicant_table.xview)
            self.applicant_table.configure(xscroll=scrollbar.set)
            scrollbar.pack(side=BOTTOM, fill=X)

            verifybtn = Button(self.verification, text='Verify', width=12, command=self.verification_submit)
            verifybtn.pack(fill=X)

            self.verification.mainloop()

    def login_type_select(self,args):
        self.login_type = args
        

    def run(self):
        self.root = Tk()
        self.root.title('Passport System')
        self.root.geometry('500x500')
        self.root.resizable(width=False, height=False)

        usernamelabel = Label(self.root, text='Username:')
        usernamelabel.place(relx = 0.1 , rely =0.1)

        self.username = Entry(self.root , width= 55)
        self.username.place(relx = 0.25 , rely =0.1)

        passwordlabel = Label(self.root, text='Password:')
        passwordlabel.place(relx = 0.1 , rely =0.2)

        self.password = Entry(self.root , width= 55 , show="*")
        self.password.place(relx = 0.25 , rely =0.2)

        logintypelabel = Label(self.root, text='Login Type:')
        logintypelabel.place(relx = 0.1 , rely =0.3)

        self.login_type = StringVar()
        self.login_type.set('Select')
        login_type_menu = OptionMenu(self.root, self.login_type, 'Admin', 'Police', 'Regional Admin', command=self.login_type_select)
        login_type_menu.place(relx = 0.25 , rely =0.3)

        self.login = Button(self.root, text='Login', width=15 , command=self.verification_window)
        self.login.place(relx = 0.1 , rely =0.4)


        applicantbtn = Button(self.root, text='Applicant', width=30, command=self.applicant_window)
        applicantbtn.place(relx = 0.5, rely =0.5)

        statusbtn = Button(self.root, text='Status', width=30, command= self.status_window)
        statusbtn.place(relx = 0.5, rely =0.6)

        self.root.mainloop()
        
Passport()