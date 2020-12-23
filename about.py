from tkinter import *
import webbrowser as wb


class Gagan:
    def __init__(self):
        self.f = Toplevel(width=600, height=400, bg='#BAFCB0')
        self.f.propagate(0)
        self.f.title("About")
        self.f.resizable(False, False)
        self.f.iconbitmap('required/icon.ico')

        self.heading = Label(self.f, text='About Developer', bg='#BAFCB0', fg='#210440', font=('Berlin Sans FB Demi', 15, 'underline'))
        self.heading.pack()

        self.img = PhotoImage(file='required/me.png')
        self.myimg = Label(self.f, image=self.img)
        self.myimg.pack(side=LEFT, padx=10)
        self.me = """Hi everyone, 
        I am Gagan who developed "Phone Log", 
        this is my second project using python,
        this is made to organise your contacts nicely.
        You can send feedback to my mail.
        Hope you are enjoying using it.."""
        self.text_about = Text(self.f, bg='#BAFCB0', fg='#F7002C', width=50, height=20, font=('Arial Rounded MT Bold', 12), relief=FLAT)
        self.text_about.place(x=200, y=130)
        self.text_about.insert(END, self.me)
        self.text_about.configure(state=DISABLED)
        self.text_about.tag_add('myself', 1.0, 1.12)
        self.text_about.tag_config('myself', foreground='blue')

        self.mymail = Label(self.f, text='gaganreddy2705@gmail.com', bg='#BAFCB0', fg='blue', cursor='hand2', font=('Calibri', 13, 'underline'))
        self.mymail.place(x=300, y=250)
        self.mymail.bind('<Button-1>', self.mymailopen)
        self.mail_lbl = Label(self.f, text='My mail:', bg='#BAFCB0', fg='#93810D', font=('Calibri', 13))
        self.mail_lbl.place(x=220, y=250)

        self.redirect = Button(self.f, text='Send feedback', bg='#11EFF7', width=20, height=2, font=('Arial', 10, 'bold'), command=self.go_to_gmail)
        self.redirect.place(x=240, y=350)

        self.blog = Button(self.f, text='View Blog', bg='#11EFF7', width=20, height=2,
                               font=('Arial', 10, 'bold'), command=self.view_blog)
        self.blog.place(x=20, y=350)

        self.exit_about = Button(self.f, text='Close', bg='#11EFF7', width=10, height=2,
                               font=('Arial', 10, 'bold'), command=self.exit_window)
        self.exit_about.place(x=470, y=350)
        self.f.mainloop()

    def go_to_gmail(self):
        self.gmail = wb.open("mailto: gaganreddy2705@gmail.com")

    def mymailopen(self, event):
        pass

    def view_blog(self):
        wb.open('https://gaganadithya.blogspot.com')

    def exit_window(self):
        self.f.destroy()

if __name__ == '__main__':
    ab = Gagan()