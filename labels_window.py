"""This window is not included in the application"""
from tkinter import *
from tkinter import messagebox
import sqlite3 as sq

class edit_labels:
    def __init__(self, username, bno):
        self.button_no = bno
        self.user = username

        self.labels = Toplevel(width=600, height=600, bg='white')
        self.labels.propagate(0)
        self.labels.resizable(0, 0)
        self.labels.title('Edit Label')
        self.labels.iconbitmap('required/icon.ico')

        self.heading = Label(self.labels, text='Edit Label', bg='white', fg='dark blue', font=('Times new roman', 20, 'bold'))
        self.heading.pack()

        self.label_name_lbl = Label(self.labels, text='Label name ', bg='white', fg='#F73A56', font=('Century', 15, 'bold'))
        self.label_name_lbl.place(x=30, y=60)

        self.label_name = Entry(self.labels, width=15, bg='#F9FFF8', fg='#2C6224', font=('Arial', 14, 'bold'))
        self.label_name.place(x=160, y=60)
        self.label_name.focus()

        self.notes = LabelFrame(self.labels, width=200, height=200, bg='white', fg='blue', text='Notes', bd=5, font=('Verdana', 14, 'bold'))
        self.notes.place(x=320, y=350)

        self.note = Text(self.notes, width=25, height=8, bg='white', font=('Calibri', 13))
        self.note.pack()

        self.select_contacts = LabelFrame(self.labels, text='Select Contacts', width=500, height=200, bg='white', fg='dark green', bd=5, font=('Verdana', 14, 'bold'))
        self.select_contacts.propagate(0)
        self.select_contacts.place(x=20, y=130)

        self.all_contacts = Listbox(self.select_contacts, height=10, width=25, activestyle='dotbox', bg='white', fg='blue', font='Helvetica', selectmode=MULTIPLE)
        self.all_contacts.pack(side=LEFT)
        self.all_contacts.bind('<<ListboxSelect>>', self.on_select)

        self.show_selected = Text(self.select_contacts, width=20, height=6, bg='white', fg='black', font=('Calibri', 13), wrap=WORD)
        self.show_selected.pack(side=LEFT, padx=20)

        self.conn = sq.connect(database='phone_log.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute(f"""SELECT CONTACT FROM {self.user}""")
        self.details = self.cursor.fetchall()
        self.contacts = []

        for i in range(len(self.details)):
            self.contacts.append(self.details[i][0])
            self.all_contacts.insert(END, self.details[i][0])

        self.conn.close()

        self.save_changes = Button(self.labels, text='Save Changes', width=15, bg='#FFF7AF', fg='dark blue', activebackground='light green', activeforeground='black', font=('Times new roman', 14, 'bold'), command=self.save_to_database)
        self.save_changes.place(x=50, y=360)
        self.save_changes.bind('<Enter>', lambda eff: self.onenter(self.save_changes, bg='light green'))
        self.save_changes.bind('<Leave>', lambda eff: self.onleave(self.save_changes, bg='#FFF7AF'))

        self.back = Button(self.labels, width=15, text='Back', bg='#FFF7AF', fg='dark blue', activebackground='light green', activeforeground='black', font=('Times new roman', 14, 'bold'))
        self.back.place(x=50, y=420)
        self.back.bind('<Enter>', lambda eff: self.onenter(button=self.back, bg='light green'))
        self.back.bind('<Leave>', lambda eff: self.onleave(button=self.back, bg='#FFF7AF'))

        self.exit = Button(self.labels, width=15, text='Exit', bg='#FFF7AF', fg='dark blue', activebackground='light green', activeforeground='black', font=('Times new roman', 14, 'bold'), command=self.labels.destroy)
        self.exit.place(x=50, y=480)
        self.exit.bind('<Enter>', lambda eff: self.onenter(self.exit, bg='light green'))
        self.exit.bind('<Leave>', lambda eff: self.onleave(self.exit, bg='#FFF7AF'))

        self.labels.mainloop()

    def on_select(self, event):
        self.lst = []
        indexes = self.all_contacts.curselection()
        for i in indexes:
            self.lst.append(self.all_contacts.get(i))
        print(self.lst)
        self.show_selected.delete(0.0, END)
        self.show_selected.insert(0.0, self.lst)

    def onenter(self, button, bg='light grey'):
        button.config(bg=bg)

    def onleave(self, button, bg='#E0F8C8'):
        button.config(bg=bg)

    def save_to_database(self):
        self.name = self.label_name.get()
        self.note_lbl = self.note.get(0.0, END)
        self.lst = []
        indexes = self.all_contacts.curselection()
        for i in indexes:
            self.lst.append(self.all_contacts.get(i))


        self.conn = sq.connect(database='phone_log.db')
        self.cursor = self.conn.cursor()

        if len(self.lst) < 15:
            for i in range(15 - len(self.lst)):
                self.lst.append('gd ')
        print(self.lst)

        self.cursor.execute(f"""UPDATE {self.user}_labels SET LABEL_NAME = '{self.name}', NOTE ='{self.note_lbl}', c1='{self.lst[0]}', c2='{self.lst[1]}', c3='{self.lst[2]}', c4='{self.lst[3]}', c5='{self.lst[4]}', c6='{self.lst[5]}', c7='{self.lst[6]}', c8='{self.lst[7]}', c9='{self.lst[8]}', c10='{self.lst[9]}', c11='{self.lst[10]}', c12='{self.lst[11]}', c13='{self.lst[12]}', c14='{self.lst[13]}', c15='{self.lst[14]}' WHERE VAL_NO='{self.button_no}'""")
        self.conn.commit()
        self.conn.close()

        messagebox.showinfo("Success", "Successfully updated details")

if __name__ == '__main__':
    obj = edit_labels('gagan', 1)