"""This window recovers password using security questions"""
from tkinter import *
import sqlite3 as sq
import Sign_in
from tkinter import messagebox
import hashlib as hl

class forgot_password:
    def __init__(self):
        self.root = Tk()
        self.root.title('Forgot Password')
        self.root.iconbitmap('required/icon.ico')
        self.root.resizable(False, False)
        self.f = Frame(self.root, width=500, height=170, bg='#0E0909')
        self.f.propagate(0)
        self.f.pack()

        self.heading = Label(self.f, text='Recover your account..', width=30, height=1, bg='#0E0909', fg='#80FF00', font=('Times new roman', 18, 'bold'))
        self.heading.pack()

        self.username_var = StringVar()
        self.username = Entry(self.f, width=20, bg='white', textvariable=self.username_var, fg='dark blue', font=('Arial', 14, 'bold'))
        self.username.place(x=200, y=60)
        self.username.focus()

        self.username_lbl = Label(self.f, text='Enter username:', width=14, bg='#0E0909', fg='#00EAFF', font=('Verdana', 13, 'bold italic'))
        self.username_lbl.place(x=10, y=60)

        self.back = Button(self.f, text='Back', width=8, cursor='hand2', height=1, bg='#FEFA68', fg='#000BC5', font=('Arial', 14, 'bold'), command=self.back_to_login)
        self.back.place(x=20, y=120)
        self.back.bind('<Enter>', self.entered_back_button)
        self.back.bind('<Leave>', self.leave_back_button)

        self.next = Button(self.f, text='Get questions', width=13, cursor='hand2', height=1, bg='#F5F749', fg='#A61405', font=('Arial', 14, 'bold'), command=self.check)
        self.next.place(x=165, y=120)
        self.next.bind('<Enter>', self.entered_next_button)
        self.next.bind('<Leave>', self.leave_next_button)
        self.username.bind('<Return>', self.invoke_button)

        self.exit = Button(self.f, text='Exit', width=8, cursor='hand2', height=1, bg='#FEFA68', fg='#000BC5', font=('Arial', 14, 'bold'), command=self.root.destroy)
        self.exit.place(x=360, y=120)
        self.exit.bind('<Enter>', self.entered_exit_button)
        self.exit.bind('<Leave>', self.leave_exit_button)

        #self.happy = PhotoImage(file='happy.png')
        #self.happy_lbl = Label(self.f, image=self.happy)
        #self.happy_lbl.place(x=440, y=200)

    def invoke_button(self, event):
        self.next.invoke()

    def check(self):
        global user
        user = self.username_var.get()

        conn = sq.connect(database='phone_log.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(USER_NAME) FROM user_data')
        self.count = cursor.fetchone()
        self.count = self.count[0]

        cursor.execute('SELECT USER_NAME FROM user_data')
        self.names_from_db = cursor.fetchall()
        self.names = []

        for i in range(self.count):
            self.var = self.names_from_db[i][0]
            if self.var not in self.names:
                self.names.append(self.var)

        if self.username_var.get() not in self.names:
            messagebox.showerror('Try again!', 'Username doesn\'t exists..')
        else:
            self.f.config(width=530, height=400)
            self.username.config(state=DISABLED)
            self.next.config(text='Change Password', width=16, command=self.check_answers)
            self.back.place(x=20, y=350)
            self.next.place(x=165, y=350)
            self.exit.place(x=400, y=350)
            cursor.execute(f'''SELECT sq1, sq2 FROM user_data WHERE USER_NAME = "{self.username_var.get()}"''')
            self.questions = cursor.fetchone()
            self.question1 = self.questions[0]
            self.question2 = self.questions[1]

            self.question_1 = Entry(self.f, width=28, bg='white', fg='dark green', disabledforeground='dark green', font=('Arial', 14, 'bold'))
            self.question_1.place(x=100, y=150)
            self.question_1.insert(END, self.question1)
            self.question_1.config(state=DISABLED)

            self.question_2 = Entry(self.f, width=28, bg='white', fg='dark green', disabledforeground='dark green', font=('Arial', 14, 'bold'))
            self.question_2.place(x=100, y=240)
            self.question_2.insert(END, self.question2)
            self.question_2.config(state=DISABLED)

            global answer_1
            answer_1 = Entry(self.f, width=28, bg='white', fg='dark blue', font=('Arial', 12, 'bold'), show='*')
            answer_1.place(x=160, y=180)

            global answer_2
            answer_2 = Entry(self.f, width=28, bg='white', fg='dark blue', font=('Arial', 12, 'bold'), show='*')
            answer_2.place(x=160, y=270)

            self.q1_lbl = Label(self.f, text='Question 1', bg='#0E0909',fg='#E0F916', font=('Cambria', 13, 'italic'))
            self.q1_lbl.place(x=10, y=150)

            self.q2_lbl = Label(self.f, text='Question 2', bg='#0E0909',fg='#E0F916', font=('Cambria', 13, 'italic'))
            self.q2_lbl.place(x=10, y=240)

            self.ans1_lbl = Label(self.f, text='Answer 1', bg='#0E0909', fg='#56F91A', font=('Cambria', 13, 'italic'))
            self.ans1_lbl.place(x=80, y=180)

            self.ans1_lbl = Label(self.f, text='Answer 2', bg='#0E0909', fg='#56F91A', font=('Cambria', 13, 'italic'))
            self.ans1_lbl.place(x=80, y=270)

            cursor.execute(f'''SELECT ans1, ans2 FROM user_data WHERE USER_NAME = "{self.username_var.get()}"''')
            answers = cursor.fetchone()
            global answer1
            global answer2
            answer1 = answers[0]
            answer2 = answers[1]

            conn.close()

    def entered_back_button(self, event):
        self.back.config(bg='light green')

    def entered_next_button(self, event):
        self.next.config(bg='light green')

    def entered_exit_button(self, event):
        self.exit.config(bg='light green')

    def leave_back_button(self, event):
        self.back.config(bg='#FEFA68')

    def leave_next_button(self, event):
        self.next.config(bg='#F5F749')

    def leave_exit_button(self, event):
        self.exit.config(bg='#FEFA68')

    def back_to_login(self):
        self.root.destroy()
        Sign_in.login()

    def check_answers(self):
        self.ans1 = answer_1.get()
        self.ans1 = hl.sha256(self.ans1.encode('utf-8'))
        self.ans_1 = self.ans1.hexdigest()
        self.ans2 = answer_2.get()
        self.ans2 = hl.sha256(self.ans2.encode('utf-8'))
        self.ans_2 = self.ans2.hexdigest()
        if self.ans_1 != answer1:
            messagebox.showerror('Authentication Failed', 'Wrong answer for Security Question 1')
        elif self.ans_2 != answer2:
            messagebox.showerror('Authentication Failed', 'Wrong answer for Security Question 2')
        else:
            messagebox.showinfo('Success', 'You can change your password')
            self.change_password()

    def change_password(self):
        self.f.destroy()
        global passwd
        passwd = Frame(self.root, width=500, height=300, bg='#0D0F0C')
        passwd.propagate(0)
        passwd.pack()

        self.head = Label(passwd, text='Change Password..', width=30, height=1, bg='#0D0F0C', fg='#80FF00', font=('Times new roman', 18, 'bold'))
        self.head.pack()

        global password
        global new_password
        password = StringVar()
        new_password = Entry(passwd, width=20, bg='white', fg='#164316', textvariable=password, font=('Arial', 14, 'bold'), show='*')
        new_password.place(x=150, y=70)

        new_password.focus_set()

        global retype_password
        global retype_new_password
        retype_password = StringVar()
        retype_new_password = Entry(passwd, width=19, bg='white', textvariable=retype_password, fg='#164316', font=('Arial', 14, 'bold'), show='*')
        retype_new_password.place(x=163, y=110)

        global show_password
        global show_retype_new_password
        self.img = PhotoImage(file='required/view.png')
        self.img1 = PhotoImage(file='required/view.png')
        show_password = Button(passwd, image=self.img, width=20, height=20, relief=FLAT, bg='black', fg='white', command=lambda: self.show_passwords(0))
        show_password.place(x=350, y=70)
        show_retype_new_password = Button(passwd, image=self.img1, height=20, width=20, relief=FLAT, bg='black', fg='white', command=lambda: self.show_passwords(1))
        show_retype_new_password.place(x=350, y=110)


        password_lbl = Label(passwd, text='New Password', bg='#0D0F0C', fg='#F75953', font=('Verdana', 13))
        password_lbl.place(x=10, y=70)
        
        retype_password_lbl = Label(passwd, text='Retype Password', bg='#0D0F0C', fg='#F75953', font=('Verdana', 13))
        retype_password_lbl.place(x=10, y=110)

        clear = Button(passwd, text='Clear', cursor='hand2', bg='#EDF753', width=10, height=1, fg='#0620AE', font=('Arial', 12, 'bold'), command=self.clear_details)
        clear.place(x=30, y=200)

        change = Button(passwd, text='Change Password', cursor='hand2', bg='#EDF753', width=15, height=1, fg='#AE0606', font=('Arial', 12, 'bold'), command=self.change_in_database)
        change.place(x=175, y=200)

        close = Button(passwd, text='Exit', cursor='hand2', bg='#EDF753', width=10, height=1, fg='#0620AE', font=('Arial', 12, 'bold'), command=self.root.destroy)
        close.place(x=360, y=200)

    def clear_details(self):
        password.set('')
        retype_password.set('')
        new_password.focus_set()

    def change_in_database(self):
        self.word = password.get()
        self.retype_word = retype_password.get()

        if self.word != self.retype_word:
            messagebox.showerror('Failed to Change Password', 'Passwords do not match! Try again')
        elif self.word.strip() == '':
            messagebox.showerror('Failed to Change Password', 'Please enter a password to continue')
        elif self.word.isalpha() == True:
            messagebox.showerror('Failed to change Password', 'Your password only contains alphabets. Try including some numbers')
        elif self.word.isdigit() == True:
            messagebox.showerror('Failed to change Password', 'Your password only contains numbers. Try including some alphabets')
        else:
            conn = sq.connect(database='phone_log.db')
            cursor = conn.cursor()

            self.word1 = hl.sha256(self.word.encode('utf-8'))
            self.npassword = self.word1.hexdigest()

            cursor.execute(f'''UPDATE user_data SET PASSWORD = "{self.npassword}" WHERE USER_NAME = "{user}"''')
            conn.commit()
            conn.close()

            messagebox.showinfo('Success', 'You have successfully changed your password, please login')
            self.root.destroy()
            Sign_in.login()

    def show_passwords(self, dig):
        if dig == 0:
            new_password.config(show='')
            show_password.config(command=lambda: self.hide_passwords(0))

        elif dig == 1:
            retype_new_password.config(show='')
            show_retype_new_password.config(command=lambda: self.hide_passwords(1))

    def hide_passwords(self, num):
        if num == 0:
            new_password.config(show='*')
            show_password.config(command=lambda: self.show_passwords(0))
        else:
            retype_new_password.config(show='*')
            show_retype_new_password.config(command=lambda: self.show_passwords(1))


if __name__ == '__main__':
    a = forgot_password()
    a.root.mainloop()