from tkinter import *
import sqlite3 as sq
import Sign_up
from tkinter import messagebox
import hashlib as hl
import recover_password as rp
import main_window

class login:
    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.iconbitmap('required/icon.ico')
        self.root.title('Login')
        self.f = Frame(self.root, width=400, height=350, bg='#090B0B')
        self.f.propagate(0)
        self.f.pack()

        self.heading = Label(self.f, text='Login to your account..', bg='#090B0B', fg='#F30505', font=('Courier', 15, 'bold'))
        self.heading.pack()

        self.name_var = StringVar()
        self.name = Entry(self.f, width=17, bg='#F5F5F5', textvariable=self.name_var, fg='#12019A', font=('Arial', 15, 'bold'))
        self.name.place(x=140, y=60)
        self.name.focus_set()

        self.password_var = StringVar()
        self.password = Entry(self.f, width=17, bg='#F5F5F5', textvariable=self.password_var, fg='black', font=('Arial', 15, 'bold'), show='*')
        self.password.place(x=140, y=120)

        self.show_password = Button(self.f, text='see', cursor='hand2', bg='#090B0B', fg='white', relief=FLAT,
                                    font=('Arial', 14, 'bold'), command=lambda: self.show_passwords(0))
        self.show_password.place(x=330, y=115)

        self.name_lbl = Label(self.f, text='User name:', width=10, bg='#090B0B', fg='#D3FCF8', font=('Calibri', 14, 'italic bold'))
        self.name_lbl.place(x=10, y=60)

        self.password_lbl = Label(self.f, text='Password:', width=10, bg='#090B0B', fg='#D3FCF8', font=('Calibri', 14, 'italic bold'))
        self.password_lbl.place(x=10, y=120)

        self.theme = Button(self.f, text='🌗', height=0, bg='#090B0B', cursor='hand2', fg='#F5F5F5', activebackground='black', activeforeground='#F5F5F5', relief=FLAT, font=('Arial', 15, 'bold'), command=self.change_theme)
        self.theme.place(x=-7, y=-10)

        self.next = Button(self.f, text='Continue', width=8, bg='#E1E05F', fg='#0B0394', font=('arial', 14, 'bold'), command=self.check)
        self.next.place(x=20, y=200)

        self.clear = Button(self.f, text='Clear', width=8, bg='#E1E05F', fg='#0B0394', font=('arial', 14, 'bold'), command=self.clear)
        self.clear.place(x=150, y=200)

        self.exit = Button(self.f, text='Exit', width=7, bg='#E1E05F', fg='#0B0394', font=('arial', 14, 'bold'),
                           command=self.root.destroy)
        self.exit.place(x=280, y=200)



        self.sign_up = Label(self.f, text='Not an user! Sign up here', bg='#090B0B', fg='#F9FDFD', cursor='hand2', font=('Footlight MT Light', 13))
        self.sign_up.place(x=100, y=260)
        self.sign_up.bind('<Button-1>', self.open_sign_up_window)
        self.sign_up.bind('<Enter>', self.enter_sign_up)
        self.sign_up.bind('<Leave>', self.leave_sign_up)

        self.forgot_password = Label(self.f, text='Forgot Password? Recover your account here', bg='#090B0B', fg='#F9FDFD', cursor='hand2', font=('Footlight MT Light', 13))
        self.forgot_password.place(x=40, y=290)
        self.forgot_password.bind('<Button-1>', self.forgot_password_window)
        self.forgot_password.bind('<Enter>', self.enter_forgot_password)
        self.forgot_password.bind('<Leave>', self.leave_recover_password)


    def enter_sign_up(self, event):
        self.sign_up.config(font=('Footlight MT Light', 13, 'underline'))

    def leave_sign_up(self, event):
        self.sign_up.config(font=('Footlight MT Light', 13))

    def enter_forgot_password(self, event):
        self.forgot_password.config(font=('Footlight MT Light', 13, 'underline'))

    def leave_recover_password(self, event):
        self.forgot_password.config(font=('Footlight MT Light', 13))

    def open_sign_up_window(self, event):
        self.root.destroy()
        Sign_up.Sign_up()

    def change_theme(self):
        if self.f['bg'] == '#090B0B':
            self.f.config(bg='#F5F5F5')
            self.name.config(bg='#D1D1D1')
            self.password.config(bg='#D1D1D1')
            self.name_lbl.config(bg='#F5F5F5', fg='#00463F')
            self.password_lbl.config(bg='#F5F5F5', fg='#00463F')
            self.theme.config(bg='#F5F5F5', fg='black', activebackground='#F5F5F5', activeforeground='black')
            self.heading.config(bg='#F5F5F5')
            self.sign_up.config(bg='#F5F5F5', fg='black')
            self.show_password.config(bg='#F5F5F5', fg='black')
        else:
            self.f.config(bg='#090B0B')
            self.name.config(bg='#F5F5F5')
            self.password.config(bg='#F5F5F5')
            self.name_lbl.config(bg='#090B0B', fg='#D3FCF8')
            self.password_lbl.config(bg='#090B0B', fg='#D3FCF8')
            self.theme.config(bg='#090B0B', fg='#F5F5F5', activebackground='black', activeforeground='#F5F5F5')
            self.heading.config(bg='#090B0B')
            self.sign_up.config(bg='#090B0B', fg='#F5F5F5')
            self.show_password.config(bg='#090B0B', fg='#F5F5F5')

    def check(self):
        self.conn = sq.connect(database='phone_log.db')
        cursor = self.conn.cursor()
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


        if self.name_var.get() not in self.names:
            messagebox.showerror('Error in login!', 'Username doesn\'t exists!')
        elif self.name_var.get() in self.names:
            cursor.execute(f'''SELECT PASSWORD FROM user_data WHERE USER_NAME = "{self.name_var.get()}"''')
            self.correct_password = cursor.fetchone()
            self.correct_password = self.correct_password[0]
            self.passwd = hl.sha256(self.password_var.get().encode('utf-8'))
            self.passwd = self.passwd.hexdigest()
            if self.correct_password == self.passwd:
                self.root.destroy()
                u_name = self.name_var.get()
                main_window.phone_log(username=u_name)
            else:
                messagebox.showerror('Error in login', 'Wrong Password!')

    def clear(self):
        self.name_var.set('')
        self.password_var.set('')
        self.name.focus()

    def show_passwords(self, dig):
            self.password.config(show='')
            self.show_password.config(text='hide', command=lambda: self.hide_passwords(0))

    def hide_passwords(self, num):
            self.password.config(show='*')
            self.show_password.config(text='see', command=lambda: self.show_passwords(0))

    def forgot_password_window(self, event):
        self.root.destroy()
        rp.forgot_password()


if __name__ == '__main__':
     call = login()
     call.root.mainloop()