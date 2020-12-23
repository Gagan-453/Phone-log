from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import sqlite3 as sq
import edit_contact

class show_contact:
    def __init__(self, username, contact, d='N'):
        self.d = d
        self.user = username
        self.contact_name = contact

        global profile_window
        profile_window = Toplevel(width=800, height=600, bg='white')
        profile_window.propagate(0)
        profile_window.title('View Contact')
        profile_window.iconbitmap('required/icon.ico')
        profile_window.resizable(0, 0)

        self.head = Label(profile_window, text='Contact Details', bg='white', fg='#096009', font=('Cambria', 22, 'bold'))
        self.head.pack()

        self.color = PhotoImage(file='required/colors.png')
        self.clbl = Label(profile_window, image=self.color, bg='white', fg='black')
        self.clbl.place(x=-7, y=-6)

        try:
            conn = sq.connect(database='phone_log.db')
            cursor = conn.cursor()

            if self.d == 'N':
                self.pic = cursor.execute(f"""SELECT * FROM {self.user} WHERE CONTACT='{self.contact_name}'""")
                data = cursor.fetchall()
                self.user_name = data[0][0]
                self.pic = data[0][1]
                self.gmail = data[0][5]
                self.addr = data[0][6]
                self.pnum = data[0][2]
                self.hnum = data[0][3]
                self.fnum = data[0][4]
                self.note = data[0][8]
                self.bday = data[0][7]
            else:
                self.pic = cursor.execute(f"""SELECT * FROM {self.user}_bin WHERE CONTACT='{self.contact_name}'""")
                data = cursor.fetchall()
                self.user_name = data[0][0]
                self.pic = data[0][1]
                self.gmail = data[0][5]
                self.addr = data[0][6]
                self.pnum = data[0][2]
                self.hnum = data[0][3]
                self.fnum = data[0][4]
                self.note = data[0][8]
                self.bday = data[0][7]
        except:
            pass

        try:
            self.resize_pic = Image.open(self.pic) #pic
            self.resized_pic = self.resize_pic.resize((200, 200), Image.ANTIALIAS)
            self.my_pic = ImageTk.PhotoImage(self.resized_pic)
        except:
            pass

        self.picture = Label(profile_window, height=195, image=self.my_pic, bg='white', fg='black')
        self.picture.place(x=50, y=75)

        self.name_lbl = Label(profile_window, text='Name: ', bg='white', fg='#189CCA', font=('Verdana', 13, 'bold italic'))
        self.name_lbl.place(x=300, y=100)
        self.name = Entry(profile_window, fg='dark green', font=('Arial', 15, 'bold'))
        self.name.place(x=400, y=100)
        self.name.insert(END, self.user_name)
        self.name.config(state=DISABLED, disabledforeground='#EE2E1D', disabledbackground='#FBFBFB')

        self.email_lbl = Label(profile_window, text='Email: ', bg='white', fg='#5447D0', font=('Verdana', 13, 'bold italic'))
        self.email_lbl.place(x=300, y=160)
        self.email = Entry(profile_window, fg='dark green', width=30, font=('Arial', 15, 'bold'))
        self.email.place(x=400, y=160)

        if self.gmail.strip() != '':
            self.email.insert(END, self.gmail)
            self.email.config(state=DISABLED,  disabledforeground='#5DD238', disabledbackground='#FBFBFB')
        else:
            self.email.insert(END, 'Email Address')
            self.email.config(state=DISABLED, width=25, disabledbackground='#FBFBFB', disabledforeground='grey', font=('Calibri', 13, 'italic'))

        self.address_lbl = Label(profile_window, text='Address: ', bg='white', fg='#0F348A', font=('Verdana', 13, 'bold italic'))
        self.address_lbl.place(x=300, y=250)
        self.address = Text(profile_window, fg='#ED431D', width=20, height=3, font=('Century', 14))
        self.address.place(x=400, y=230)

        if self.addr.strip() != '':
            self.address.insert(END, self.addr)
            self.address.config(state=DISABLED)
        else:
            self.address.insert(END, 'Address')
            self.address.config(state=DISABLED, width=25, fg='grey', font=('Calibri', 13, 'italic'))

        self.phone_area = LabelFrame(profile_window, text='Phone numbers', width=350, height=200, bd=5, bg='white', fg='#8C118D', font=('Times New Roman', 14, 'bold'))
        self.phone_area.propagate(0)
        self.phone_area.place(x=10, y=350)

        self.pno_lbl = Label(self.phone_area, text='Mobile: ', bg='white', fg='#EE379A', font=('Courier', 14, 'bold'))
        self.pno_lbl.place(x=10, y=20)
        self.pno = Entry(self.phone_area, width=15, bg='white', fg='black', font=('Bookman Old Style', 13, 'bold'))
        self.pno.place(x=100, y=20)

        if self.pnum.strip() != '':
            self.pno.insert(END, self.pnum)
            self.pno.config(state=DISABLED, disabledbackground='white', disabledforeground='black')
        else:
            self.pno.insert(END, 'Mobile number')
            self.pno.config(state=DISABLED, width=20, disabledbackground='white', disabledforeground='grey', font=('Calibri', 12, 'italic'))

        self.hno_lbl = Label(self.phone_area, text='Home: ', bg='white', fg='#EE379A', font=('Courier', 14, 'bold'))
        self.hno_lbl.place(x=10, y=70)
        self.hno = Entry(self.phone_area, width=15, bg='white', fg='black', font=('Bookman Old Style', 13, 'bold'))
        self.hno.place(x=100, y=70)

        if self.hnum.strip() != '':
            self.hno.insert(END, self.hnum)
            self.hno.config(state=DISABLED, disabledbackground='white', disabledforeground='black')
        else:
            self.hno.insert(END, 'Home number')
            self.hno.config(state=DISABLED, width=20, disabledbackground='white', disabledforeground='grey', font=('Calibri', 12, 'italic'))

        self.fno_lbl = Label(self.phone_area, text='Fax: ', bg='white', fg='#EE379A', font=('Courier', 14, 'bold'))
        self.fno_lbl.place(x=10, y=120)
        self.fno = Entry(self.phone_area, width=15, bg='white', fg='black', font=('Bookman Old Style', 13, 'bold'))
        self.fno.place(x=100, y=120)

        if self.fnum.strip() != '':
            self.fno.insert(END, self.fnum)
            self.fno.config(state=DISABLED, disabledbackground='white', disabledforeground='black')
        else:
            self.fno.insert(END, 'Fax number')
            self.fno.config(state=DISABLED, width=20, disabledbackground='white', disabledforeground='grey', font=('Calibri', 12, 'italic'))

        self.notes = LabelFrame(profile_window, text='Personal Notes', width=350, height=200, bd=5, bg='white', fg='#8C118D', font=('Times New Roman', 14, 'bold'))
        self.notes.propagate(0)
        self.notes.place(x=400, y=350)

        self.text = Text(self.notes, width=40, height=8, bg='white', fg='black', font=('Calibri', 13), wrap=WORD)
        self.text.propagate(0)
        self.text.pack()

        self.vsb = Scrollbar(self.text, orient=VERTICAL, command=self.text.yview)
        self.text.config(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=RIGHT, fill=Y)

        if self.note.strip() != '':
            self.text.insert(END, self.note)
            self.text.config(state=DISABLED)
        else:
            self.text.insert(END, 'Make a note to show here..')
            self.text.config(fg='grey', state=DISABLED, font=('Calibri', 13, 'italic'))

        self.edit_profile = Button(profile_window, cursor='hand2', text='🖊️ Edit Profile', bg='#B1E7A4', fg='#DD0700', font=('Century', 13 ,'bold'), command=self.open_edit_profile)
        self.edit_profile.place(x=70, y=280)

        profile_window.mainloop()

    def open_edit_profile(self):
        profile_window.destroy()
        edit_contact.edit_info(self.user, self.contact_name)



if __name__ == '__main__':
    obj = show_contact('gagan', 'Harsha')