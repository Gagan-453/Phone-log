"""This window is used to sign up to the application"""
from tkinter import *
from tkinter import messagebox
import Sign_in
import sqlite3 as sq
import hashlib as hl

class Sign_up:
    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title('Sign Up')
        self.root.iconbitmap('required/icon.ico')

        self.window = Frame(self.root, width=520, height=600, bg='#0E0D0D')
        self.window.propagate(0)
        self.window.pack()

        self.heading = Label(self.window, text='Phone Log   Registration', width=25, bg='#0E0D0D', fg='pink', font=('Cambria', 25, 'bold'))
        self.heading.pack()

        self.username_var = StringVar()
        self.username = Entry(self.window, width=32, bg='white', fg='#0565AB', textvariable=self.username_var, validate='key', validatecommand=self.check, font=('Arial Black', 10, 'bold'))
        self.username.place(x=100, y=80)
        self.username.bind('<Button-1>', self.border_highlight_username())

        self.name_var = StringVar()
        self.name = Entry(self.window, width=32, bg='white', fg='#0565AB', textvariable=self.name_var, validate='key', validatecommand=self.check, font=('Arial Black', 10, 'bold'))
        self.name.place(x=100, y=120)
        self.name.bind('<Button-1>', self.border_highlight_name())

        self.password_var = StringVar()
        self.password = Entry(self.window, width=24, bg='white', fg='#151314', textvariable=self.password_var, validate='key', validatecommand=self.check, font=('Times new roman', 11, 'bold'), show='*')
        self.password.place(x=225, y=200)
        self.password.bind('<Button-1>', self.border_highlight_password())
        self.show_password = Button(self.window, text='see', cursor='hand2', bg='black', fg='white', relief=FLAT, font=('Arial', 11, 'bold'), command=lambda: self.show_passwords(0))
        self.show_password.place(x=430, y=197)

        self.retype_password_var = StringVar()
        self.retype_password = Entry(self.window, width=24, bg='white', fg='#151314', textvariable=self.retype_password_var, validate='key', validatecommand=self.check, font=('Times new roman', 11, 'bold'), show='*')
        self.retype_password.place(x=225, y=240)
        self.show_retype_password = Button(self.window, cursor='hand2', text='see', bg='black', fg='white', relief=FLAT, font=('Arial', 11, 'bold'), command=lambda: self.show_passwords(1))
        self.show_retype_password.place(x=430, y=238)
        self.retype_password.bind('<Button-1>', self.border_highlight_retypepassword())

        self.username_lbl = Label(self.window, text='User Name:', bg='#0E0D0D', fg='#F6F103', font=('Arial', 13, 'bold'))
        self.username_lbl.place(x=0, y=80)

        self.name_lbl = Label(self.window, text='Name:', bg='#0E0D0D', fg='#F6F103', font=('Arial', 13, 'bold'))
        self.name_lbl.place(x=20, y=120)

        self.passwd_lbl = Label(self.window, text='Password:', bg='#0E0D0D', fg='#DAF11A', font=('Arial', 13, 'bold'))
        self.passwd_lbl.place(x=120, y=200)

        self.retype_passwd_lbl = Label(self.window, text='Retype password:', bg='#0E0D0D', fg='#DAF11A', font=('Arial', 13, 'bold'))
        self.retype_passwd_lbl.place(x=60, y=240)

        self.note = Label(self.window, text="NOTE below security questions are used to recover your password", bg="#0E0D0D", fg="#53F232", font=('Arial', 11, 'italic'))
        self.note.place(x=40, y=300)

        self.save = Button(self.window, text='Continue', cursor='hand2', width=13, height=1, bg='#E7F37E', fg='#08004C', activebackground='light green', font=('Calibri', 13, 'bold'), command= self.check_details)
        self.save.place(x=30, y=520)
        self.save.bind('<Enter>', self.entered_save_button)
        self.save.bind('<Leave>', self.leave_save_button)

        self.clear = Button(self.window, text='Clear', width=13, cursor='hand2', height=1, bg='#E7F37E', fg='black', activebackground='light green', font=('Calibri', 13, 'bold'), command=self.clear)
        self.clear.place(x=200, y=520)
        self.clear.bind('<Enter>', self.entered_clear_button)
        self.clear.bind('<Leave>', self.leave_clear_button)

        self.back = Button(self.window, text='Back', width=13, cursor='hand2', height=1, bg='#E7F37E', fg='black', activebackground='light green', font=('Calibri', 13, 'bold'), command=self.back_to_login)
        self.back.place(x=360, y=520)
        self.back.bind('<Enter>', self.entered_back_button)
        self.back.bind('<Leave>', self.leave_back_button)

        self.sec1 = StringVar()
        self.security_question1 = Entry(self.window, width=36, bg="white", textvariable=self.sec1, fg="black", font=('Cambria', 12))
        self.security_question1.place(x=100, y=350)
        self.security_question1.bind('<Button-1>', self.border_highlight_sq1())

        self.reply1 = StringVar()
        self.answer1 = Entry(self.window, width=27, bg="white", fg="black", textvariable=self.reply1, font=('Cambria', 12), show='*')
        self.answer1.place(x=180, y=380)
        self.answer1.bind('<Button-1>', self.border_highlight_ans1())

        self.sq1_lbl = Label(self.window, text='Question 1: ', bg='#0E0D0D', fg='#DEEB13', font=('Arial', 12))
        self.sq1_lbl.place(x=10, y=350)

        self.ans1_lbl = Label(self.window, text='Answer 1: ', bg='#0E0D0D', fg='#13EBD9', font=('Arial', 12))
        self.ans1_lbl.place(x=90, y=380)

        self.sec2 = StringVar()
        self.security_question2 = Entry(self.window, width=36, bg="white", fg="black", textvariable=self.sec2, font=('Cambria', 12))
        self.security_question2.place(x=100, y=430)
        self.security_question2.bind('<Button-1>', self.border_highlight_sq2())

        self.reply2 = StringVar()
        self.answer2 = Entry(self.window, width=27, bg="white", fg="black", textvariable=self.reply2, font=('Cambria', 12), show='*')
        self.answer2.place(x=180, y=460)
        self.answer2.bind('<Button-1>', self.border_highlight_ans2())

        self.sq2_lbl = Label(self.window, text='Question 2: ', bg='#0E0D0D', fg='#DEEB13', font=('Arial', 12))
        self.sq2_lbl.place(x=10, y=430)

        self.ans2_lbl = Label(self.window, text='Answer 2: ', bg='#0E0D0D', fg='#13EBD9', font=('Arial', 12))
        self.ans2_lbl.place(x=90, y=465)

        self.username.focus_set()
        
    def check(self):
        if self.username.get() != '':
            self.username.config(bg='#76FA73')
        else:
            self.username.config(bg='white')

        if self.name.get()!='':
            self.name.config(bg='#76FA73')
        else:
            self.name.config(bg='white')

        if (self.password.get().isalpha() != True or self.password.get().isalnum() != True) and self.password.get() != '':
            self.password.config(bg='#76FA73')
        else:
            self.password.config(bg='white')

        if self.retype_password.get().strip() == self.password:
            self.retype_password.config(bg='#76FA73')
        else:
            self.retype_password.config(bg='white')

        return True

    def border_highlight_name(self):
        self.name.config(highlightcolor='#00BDC3', highlightthickness=3)

    def border_highlight_username(self):
        self.username.config(highlightcolor='#00BDC3', highlightthickness=3)

    def border_highlight_password(self):
        self.password.config(highlightcolor='#00BDC3', highlightthickness=3)

    def border_highlight_retypepassword(self):
        self.retype_password.config(highlightcolor='#00BDC3', highlightthickness=3)

    def border_highlight_sq1(self):
        self.security_question1.config(highlightcolor='#F73113', highlightthickness=2)
    
    def border_highlight_ans1(self):
        self.answer1.config(highlightcolor="#F73113", highlightthickness=2)

    def border_highlight_sq2(self):
        self.security_question2.config(highlightcolor='#F73113', highlightthickness=2)
    
    def border_highlight_ans2(self):
        self.answer2.config(highlightcolor="#F73113", highlightthickness=2)

    def entered_back_button(self, event):
        self.back.config(bg='light green')

    def entered_save_button(self, event):
        self.save.config(bg='light green')

    def entered_clear_button(self, event):
        self.clear.config(bg='light green')

    def leave_back_button(self, event):
        self.back.config(bg='#FEFA68')

    def leave_save_button(self, event):
        self.save.config(bg='#FEFA68')

    def leave_clear_button(self, event):
        self.clear.config(bg='#FEFA68')

    def show_passwords(self, dig):
        if dig == 0:
            self.password.config(show='')
            self.show_password.config(text='hide', command=lambda: self.hide_passwords(0))

        elif dig == 1:
            self.retype_password.config(show='')
            self.show_retype_password.config(text='hide', command=lambda: self.hide_passwords(1))

    def hide_passwords(self, num):
        if num == 0:
            self.password.config(show='*')
            self.show_password.config(text='see', command=lambda: self.show_passwords(0))
        else:
            self.retype_password.config(show='*')
            self.show_retype_password.config(text='see', command=lambda: self.show_passwords(1))

    def check_details(self):
        self.name1 = self.name_var.get()
        self.password1 = self.password_var.get()
        self.retype_password1 = self.retype_password_var.get()
        self.username1 = self.username_var.get()

        if self.username1 == '':
            self.username.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up!', 'User name cannot be empty!')
        elif ' ' in self.username1:
            messagebox.showerror('Error in Sign up!', 'Username cannot contain spaces')
        elif self.check_username() != True:
            messagebox.showerror('Error in Sign up!', 'Username already exists!! Please try another name..')
        elif self.name1 == '':
            self.name.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up!', 'Name cannot be empty!')
        elif self.name1.isspace() == True:
            self.name.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up!', 'Name cannot be empty!')
        elif self.password1.isalpha():
            self.password.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up', 'Your Password only contains Alphabets try including some numbers..')
        elif self.password1.isdigit():
            self.password.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up!', 'Your password contains only number, try including some alphabets..')
        elif self.password1 == '':
            self.password.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up!', 'Password cannot be empty..')
        elif self.password1.isspace == True:
            self.password.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up!', 'Password cannot be empty..')
        elif self.retype_password1 == '':
            self.retype_password.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up!', 'Please retype the password..')
        elif self.retype_password1 != self.password1:
            self.retype_password.config(bg='#FA8273')
            messagebox.showerror('Error in Sign up!', 'Passwords do not match! Try again')
        elif self.security_question1.get().strip() == '':
            messagebox.showerror('Error in Sign up!', 'Please fill out Security Question 1')
        elif self.answer1.get().strip() == '':
            messagebox.showerror('Error in Sign up!', 'Please fill out Security Answer 1')
        elif self.security_question2.get().strip() == '':
            messagebox.showerror('Error in Sign up!', 'Please fill out Security Question 2')
        elif self.answer2.get().strip() == '':
            messagebox.showerror('Error in Sign up!', 'Please fill out Security Answer 2')
        else:
            self.add_to_database()
            messagebox.showinfo('Success', 'Successfully signed up! Please login')
            self.root.destroy()
            Sign_in.login()

    def add_to_database(self):
        self.username1 = self.username_var.get()
        self.password1 = self.password_var.get()
        self.name1 = self.name_var.get()
        self.sq1 = self.security_question1.get()
        self.sq2 = self.security_question2.get()
        self.ans1 = self.answer1.get()
        self.ans2 = self.answer2.get()

        conn = sq.connect(database='phone_log.db')
        cursor = conn.cursor()

        self.password1 = hl.sha256(self.password1.encode('utf-8'))
        self.hex_password = self.password1.hexdigest()
        self.seq1 = hl.sha256(self.ans1.encode('utf-8'))
        self.seq2 = hl.sha256(self.ans2.encode('utf-8'))
        self.ans1 = self.seq1.hexdigest()
        self.ans2 = self.seq2.hexdigest()
        self.insert_info = """INSERT INTO user_data
                    (USER_NAME, NAME, PASSWORD, sq1, ans1, sq2, ans2)
                    VALUES(?, ?, ?, ?, ?, ?, ?)"""
        self.data = (self.username1, self.name1, self.hex_password, self.sq1, self.ans1, self.sq2, self.ans2)
        cursor.execute(self.insert_info, self.data)

        self.new_table = cursor.execute(f"""CREATE TABLE {self.username1}(CONTACT, pic, phone1, phone2, phone3, email, address, birthday, notes)""")
        self.my_data = cursor.execute(f"""CREATE TABLE me_{self.username1} (NAME, pic, phone1, phone2, phone3, email, address, birthday, notes)""")
        self.labels_data = cursor.execute(f"""CREATE TABLE {self.username1}_bin (CONTACT, pic, phone1, phone2, phone3, email, address, birthday, notes)""")

        conn.commit()
        conn.close()

        conn = sq.connect(database='phone_log.db')
        cursor = conn.cursor()
        self.insert = f"""INSERT INTO me_{self.username1} (NAME, pic, phone1, phone2, phone3, email, address, notes) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
        self.loc = 'required/user1.png'
        self.insert_data = (self.name1, self.loc, '', '', '', '', '', '')
        cursor.execute(self.insert, self.insert_data)
        conn.commit()
        conn.close()

        self.file = open('required/sort.txt', 'w')
        self.file.write(self.username1 + ' : ' + 'Name' + '\n')
        self.file.close()

    def check_username(self):
        conn = sq.connect(database='phone_log.db')
        cursor = conn.cursor()

        #cursor.execute("SELECT COUNT(USER_NAME) FROM user_data")
        #self.count = cursor.fetchone()
        #self.count = self.count[0]

        cursor.execute("SELECT USER_NAME FROM user_data")
        self.usernames_from_db = cursor.fetchall()

        self.usernames = []

        for i in range(len(self.usernames_from_db)):
            self.usernames.append(self.usernames_from_db[i][0])

        if self.username_var.get() not in self.usernames:
            return True
        else:
            return False

        conn.close()

    def back_to_login(self):
        self.root.destroy()
        Sign_in.login()

    def clear(self):
        self.name_var.set('')
        self.password_var.set('')
        self.retype_password_var.set('')
        self.username_var.set('')
        self.username.focus_set()
        self.name.config(bg='white')
        self.password.config(bg='white')
        self.username.config(bg='white')
        self.sec1.set('')
        self.sec2.set('')
        self.reply1.set('')
        self.reply2.set('')

if __name__ == '__main__':
    obj = Sign_up()
    obj.root.mainloop()