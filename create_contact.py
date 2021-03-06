from tkinter import *
from tkinter import messagebox
import sqlite3 as sq
from PIL import Image, ImageDraw
from PIL import ImageTk
from tkinter import filedialog
import main_window

class edit_info:
    def __init__(self, username):
        self.user = username

        self.root = Tk()
        self.root.title('Create Contact')
        self.root.resizable(0, 0)
        self.root.iconbitmap('required/icon.ico')

        self.edit_window = Frame(self.root, width=800, height=630, bg='white')
        self.edit_window.propagate(0)
        self.edit_window.pack()

        try:
            self.lb = Image.open('required/lt.png') #pic
            self.lb = self.lb.resize((100, 100), Image.ANTIALIAS)
            self.lt = ImageTk.PhotoImage(self.lb)
            self.lt_lbl = Label(self.edit_window, height=190, image=self.lt, bg='white', fg='black')
            self.lt_lbl.place(x=-5, y=-50)
        except:
            pass

        try:
            self.br = Image.open('required/rb.png') #pic
            self.br = self.br.resize((100, 100), Image.ANTIALIAS)
            self.br = ImageTk.PhotoImage(self.br)
            self.br_lbl = Label(self.edit_window, height=190, image=self.br, bg='white', fg='black')
            self.br_lbl.place(x=695, y=470)
        except:
            pass

        self.head = Label(self.edit_window, text='Create Contact', bg='white', fg='#B8CE00', font=('Cambria', 22, 'bold'))
        self.head.pack()

        try:
            self.resize_pic = Image.open('required/user1.png') #pic
            self.resized_pic = self.resize_pic.resize((200, 200), Image.ANTIALIAS)
            self.my_pic = ImageTk.PhotoImage(self.resized_pic)
        except:
            pass

        self.picture = Label(self.edit_window, height=195, image=self.my_pic, bg='white', fg='black')
        self.picture.place(x=50, y=75)

        self.change_pic = Button(self.edit_window, text='🖊️ Change Picture', cursor='hand2', bg='#B1E7A4', fg='#DD0700', font=('Century', 13, 'bold'), command=self.choose_picture)
        self.change_pic.place(x=70, y=280)

        self.name_lbl = Label(self.edit_window, text='Name: ', bg='white', fg='#189CCA', font=('Verdana', 13, 'bold italic'))
        self.name_lbl.place(x=300, y=100)
        self.name = Entry(self.edit_window, fg='dark green', font=('Arial', 15, 'bold'))
        self.name.place(x=400, y=100)

        self.email_lbl = Label(self.edit_window, text='Email: ', bg='white', fg='#5447D0', font=('Verdana', 13, 'bold italic'))
        self.email_lbl.place(x=300, y=160)
        self.email = Entry(self.edit_window, fg='#EE9637', width=25, font=('Century', 14))
        self.email.place(x=400, y=160)

        self.address_lbl = Label(self.edit_window, text='Address: ', bg='white', fg='#0F348A', font=('Verdana', 13, 'bold italic'))
        self.address_lbl.place(x=300, y=250)
        self.address = Text(self.edit_window, fg='#ED431D', width=20, height=3, font=('Cambria', 12))
        self.address.place(x=400, y=230)

        self.phone_area = LabelFrame(self.edit_window, text='Phone numbers', width=350, height=200, bd=5, bg='white', fg='#8C118D', font=('Times New Roman', 14, 'bold'))
        self.phone_area.propagate(0)
        self.phone_area.place(x=10, y=350)

        self.pno_lbl = Label(self.phone_area, text='Mobile: ', bg='white', fg='#EE379A', font=('Courier', 14, 'bold'))
        self.pno_lbl.place(x=10, y=20)
        self.pno = Entry(self.phone_area, width=15, bg='white', fg='black', font=('Bookman Old Style', 13, 'bold'))
        self.pno.place(x=100, y=20)

        self.hno_lbl = Label(self.phone_area, text='Home: ', bg='white', fg='#EE379A', font=('Courier', 14, 'bold'))
        self.hno_lbl.place(x=10, y=70)
        self.hno = Entry(self.phone_area, width=15, bg='white', fg='black', font=('Bookman Old Style', 13, 'bold'))
        self.hno.place(x=100, y=70)

        self.fno_lbl = Label(self.phone_area, text='Fax: ', bg='white', fg='#EE379A', font=('Courier', 14, 'bold'))
        self.fno_lbl.place(x=10, y=120)
        self.fno = Entry(self.phone_area, width=15, bg='white', fg='black', font=('Bookman Old Style', 13, 'bold'))
        self.fno.place(x=100, y=120)

        self.notes = LabelFrame(self.edit_window, text='Notes', width=350, height=200, bd=5, bg='white', fg='#8C118D', font=('Times New Roman', 14, 'bold'))
        self.notes.propagate(0)
        self.notes.place(x=400, y=350)

        self.text = Text(self.notes, width=40, height=8, bg='white', fg='black', font=('Calibri', 13), wrap=WORD)
        self.text.propagate(0)
        self.text.pack()

        self.vsb = Scrollbar(self.text, orient=VERTICAL, command=self.text.yview)
        self.text.config(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=RIGHT, fill=Y)

        self.save_changes = Button(self.edit_window, cursor='hand2', text='Create Contact', width=15, bg='#F2F691', fg='#132FCA', font=('Arial', 15, 'bold'), command=self.save_to_database)
        self.save_changes.place(x=50, y=570)

        self.back = Button(self.edit_window, cursor='hand2', text='Cancel', width=10, bg='#F2F691', fg='#132FCA', font=('Arial', 15, 'bold'), command=self.back_to_main)
        self.back.place(x=300, y=570)

        self.exit = Button(self.edit_window, cursor='hand2', text='Exit', width=10, bg='#F2F691', fg='#132FCA', font=('Arial', 15, 'bold'), command=self.root.destroy)
        self.exit.place(x=480, y=570)

        global i
        i = 'required/user1.png'

    def choose_picture(self):
        self.filename = filedialog.askopenfilename(parent=self.root, title='Select a picture', filetypes=(("Pictures", "*.png"), ("All files", ".")))

        if self.filename != None:
            try:
                img = Image.open(self.filename)

                # crop image 
                width, height = img.size
                x = (width - height)//2
                img_cropped = img.crop((x, 0, x+height, height))

                # create grayscale image with white circle (255) on black background (0)
                mask = Image.new('L', img_cropped.size)
                mask_draw = ImageDraw.Draw(mask)
                width, height = img_cropped.size
                mask_draw.ellipse((0, 0, width, height), fill=255)
                #mask.show()

                # add mask as alpha channel
                img_cropped.putalpha(mask)

                # save as png which keeps alpha channel 
                img_cropped.save(f'circle_photos/{self.user}_{self.name.get()}.png')

                self.img = Image.open(f'circle_photos/{self.user}_{self.name.get()}.png') #pic
                self.img = self.img.resize((200, 200), Image.ANTIALIAS)
                self.my_img = ImageTk.PhotoImage(self.img)

                self.picture.config(image=self.my_img)

            except:
                pass
            
            global i
            i = f'circle_photos/{self.user}_{self.name.get()}.png'

    def save_to_database(self):
        self.user_name = self.name.get()
        self.user_email = self.email.get()
        self.user_address = self.address.get(0.0, END)
        self.pno1 = self.pno.get()
        self.pno2 = self.hno.get()
        self.pno3 = self.fno.get()
        self.pnotes = self.text.get(0.0, END)
        self.photo = i

        try:
            conn = sq.connect(database='phone_log.db')
            cursor = conn.cursor()
            self.check_name = cursor.execute(f"""SELECT CONTACT FROM {self.user}""")
            self.names = cursor.fetchall()
            self.unames = []
            for j in self.names:
                self.unames.append(j[0])

            if self.user_name in self.unames:
                messagebox.showerror('Contact exists', 'A contact with this name already exists. Try again!')
            else:

                self.update_to_db = f"""INSERT INTO {self.user}
                            (CONTACT, pic, phone1, phone2, phone3, email, address, notes)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
                self.data = [self.user_name, self.photo, self.pno1, self.pno2, self.pno3, self.user_email, self.user_address, self.pnotes]
                cursor.execute(self.update_to_db, self.data)


                conn.commit()
                conn.close()
                
                messagebox.showinfo('Contact created', 'Contact created successfully')
                self.root.destroy()
                main_window.phone_log(username=self.user)
        except:
            pass


    def back_to_main(self):
        self.root.destroy()
        main_window.phone_log(self.user)


if __name__ == '__main__':
    obj = edit_info(username='gagan')
    obj.root.mainloop()