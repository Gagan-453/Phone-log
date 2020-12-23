"""This window is used to delete user's account"""
from tkinter import *
from tkinter import messagebox
import main_window
import sqlite3 as sq
import hashlib as hl

class delete_window:
    def __init__(self, username):
        self.user = username
        self.root = Tk()
        self.root.title('Delete Account')
        self.root.iconbitmap('required/icon.ico')
        self.root.resizable(0, 0)

        self.delete_account = Frame(self.root, width=500, height=330, bg='black')
        self.delete_account.propagate(0)
        self.delete_account.pack()

        self.heading = Label(self.delete_account, text='Delete your account..', bg='black', fg='#64F7D8', font=('Verdana', 16, 'bold'))
        self.heading.pack()

        self.pic = PhotoImage(file='required/sorry.png')
        self.sorry_pic = Label(self.delete_account, image=self.pic, bg='black', fg='white')
        self.sorry_pic.place(x=90, y=50)

        self.sorry = Label(self.delete_account, text='We are sorry to see you go..', width=23, height=1, bg='black', fg='#58E72B', font=('Cambria', 15, 'italic'))
        self.sorry.place(x=150, y=60)

        self.note = Label(self.delete_account, text='NOTE you can\'t recover your account once deleted', bg='black', fg='#28D9B6', font=('Arial', 13, 'italic'))
        self.note.place(x=20, y=200)

        self.enter_password = Entry(self.delete_account, width=20, bg='white', fg='dark blue', font=('Arial', 13, 'bold'), show='*')
        self.enter_password.place(x=160, y=140)

        self.enter_password_lbl = Label(self.delete_account, text='Enter Password', width=12, bg='black', fg='#E34141', font=('Times New Roman', 14, 'bold'))
        self.enter_password_lbl.place(x=10, y=140)

        self.delete = Button(self.delete_account, cursor='hand2', text='Delete your account', bg='#F84848', fg='#195712', activebackground='#195712', activeforeground='#F81616', font=('Footlight MT Light', 13, 'bold'), command=self.delete_from_db)
        self.delete.place(x=20, y=260)

        self.cancel = Button(self.delete_account, width=12, text='Cancel', bg='#E2F848', fg='#2828D9', font=('Times New Roman', 13, 'bold'), command=self.open_main)
        self.cancel.place(x=210, y=260)

        self.exit = Button(self.delete_account, width=12, text='Exit', bg='#E2F848', fg='#2828D9', font=('Times New Roman', 13, 'bold'), command=self.root.destroy)
        self.exit.place(x=350, y=260)
        
        self.enter_password.focus_set()

    def delete_from_db(self):
        self.conn = sq.connect(database='phone_log.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute(f"""SELECT PASSWORD FROM USER_DATA WHERE USER_NAME='{self.user}'""")
        self.passwd = self.cursor.fetchone()
        self.passwd = self.passwd[0]

        self.password1 = self.enter_password.get()
        self.entered_password = hl.sha256(self.password1.encode('utf-8'))
        self.hex_password = self.entered_password.hexdigest()

        if self.hex_password == self.passwd:
            self.cursor.execute(f"""DROP TABLE {self.user}""")
            self.cursor.execute(f"""DELETE FROM USER_DATA WHERE USER_NAME='{self.user}'""")
            self.cursor.execute(f"""DROP TABLE me_{self.user}""")
            self.cursor.execute(f"""DROP TABLE {self.user}_bin""")
            messagebox.showinfo('Deleted your account', 'Successfully deleted your account')
            self.root.destroy()
        else:
            messagebox.showerror('Can\'t delete account', 'You entered wrong password! Try again..')
        self.conn.commit()
        self.conn.close()

    def open_main(self):
        self.root.destroy()
        main_window.phone_log(username=self.user)

if __name__ == '__main__':
    obj = delete_window('abc')
    obj.root.mainloop()