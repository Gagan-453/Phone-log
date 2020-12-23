from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from tkinter import ttk
import about
import Sign_up
import Sign_in
import delete_account
import edit_details
import view_contact
import create_contact
import os
import sqlite3 as sq

class Scrollable_frame(tk.Frame):
    def __init__(self, parent, username):
        self.parent = parent
        self.user = username
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, width=800, height=600, background="#ffffff")
        self.frame = tk.Frame(self.canvas,  background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((100, 100), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.user_contacts()

    def user_contacts(self):
        Label(self.frame, text='Contacts', bg='white', fg='green', font=('Arial', 20, 'bold')).pack(pady=20)
        self.new_pic = Image.open('required/plus.png')
        self.new_pic_resize = self.new_pic.resize((40, 40), Image.ANTIALIAS)
        self.New_resized_pic = ImageTk.PhotoImage(self.new_pic_resize)

        global new_cnt
        new_cnt = Button(self.frame, image=self.New_resized_pic, compound=LEFT, font=('Cambria', 15, 'bold'), bg='white', relief=FLAT, fg='dark blue', borderwidth=3, anchor='w', command=self.new_contact)
        new_cnt.place(x=0, y=0)
        new_cnt.bind('<Enter>', self.show_new_contact)
        new_cnt.bind('<Leave>', self.hide_new_contact)

        try:
            self.conn = sq.connect(database='phone_log.db')
            self.cursor = self.conn.cursor()
            self.get_contacts = self.cursor.execute(f'SELECT CONTACT, EMAIL, PIC FROM {self.user}')
            self.cts = self.cursor.fetchall()
            self.contact_names = []
            self.contact_emails = []
            self.contact_pics = []
        except:
            pass

        for name in self.cts:
            self.contact_names.append(name[0])
            self.contact_emails.append(name[1])
            self.contact_pics.append(name[2])

        self.cpic = Image.open('required/user1.png')
        self.cpic_resize = self.cpic.resize((30, 30), Image.ANTIALIAS)
        self.resized_cpic = ImageTk.PhotoImage(self.cpic_resize)

        self.delete_img = Image.open('required/delete.png')
        self.resize_delete_img = self.delete_img.resize((25, 25), Image.ANTIALIAS)
        self.delete_icon = ImageTk.PhotoImage(self.resize_delete_img)

        self.label_img = Image.open('required/label1.png')
        self.resize_label_img = self.label_img.resize((25, 25), Image.ANTIALIAS)
        self.label_icon = ImageTk.PhotoImage(self.resize_label_img)

        for widgets in range(len(self.contact_names)):
            self.contact_detail = Text(self.frame, bg='#ECF3F3', fg='black', width=88, height=2, font=('Arial', 13), cursor='hand2', state=DISABLED)
            self.contact_detail.propagate(0)
            self.contact_detail.pack(pady=3, expand=False)
            
            self.c_pic = Button(self.contact_detail, relief=FLAT, image=self.resized_cpic, bg='#ECF3F3', fg='black')
            self.c_pic.pack(side=LEFT)

            self.name = Button(self.contact_detail, relief=FLAT, width=20, text=self.contact_names[widgets], bg='#ECF3F3', fg='black', font=('Times new roman', 15))
            self.name.pack(side=LEFT, padx=40)

            self.delete = Button(self.contact_detail, relief=FLAT, image=self.delete_icon, bg='#ECF3F3', fg='black')
            self.delete.pack(side=RIGHT)

            self.label = Button(self.contact_detail, relief=FLAT, image=self.label_icon, bg='#ECF3F3', fg='black')
            self.label.pack(side=RIGHT, padx=5)
            
            self.email = Button(self.contact_detail, relief=FLAT, text=self.contact_emails[widgets], width=30, bg='#ECF3F3', fg='grey', font=('Calibri', 13))
            self.email.pack(side=LEFT, padx=60)
            self.name['command'] = lambda uname=self.contact_names[widgets]: self.show_details(uname)
            self.email['command'] = lambda uname=self.contact_names[widgets]: self.show_details(uname)
            self.c_pic['command'] = lambda uname=self.contact_names[widgets]: self.show_details(uname)
            self.delete['command'] = lambda uname=self.contact_names[widgets]: self.delete_contact(uname)

        if len(self.contact_names) < 13:
            self.add = 13 - len(self.contact_names)
            for i in range(self.add):
                tg = Text(self.frame, bg='white', relief=FLAT, state=DISABLED, width=99, height=2, cursor='arrow')
                tg.pack()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_details(self, name):
        view_contact.show_contact(self.user, name)

    def new_contact(self):
        self.parent.destroy()
        create_contact.edit_info(self.user)

    def show_new_contact(self, event):
        new_cnt.config(text='New Contact')
    def hide_new_contact(self, event):
        new_cnt.config(text='')

    def delete_contact(self, contactname):
        self.choice = messagebox.askquestion('Warning', 'Are you sure you want to delete this contact?')

        if self.choice == 'yes':
            try:
                self.c = sq.connect(database='phone_log.db')
                self.cr = self.c.cursor()
                self.delete_ctc = self.cr.execute(f"""DELETE FROM {self.user} WHERE CONTACT='{contactname}'""")
                self.c.commit()
                self.c.close()

                messagebox.showinfo('Contact deleted', 'Contact successfully deleted')
            except:
                pass
        else:
            pass

class phone_log:
    def __init__(self, username):
        self.user = username
        self.root = Tk()
        self.root.title('Phone Log')
        self.root.iconbitmap('required/icon.ico')
        self.root.resizable(0, 0)

        self.menu = Frame(self.root, width=160, height=600, bg='#E0F8C8')
        self.menu.propagate(0)
        self.menu.pack(side=LEFT)

        try:
            self.contacts_pic = Image.open("required/contacts.png")
            self.contacts_pic = self.contacts_pic.resize((70, 70), Image.ANTIALIAS)
            self.contacts = ImageTk.PhotoImage(self.contacts_pic)
        except:
            pass

        global contact
        contact = Button(self.menu, cursor='hand2', text='  Contacts', compound='left', relief=FLAT, bg='#E0F8C8', fg='black', activebackground='light grey', image=self.contacts, font=('Cambria', 13, 'bold'), command=self.contacts_page)
        contact.place(x=0, y=100)
        contact.bind('<Enter>', lambda eff: self.onenter(contact))
        contact.bind('<Leave>', lambda eff: self.onleave(contact))

        self.contact = contact

        try:
            self.labels_pic = Image.open("required/label.png")
            self.labels_pic = self.labels_pic.resize((70, 70), Image.ANTIALIAS)
            self.labels = ImageTk.PhotoImage(self.labels_pic)
        except:
            pass

        global label
        label = Button(self.menu, cursor='hand2', text='  Labels', compound='left', relief=FLAT, bg='#E0F8C8', fg='black', activebackground='light grey', image=self.labels, font=('Cambria', 13, 'bold'), command=self.labels_page)
        label.place(x=0, y=200)
        label.bind('<Enter>', lambda eff: self.onenter(label))
        label.bind('<Leave>', lambda eff: self.onleave(label))
        try:
            self.me_pic = Image.open("required/user.png")
            self.me_pic = self.me_pic.resize((70, 70), Image.ANTIALIAS)
            self.me_button = ImageTk.PhotoImage(self.me_pic)
        except:
            pass

        global me
        me = Button(self.menu, cursor='hand2', text='  Me', compound='left', relief=FLAT, bg='#E0F8C8', fg='black', activebackground='light grey', image=self.me_button, font=('Cambria', 13, 'bold'), command=self.your_profile)
        me.place(x=0, y=300)
        me.bind('<Enter>', lambda eff: self.onenter(me))
        me.bind('<Leave>', lambda eff: self.onleave(me))

        try:
            self.settings_pic = Image.open("required/settings.png")
            self.settings_pic = self.settings_pic.resize((70, 70), Image.ANTIALIAS)
            self.settings = ImageTk.PhotoImage(self.settings_pic)
        except:
            pass

        global setting
        setting = Button(self.menu, cursor='hand2', text='  Settings', compound='left', relief=FLAT, bg='#E0F8C8', fg='black', activebackground='light grey', image=self.settings, font=('Cambria', 13, 'bold'), command=self.settings_page)
        setting.place(x=0, y=400)
        setting.bind('<Enter>', lambda eff: self.onenter(setting))
        setting.bind('<Leave>', lambda eff: self.onleave(setting))

        self.exit = Button(self.menu, text='⬅ Exit', bg='#E0F8C8', fg='dark blue', relief=FLAT, font=('Arial', 14, 'bold'), command=self.root.destroy)
        self.exit.pack(side=BOTTOM)

        self.contacts_page()


    def settings_page(self):
        self.destroy_frames()
        setting['fg'] = 'dark blue'
        setting['bg'] = '#ABEDEB'
        global settings_window
        settings_window = Frame(self.root, width=800, height=600, bg='white')
        settings_window.propagate(0)
        settings_window.pack()

        self.color = PhotoImage(file='required/colors.png')
        self.clbl = Label(settings_window, image=self.color, bg='white', fg='black')
        self.clbl.place(x=-5, y=-6)

        self.heading = Label(settings_window, text='Settings', bg='white', fg='#E11919', font=('Verdana', 19, 'bold'))
        self.heading.pack(pady=10)

        try:
            self.settings_pic = Image.open("required/settings.png")
            self.settings_pic = self.settings_pic.resize((70, 70), Image.ANTIALIAS)
            self.setting_pic = ImageTk.PhotoImage(self.settings_pic)
        except:
            pass

        self.settings_picture = Label(settings_window, image=self.setting_pic, bg='white', fg='black')
        self.settings_picture.place(x=250, y=0)

        self.sort_contacts_lbl = Label(settings_window, text='Sort Contacts By: ', bg='white', fg='#227052', font=('Cambria', 18, 'bold'))
        self.sort_contacts_lbl.place(x=100, y=100)

        global n
        n = StringVar()
        self.sortby = ttk.Combobox(settings_window, width = 20, textvariable = n) 
        self.sortby['values'] = ('Name', 'Date of Birth', 'Random')
        self.sortby.current(0)
        self.sortby.place(x=320, y=108)

        howtouse = Button(settings_window, text='❓ How to use', cursor='hand2', width=30, relief=FLAT, bg='#ECCCD2', font=('Arial', 17, 'bold'))
        howtouse.place(x=20, y=200)
        howtouse.bind('<Enter>', lambda eff: self.onenter(howtouse, '#C8D2C1'))
        howtouse.bind('<Leave>', lambda eff: self.onleave(howtouse, '#ECCCD2'))

        aboutdeveloper = Button(settings_window, text='About Developer', cursor='hand2', width=30, relief=FLAT, bg='#ECCCD2', fg='#165C39', font=('Arial', 17, 'bold'), command=about.Gagan)
        aboutdeveloper.place(x=20, y=260)
        aboutdeveloper.bind('<Enter>', lambda eff: self.onenter(aboutdeveloper, '#C8D2C1'))
        aboutdeveloper.bind('<Leave>', lambda eff: self.onleave(aboutdeveloper, '#ECCCD2'))

        aboutapp = Button(settings_window, text='About Application', cursor='hand2', width=28, relief=FLAT, bg='#ECCCD2', fg='#C01600', font=('Bookman Old Style', 17, 'bold'), command=lambda: os.startfile('about.txt'))
        aboutapp.place(x=20, y=320)
        aboutapp.bind('<Enter>', lambda eff: self.onenter(aboutapp, '#C8D2C1'))
        aboutapp.bind('<Leave>', lambda eff: self.onleave(aboutapp, '#ECCCD2'))

        self.save_changes = Button(settings_window, cursor='hand2', text='Save Changes', bg='#F2F727', fg='#5034E3', width=15, font=('Arial', 15, 'bold'))
        self.save_changes.place(x=60, y=420)
        self.save_changes.bind('<Enter>', lambda eff: self.onenter(self.save_changes, bg='#4FF04E'))
        self.save_changes.bind('<Leave>', lambda eff: self.onleave(self.save_changes, bg='#F2F727'))

        self.cancel = Button(settings_window, cursor='hand2', text='Cancel', bg='#F2F727', fg='#5034E3', width=11, font=('Arial', 15, 'bold'), command=self.contacts_page)
        self.cancel.place(x=320, y=420)
        self.cancel.bind('<Enter>', lambda eff: self.onenter(self.cancel, bg='#4FF04E'))
        self.cancel.bind('<Leave>', lambda eff: self.onleave(self.cancel, bg='#F2F727'))

        self.separator = Label(settings_window, text='', height=50, bg='dark green')
        self.separator.place(x=500, y=0)

        self.switch_account = Button(settings_window, width=20, height=1, text='Switch Account', cursor='hand2', bg='#C7FFF5', fg='#B90000', font=('Cambria', 16, 'bold'), command=self.open_signin)
        self.switch_account.place(x=520, y=60)

        self.new_account = Button(settings_window, width=20, height=1, text='Create New Account', cursor='hand2', bg='#C7FFF5', fg='#B90000', font=('Cambria', 16, 'bold'), command=self.open_signup)
        self.new_account.place(x=520, y=140)

        self.view_mytab = Button(settings_window, width=20, height=1, text='Show my details', cursor='hand2', bg='#C7FFF5', fg='#B90000', font=('Cambria', 16, 'bold'), command=self.your_profile)
        self.view_mytab.place(x=520, y=220)

        self.labelstab = Button(settings_window, width=20, height=1, text='Show labels', cursor='hand2', bg='#C7FFF5', fg='#B90000', font=('Cambria', 16, 'bold'), command=self.labels_page)
        self.labelstab.place(x=520, y=300)

        self.gagan = Label(settings_window, text='~ Gagan Adithya', bg='white', fg='grey', font=('Times New Roman', 14))
        self.gagan.place(x=360, y=530)

        global source
        source = Label(settings_window, text='Download source code here', bg='white', fg='dark blue', cursor='hand2', font=('Calibri', 13))
        source.place(x=30, y=530)
        source.bind('<Enter>', self.underline)
        source.bind('<Leave>', self.leave_underline)

        self.delete_account = Button(settings_window, text='Delete your account', cursor='hand2', bg='#F96D6D', fg='#0F0572', font=('Century', 14, 'bold'), command=self.opendeleteaccount)
        self.delete_account.place(x=550, y=520)
        self.delete_account.bind('<Enter>', lambda eff: self.onenter(self.delete_account, bg='#F72A20'))
        self.delete_account.bind('<Leave>', lambda eff: self.onleave(self.delete_account, bg='#F96D6D'))

        self.clear_contacts = Button(settings_window, width=16, text='Clear Contacts', cursor='hand2', bg='#EE3556', fg='#0F0572', font=('Century', 14, 'bold'), command=self.opendeleteaccount)
        self.clear_contacts.place(x=550, y=450)
        self.clear_contacts.bind('<Enter>', lambda eff: self.onenter(self.clear_contacts, bg='#F72A20'))
        self.clear_contacts.bind('<Leave>', lambda eff: self.onleave(self.clear_contacts, bg='#EE3556'))

    def your_profile(self):
        self.destroy_frames()
        me['fg'] = 'dark blue'
        me['bg'] = '#ABEDEB'
        global profile_window
        profile_window = Frame(self.root, width=800, height=600, bg='white')
        profile_window.propagate(0)
        profile_window.pack()

        self.head = Label(profile_window, text='My Profile', bg='white', fg='#096009', font=('Cambria', 22, 'bold'))
        self.head.pack()

        self.color = PhotoImage(file='required/colors.png')
        self.clbl = Label(profile_window, image=self.color, bg='white', fg='black')
        self.clbl.place(x=-7, y=-6)

        try:
            conn = sq.connect(database='phone_log.db')
            cursor = conn.cursor()
            self.pic = cursor.execute(f"""SELECT * FROM me_{self.user}""")
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
            self.email.insert(END, 'Your Email')
            self.email.config(state=DISABLED, width=25, disabledbackground='#FBFBFB', disabledforeground='grey', font=('Calibri', 13, 'italic'))

        self.address_lbl = Label(profile_window, text='Address: ', bg='white', fg='#0F348A', font=('Verdana', 13, 'bold italic'))
        self.address_lbl.place(x=300, y=250)
        self.address = Text(profile_window, fg='#ED431D', width=20, height=3, font=('Century', 14))
        self.address.place(x=400, y=230)

        if self.addr.strip() != '':
            self.address.insert(END, self.addr)
            self.address.config(state=DISABLED)
        else:
            self.address.insert(END, 'Your Address')
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
            self.text.insert(END, 'Take a note to show here..')
            self.text.config(fg='grey', state=DISABLED, font=('Calibri', 13, 'italic'))

        self.edit_profile = Button(profile_window, cursor='hand2', text='🖊️ Edit Profile', bg='#B1E7A4', fg='#DD0700', font=('Century', 13 ,'bold'), command=self.open_edit_profile)
        self.edit_profile.place(x=70, y=280)

    def contacts_page(self):
        self.destroy_frames()
        contact['fg'] = 'dark blue'
        contact['bg'] = '#ABEDEB'

        #global contacts_window
        #contacts_window = Frame(self.root, width=800, height=600, bg='white')
        #contacts_window.propagate(0)
        #contacts_window.pack()

        global o
        o = Scrollable_frame(self.root, self.user)
        o.pack(side=LEFT)

    def labels_page(self):
        self.destroy_frames()
        label['fg'] = 'dark blue'
        label['bg'] = '#ABEDEB'
        global labels_window
        labels_window = Frame(self.root, width=800, height=600, bg='white')
        labels_window.propagate(0)
        labels_window.pack()

    def destroy_frames(self):
        contact['fg'] = 'black'
        contact['bg'] = '#E0F8C8'
        label['fg'] = 'black'
        label['bg'] = '#E0F8C8'
        me['fg'] = 'black'
        me['bg'] = '#E0F8C8'
        setting['fg'] = 'black'
        setting['bg'] = '#E0F8C8'
        try:
            if settings_window.winfo_exists():
                settings_window.pack_forget()
        except:
            pass

        try:
            if profile_window.winfo_exists():
                profile_window.pack_forget()
        except:
            pass

        try:
            if o.winfo_exists():
                o.pack_forget()
        except:
            pass

        try:
            if labels_window.winfo_exists():
                labels_window.pack_forget()
        except:
            pass


    def onenter(self, button, bg='light grey'):
        button.config(bg=bg)

    def onleave(self, button, bg='#E0F8C8'):
        button.config(bg=bg)

    def open_signup(self):
        self.root.destroy()
        Sign_up.Sign_up()

    def open_signin(self):
        self.root.destroy()
        Sign_in.login()

    def underline(self, event):
        source['font'] = ('Calibri', 13, 'underline')
        
    def leave_underline(self, event):
        source['font'] = ('Calibri', 13)

    def opendeleteaccount(self):
        self.root.destroy()
        delete_account.delete_window()

    def open_edit_profile(self):
        self.root.destroy()
        edit_details.edit_info(self.user)
        
    

if __name__ == '__main__':
    obj = phone_log(username='gagan')
    obj.root.mainloop()