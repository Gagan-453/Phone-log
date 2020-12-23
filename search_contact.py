from tkinter import *
from PIL import Image, ImageTk
import sqlite3 as sq
import tkinter as tk
import view_contact
import main_window

class search_for_contact:
    def __init__(self, username):
        self.user = username
        
        self.root = Tk()
        self.root.title('Search Contacts')
        self.root.iconbitmap('required/icon.ico')
        self.root.resizable(0, 0)
        
        self.search_window = Frame(self.root, width=810, height=50, bg='white')
        self.search_window.propagate(0)
        self.search_window.pack()

        self.search_lbl = Label(self.search_window, text='Search Contacts: ', bg='white', fg='dark blue', font=('Times New Roman', 13))
        self.search_lbl.place(x=20, y=20)

        global search_bar
        search_bar = Entry(self.search_window, width=20, bg='#ECF3F3', fg='black', font=('Bookman Old Style', 14, 'bold'), validate='key')
        search_bar.place(x=150, y=20)
        search_bar['validatecommand'] = self.test

        self.search_img = Image.open('required/search.png')
        self.resize_search_img = self.search_img.resize((25, 25), Image.ANTIALIAS)
        self.search_icon = ImageTk.PhotoImage(self.resize_search_img)

        self.search = Button(self.search_window, image=self.search_icon, relief=FLAT, bg='white', fg='black')
        self.search.place(x=410, y=20)

        self.obj = self.Scrollable_frame(self.root, self.user)
        self.obj.pack()

        self.back = Button(self.search_window, text='Back', width=7, bg='#FBFC9C', fg='#DE2E2E', font=('Arial Black', 14, 'bold'), command=self.back_to_main)
        self.back.pack(side=RIGHT)

        self.exit = Button(self.search_window, text='Exit', width=7, bg='#FBFC9C', fg='#DE2E2E', font=('Arial Black', 14, 'bold'), command=self.root.destroy)
        self.exit.pack(side=RIGHT, padx=15)

    def test(self):
        self.obj.destroy()
        self.obj = self.Scrollable_frame(self.root, self.user, val=search_bar.get())
        self.obj.pack()
        return True

    def back_to_main(self):
        self.root.destroy()
        main_window.phone_log(username=self.user)


    class Scrollable_frame(tk.Frame):
        def __init__(self, parent, username, val=''):
            self.parent = parent
            self.user = username
            tk.Frame.__init__(self, parent)
            self.canvas = tk.Canvas(self, borderwidth=0, width=800, height=500, background="#ffffff")
            self.frame = tk.Frame(self.canvas,  background="#ffffff")
            self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.vsb.set)

            self.vsb.pack(side="right", fill="y")
            self.canvas.pack(side="left")
            self.canvas.create_window((100, 100), window=self.frame, anchor="nw",
                                    tags="self.frame")

            self.frame.bind("<Configure>", self.onFrameConfigure)

            self.contact_entered = val
            self.conn = sq.connect(database='phone_log.db')
            self.cursor = self.conn.cursor()

            self.get_contacts = self.cursor.execute(f'SELECT CONTACT, PHONE1, PIC FROM {self.user}')
            self.cts = self.cursor.fetchall()

            self.conn.close()

            self.contact_names = []
            self.contact_nums = []
            self.contact_pics = []

            for name in self.cts:
                self.contact_names.append(name[0])
                self.contact_nums.append(name[1])
                self.contact_pics.append(name[2])

            self.cpic = Image.open('required/user1.png')
            self.cpic_resize = self.cpic.resize((30, 30), Image.ANTIALIAS)
            self.resized_cpic = ImageTk.PhotoImage(self.cpic_resize)

            if self.contact_entered.strip() == '':
                for widgets in range(len(self.contact_names)):
                    self.contact_detail = Text(self.frame, bg='#ECF3F3', fg='black', width=88, height=2, font=('Arial', 13), cursor='hand2', state=DISABLED)
                    self.contact_detail.propagate(0)
                    self.contact_detail.pack(pady=3, expand=False)
                    
                    self.c_pic = Button(self.contact_detail, relief=FLAT, image=self.resized_cpic, bg='#ECF3F3', fg='black')
                    self.c_pic.pack(side=LEFT)

                    self.name = Button(self.contact_detail, width=20, relief=FLAT, text=self.contact_names[widgets], bg='#ECF3F3', fg='black', font=('Times new roman', 15))
                    self.name.pack(side=LEFT, padx=40)
                    
                    self.phone = Button(self.contact_detail, relief=FLAT, text=self.contact_nums[widgets], width=30, bg='#ECF3F3', fg='grey', font=('Calibri', 13))
                    self.phone.pack(side=LEFT, padx=60)

                    self.name['command'] = lambda uname=self.contact_names[widgets]: self.show_details(uname)
                    self.phone['command'] = lambda uname=self.contact_names[widgets]: self.show_details(uname)
                    self.c_pic['command'] = lambda uname=self.contact_names[widgets]: self.show_details(uname)

            else:
                for names in range(len(self.contact_names)):
                    if (self.contact_entered.strip() in self.contact_names[names]) or (self.contact_entered.strip() in self.contact_nums[names]):
                        self.contact_detail = Text(self.frame, bg='#ECF3F3', fg='black', width=88, height=2, font=('Arial', 13), cursor='hand2', state=DISABLED)
                        self.contact_detail.propagate(0)
                        self.contact_detail.pack(pady=3, expand=False)
                        
                        self.c_pic = Button(self.contact_detail, relief=FLAT, image=self.resized_cpic, bg='#ECF3F3', fg='black')
                        self.c_pic.pack(side=LEFT)

                        self.name = Button(self.contact_detail, width=20, relief=FLAT, text=self.contact_names[names], bg='#ECF3F3', fg='black', font=('Times new roman', 15))
                        self.name.pack(side=LEFT, padx=40)
                        
                        self.phone = Button(self.contact_detail, relief=FLAT, text=self.contact_nums[names], width=30, bg='#ECF3F3', fg='grey', font=('Calibri', 13))
                        self.phone.pack(side=LEFT, padx=60)

                        self.name['command'] = lambda uname=self.contact_names[names]: self.show_details(uname)
                        self.phone['command'] = lambda uname=self.contact_names[names]: self.show_details(uname)
                        self.c_pic['command'] = lambda uname=self.contact_names[names]: self.show_details(uname)



        def onFrameConfigure(self, event):
            '''Reset the scroll region to encompass the inner frame'''
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def show_details(self, name):
            view_contact.show_contact(self.user, name)


if __name__ == "__main__":
    obj = search_for_contact(username='gagan')
    obj.root.mainloop()