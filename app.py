import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from PIL import Image,ImageTk
import requests
import unicodedata
import webbrowser
import yfinance as yf
import matplotlib.pyplot as plt
import json
import webbrowser
import pyodbc
from tkinter import messagebox
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import threading
import time
import concurrent.futures
import random
import smtplib
import imghdr
from email.message import EmailMessage



state = 0
global cur_id
cur_id = 0
hist_data = [0,0,0]
l = []

def update_continous(name):
    try:
        x = []
        for i in name:
            data2 = yf.Ticker(i)
            x.append(data2.info['regularMarketPrice'])
            #x.append(random.randint(1,100))
        return x
    except:
        print('X')

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
"Server=YourServerName;"
"Database = YourDatabase;"
"username= YourUsername;"
"password= YourPassword;"
"Trusted_Connection=yes;",autocommit=True)
db = conn.cursor()
print("conn")
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)



        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        global container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Login_Window, Register_Window,Load_Window):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login_Window")
    def add(self):
        for F in ( Watchlist_Window, News_Window, Funds_Window, Portfolio_Window, Profile_Window, History_Window,Orders_Window ):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
    def order(self,window):
        F=Orders_Window
        page_name = F.__name__
        frame = F(parent=container, controller=self)
        self.frames[page_name] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(window)

    def history(self,window):
        for F in (History_Window,Portfolio_Window,Funds_Window):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(window)

    def port(self):
        F=Portfolio_Window
        page_name = F.__name__
        frame = F(parent=container, controller=self)
        self.frames[page_name] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Portfolio_Window")


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Load_Window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#131722')
        self.controller = controller
        self.controller.title("Macs")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(1)
        logoimg = Image.open(r"logo.png")
        logoimg = logoimg.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg)
        lblimg1 = tk.Label(self,image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)


class Login_Window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#131722')
        self.controller = controller
        self.controller.title("Macs")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(2)
        def check():
            email=self.txtuser.get()
            passw=self.txtpass.get()
            flag=0

            emailid = db.execute("""SELECT * FROM users WHERE email = ?""", email).fetchone()
            if not email or not passw:
                messagebox.showerror(message = "Fields cannot be empty!!")
                flag=1
            elif emailid is None or not check_password_hash(emailid.hash1,passw):
                messagebox.showerror(message = "Invalid Username/Password!")
                flag=1
            if flag==0:
                global cur_id
                cur_id = emailid.id
                print(cur_id)
                controller.add()
                self.txtuser.dell()
                self.txtpass.dell()
                controller.show_frame("Watchlist_Window")


        logoimg = Image.open(r"logo.png")
        logoimg = logoimg.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg)
        lblimg1 = tk.Label(self,image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)

        loginbtn2 = tk.Button(self,text="Login",font=("Arial",25),fg="#007BFF",bg="#131722",borderwidth=0)
        loginbtn2.place(x=1209.48,y=35.84,width=82.53,height=45)

        regbtn2 = tk.Button(self,text="Register",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Register_Window"))
        regbtn2.place(x=1019.76,y=35.84,width=122.37,height=45)

        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)

        frame = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame.place(x=412.65,y=141.65,width=539.76,height=422.4)

        get_str = tk.Label(frame,text="Login",font=("Arial",25),fg="white",bg="#131722")
        get_str.place(x=214,y=41,width=93.91,height=40.11)

        self.txtuser = Placeholder(frame,placeholder='  Email Address',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
        self.txtuser.place(x=92,y=118,width=350.99,height=52.91)

        self.txtpass = Placeholder(frame,placeholder='  Password',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
        self.txtpass.place(x=92,y=190,width=350.99,height=52.91)

        #loginbtn = tk.Button(frame,text="Login",font=("Arial",20,"bold"),fg="white",bg="#007BFF",command=lambda: controller.show_frame("Watchlist_Window"))
        loginbtn = tk.Button(frame,text="Login",font=("Arial",20,"bold"),activeforeground="white",activebackground="black",fg="white",bg="#007BFF",command=check)
        loginbtn.place(x=92,y=292,width=350.99,height=52.91)



class Register_Window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#131722')
        self.controller = controller
        self.controller.title("Macs")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(3)
        def check():
            user = self.txtuser.get()
            email = self.txtpass.get()
            pass1 = self.txtpass1.get()
            pass2 = self.txtpass2.get()
            pan = self.txtpass3.get()
            mob = self.txtpass4.get()

            def mails():
                try:
                    name = user
                    EMAIL_ADDRESS = "teammacs016@gmail.com"
                    EMAIL_PASSWORD = "Vesit123"
                    with open("my-new-message.html", "r", encoding='utf-8') as f:
                        text= f.read()
                    msg = EmailMessage()
                    text = text.replace("AbCdEfGh",name)
                    msg['Subject'] = 'Welcome to Macs Family!'
                    msg['From'] = "teammacs6@gmail"
                    msg['To'] = email

                    msg.set_content('This is a plain text email')

                    msg.add_alternative(text, subtype='html')


                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                except:
                    pass


            users = db.execute("""SELECT * FROM users WHERE username = ?""", user).fetchone()
            emailid = db.execute("""SELECT * FROM users WHERE email = ?""", email).fetchone()
            flag = 0
            if not user or not email or not pass1 or not pass2 or not mob or not pan:
                messagebox.showerror(message = "Fields cannot be empty!!")
                flag=1
            elif users is not None:
                messagebox.showerror(message = "User already exists!!")
                flag=1
            elif emailid is not None:
                messagebox.showerror(message = "Email already taken!!")
                flag=1
            elif pass1 != pass2:
                messagebox.showerror(message = "Passwords Do not match!!")
                flag=1
            else:
                try:
                    mob = int(mob)
                    if mob < 0:
                        messagebox.showerror(message = "Mobile No. Cant be Negative")
                        flag=1
                except ValueError:
                    messagebox.showerror(message = "Mobile No. needs to be an integer!!")
                    flag=1
            if flag==0:
                pass1 = generate_password_hash(pass1)
                db.execute("""INSERT INTO users(username,email,mobile,hash1,pan) VALUES(?, ?,?,?,?)""", user,email,mob,pass1,pan)
                cur_idT = db.execute("SELECT id FROM users WHERE username = ?", user).fetchone()
                global cur_id
                cur_id = cur_idT.id
                print(cur_id)
                controller.add()
                self.txtuser.dell()
                self.txtpass.dell()
                self.txtpass1.dell()
                self.txtpass2.dell()
                self.txtpass3.dell()
                self.txtpass4.dell()
                mails()
                controller.show_frame("Watchlist_Window")




        logoimg = Image.open(r"logo.png")
        logoimg = logoimg.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg)
        lblimg1 = tk.Label(self,image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)

        loginbtn2 = tk.Button(self,text="Login",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Login_Window"))
        loginbtn2.place(x=1209.48,y=35.84,width=82.53,height=45)

        regbtn2 = tk.Button(self,text="Register",font=("Arial",25),fg="#007BFF",bg="#131722",borderwidth=0)
        regbtn2.place(x=1019.76,y=35.84,width=122.37,height=45)

        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)

        frame = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame.place(x=413.48,y=139.09,width=539.76,height=596.48)

        get_str = tk.Label(frame,text="Create Account",font=("Arial",25),fg="white",bg="#131722")
        get_str.place(x=152,y=20,width=235,height=40)

        self.txtuser = Placeholder(frame,placeholder='  Full Name',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
        self.txtuser.place(x=95,y=95,width=350.99,height=52.91)

        self.txtpass = Placeholder(frame,placeholder='  Email Address',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
        self.txtpass.place(x=95,y=160,width=350.99,height=52.91)

        self.txtpass1 = Placeholder(frame,placeholder='  Password',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
        self.txtpass1.place(x=95,y=225,width=350.99,height=52.91)

        self.txtpass2 = Placeholder(frame,placeholder='  Confirm Password',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
        self.txtpass2.place(x=95,y=290,width=350.99,height=52.91)

        self.txtpass3 = Placeholder(frame,placeholder='  Pan Number',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
        self.txtpass3.place(x=95,y=355,width=350.99,height=52.91)

        self.txtpass4 = Placeholder(frame,placeholder='  Mobile Number',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
        self.txtpass4.place(x=95,y=420,width=350.99,height=52.91)



        loginbtn = tk.Button(frame,text="Register",font=("Arial",20,"bold"),activeforeground="white",activebackground="black",fg="white",bg="#007BFF",command=check)
        loginbtn.place(x=95,y=501,width=350.99,height=52.91)



class Watchlist_Window(tk.Frame):

    def __init__(self, parent, controller):
        self.parent=parent
        tk.Frame.__init__(self, parent,bg='#131722')
        self.controller = controller
        self.controller.title("Macs")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(4)




        price1 = []
        data = yf.Ticker("^NSEI")
        price1.append({'name':data.info['shortName'],'symbol':data.info['symbol'],'price':data.info['regularMarketPrice']})

        logoimg = Image.open(r"logo.png")
        logoimg = logoimg.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg)
        lblimg1 = tk.Label(self,image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)


        Newsbtn = tk.Button(self,text="News",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda:controller.show_frame("News_Window"))
        Newsbtn.place(x=265,y=52,width=88,height=41)


        Watchbtn = tk.Button(self,text="Watchlist",font=("Arial",25),fg="#007BFF",bg="#131722",borderwidth=0)
        Watchbtn.place(x=474,y=54,width=156,height=41)


        portbtn = tk.Button(self,text="Portfolio",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda:controller.show_frame("Portfolio_Window"))
        portbtn.place(x=769,y=52,width=136,height=41)


        ordbtn = tk.Button(self,text="Orders",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda:controller.show_frame("Orders_Window"))
        ordbtn.place(x=1011,y=52,width=104,height=41)



        img = Image.open("profile14.png")
        img = img.resize((60,60),Image.ANTIALIAS)

        self.photoImg =  ImageTk.PhotoImage(img)

        img1 = Image.open("profileicon2.png")
        img1 = img1.resize((35,35),Image.ANTIALIAS)

        self.profile =  ImageTk.PhotoImage(img1)

        img2 = Image.open("fund.png")
        img2 = img2.resize((30,30),Image.ANTIALIAS)

        self.fund =  ImageTk.PhotoImage(img2)

        self.profile =  ImageTk.PhotoImage(img1)

        img3 = Image.open("theme2.png")
        img3 = img3.resize((30,30),Image.ANTIALIAS)

        self.theme2 =  ImageTk.PhotoImage(img3)


        img4 = Image.open("logout2.png")
        img4 = img4.resize((30,30),Image.ANTIALIAS)

        self.logout =  ImageTk.PhotoImage(img4)



        mainmenu1 = tk.Menubutton(self, image=self.photoImg,bg="#131722",relief="flat",activebackground="#131722")
        mainmenu1.place(x=1280,y=30.97,width=70,height=70)

        submenu1 = tk.Menu(mainmenu1,fg='white',font=("Roboto",18),bg="#131722",borderwidth=1,tearoff=0,activeborderwidth=7,activeforeground="blue",activebackground="#131722",relief="flat")
        #submenu1.place(x=1370,y=30.97,width=70,height=70)

#Where 0 is the index of the desired
        mainmenu1.config(menu=submenu1)



        #submenu1.config(bg="#131722")

        #submenu1.add_command(tk.Button="Option 1.1")


        submenu1.add_command(label="                           ",image=self.photoImg,compound='center')
        global namez
        namez= db.execute("""SELECT username from users where id = ?""",cur_id).fetchone()
        submenu1.add_command(label=namez[0],compound='top')
        submenu1.add_separator()

#
        submenu1.add_command(image=self.profile,label="     Profile",compound='left',command=lambda:controller.show_frame("Profile_Window"))
        submenu1.add_command(label="     Funds",image=self.fund,compound='left',command=lambda:controller.show_frame("Funds_Window"))
        submenu1.add_command(label="     Theme",image=self.theme2,compound='left')
        submenu1.add_command(label="     Log Out",image=self.logout,compound='left',command=lambda:popup4(self,self.parent,self.controller))

        submenu1.entryconfig(6, activeforeground='red')

        submenu1.entryconfig(1, activeforeground='white')
        def make_w():
            watch = db.execute("""SELECT *from watchlist where user_id=?""",cur_id).fetchall()
            if watch is None:
                pass
            else:
                watch1=[i for i in watch]
                for watch in watch1:
                    symbol1.insert(0,str(watch[1]))
                    name1.insert(0,str(watch[2]))
                    for row in range(len(symbol1)):
                        for column in range(3):
                            if row == 0:
                                if column == 0:
                                    label=tk.Label(self.scrollable_frame,text=name1[row],bg="#131722",font=("Arial",13,"bold"),fg="white",padx=45,pady=10,anchor='w')
                                    label.bind('<Button-1>',get_graph)
                                    label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                                    self.scrollable_frame.grid_columnconfigure(column,weight=1)
                                elif column == 2:
                                    button=tk.Button(self.scrollable_frame,text="Remove",bg="red",fg="white",padx=30,pady=10)
                                    button.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                                    button['command']=lambda btn_remove=button:remove_data(btn_remove)
                                    self.scrollable_frame.grid_columnconfigure(column,weight=1)
                                else:
                                    data = yf.Ticker(symbol1[row])
                                    s_p = data.info['regularMarketPrice']
                                    label=tk.Label(self.scrollable_frame,text=s_p,bg="#131722",font=("Arial",12),fg="#26DE81",padx=35,pady=10)
                                    label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                                    self.scrollable_frame.grid_columnconfigure(column,weight=1)
                                    price.insert(0,s_p)
                            else:
                                if column == 0:
                                    label=tk.Label(self.scrollable_frame,text=name1[row],bg="#131722",font=("Arial",13,"bold"),fg="white",padx=45,pady=10,anchor='w')
                                    label.bind('<Button-1>',get_graph)
                                    label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                                    self.scrollable_frame.grid_columnconfigure(column,weight=1)
                                elif column == 2:
                                    button=tk.Button(self.scrollable_frame,text="Remove",bg="red",fg="white",padx=30,pady=10)
                                    button.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                                    button['command']=lambda btn_remove=button:remove_data(btn_remove)
                                    self.scrollable_frame.grid_columnconfigure(column,weight=1)
                                else:
                                    data = price[row]
                                    label=tk.Label(self.scrollable_frame,text=data,bg="#131722",font=("Arial",12),fg="#26DE81",padx=35,pady=10)
                                    label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                                    self.scrollable_frame.grid_columnconfigure(column,weight=1)








        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)
        def click(*args):
            self.txtserc.delete(0, 'end')
            lblimg2.place_forget()
        global symbol1
        global name1
        symbol1 = []
        name1 = []
        price = []
        def remove_data(btn_remove):
            row1 = btn_remove.grid_info()['row']
            symbol1.pop(row1)
            name1.pop(row1)
            price.pop(row1)
            for label in self.scrollable_frame.grid_slaves():
                if int(label.grid_info()['row'])==row1:
                    label.grid_forget()
                elif int(label.grid_info()['row']) > row1:
                    label.grid(row=label.grid_info()['row'] -1,column=label.grid_info()['column'])

        def leave(*args):
            keyword = self.txtserc.get()
            self.txtserc.delete(0, 'end')
            self.txtserc.insert(0,'      Search')
            lblimg2.place(x=120,y=290,width=35,height=35)
            url = (f'https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm={keyword}?device=console&returnMeta=true')

            response = requests.get(url)



            i = json.loads(response.content)['data']['items'][0]
            symbol1.insert(0,str(i['symbol']))
            name1.insert(0,str(i['name']))

            for label in self.scrollable_frame.grid_slaves():
                label.grid_forget()
            for row in range(len(symbol1)):
                for column in range(3):
                    if row == 0:
                        if column == 0:
                            label=tk.Label(self.scrollable_frame,text=name1[row],bg="#131722",font=("Arial",13,"bold"),fg="white",padx=45,pady=10,anchor='w')
                            label.bind('<Button-1>',get_graph)
                            label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                            self.scrollable_frame.grid_columnconfigure(column,weight=1)
                        elif column == 2:
                            button=tk.Button(self.scrollable_frame,text="Remove",bg="red",fg="white",padx=30,pady=10)
                            button.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                            button['command']=lambda btn_remove=button:remove_data(btn_remove)
                            self.scrollable_frame.grid_columnconfigure(column,weight=1)
                        else:
                            data = yf.Ticker(symbol1[row])
                            s_p = data.info['regularMarketPrice']
                            label=tk.Label(self.scrollable_frame,text=s_p,bg="#131722",font=("Arial",12),fg="#26DE81",padx=35,pady=10)
                            label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                            self.scrollable_frame.grid_columnconfigure(column,weight=1)
                            price.insert(0,s_p)
                    else:
                        if column == 0:
                            label=tk.Label(self.scrollable_frame,text=name1[row],bg="#131722",font=("Arial",13,"bold"),fg="white",padx=45,pady=10,anchor='w')
                            label.bind('<Button-1>',get_graph)
                            label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                            self.scrollable_frame.grid_columnconfigure(column,weight=1)
                        elif column == 2:
                            button=tk.Button(self.scrollable_frame,text="Remove",bg="red",fg="white",padx=30,pady=10)
                            button.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                            button['command']=lambda btn_remove=button:remove_data(btn_remove)
                            self.scrollable_frame.grid_columnconfigure(column,weight=1)
                        else:
                            data = price[row]
                            label=tk.Label(self.scrollable_frame,text=data,bg="#131722",font=("Arial",12),fg="#26DE81",padx=35,pady=10)
                            label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                            self.scrollable_frame.grid_columnconfigure(column,weight=1)
            self.focus_set()




        self.txtserc=tk.Entry(self,font=("Arial",25,"bold"),bg="#2A2E39",fg="#4F5966")
        self.txtserc.insert(0,'      Search')
        self.txtserc.place(x=106,y=280,width=350,height=50)
        self.txtserc.bind("<Button-1>", click)
        self.txtserc.bind("<Return>", leave)

        logoimg1 = Image.open('Search.png')
        logoimg1 = logoimg1.resize((35,35),Image.ANTIALIAS)
        self.photoimage12 = ImageTk.PhotoImage(logoimg1)
        lblimg2 = tk.Label(self,image=self.photoimage12,bg="#2A2E39",borderwidth=0)
        lblimg2.place(x=120,y=290,width=35,height=35)


        def get_graph(event):
            global row2
            row2 = event.widget.grid_info()['row']
            plt.clf()
            price1[0]['symbol']=symbol1[row2]
            price1[0]['name']=name1[row2]
            price1[0]['price']=price[row2]

            for label in self.scrollable_frame.grid_slaves():
                if int(label.grid_info()['row'])==row2:
                    label.config(bg='#2A2E39')
                    if int(label.grid_info()['column'])==2:
                        label.config(bg='red')
                else:
                    label.config(bg='#131722')
                    if int(label.grid_info()['column'])==2:
                        label.config(bg='red')

            data1 = yf.download(
                tickers = symbol1[row2],
                period = "1d",
                interval = "1m",
                auto_adjust = False,
                prepost = False,
                threads = True,
                proxy = None
            )

            data1['Adj Close'].plot()
            plt.title(name1[row2])
            plt.savefig('books_read.png')
            graph = Image.open('books_read.png')
            graph = graph.resize((680,350),Image.ANTIALIAS)
            self.photoimage2 = ImageTk.PhotoImage(graph)
            lblimg1 = tk.Label(self,image=self.photoimage2,bg="#131722",borderwidth=0)
            lblimg1.place(x=619,y=250,width=680,height=365)

        def clickAbout():
            def sell():
                quan = quantity_entry.get()
                price1 = price_entry.get()
                flag=0
                if state == 1:
                    if not quan:
                        messagebox.showerror(message = "Quantity needed!!")
                    else:
                        try:
                            quan = int(quan)
                            if quan < 0:
                                messagebox.showerror(message = "Quantity Cant be Negative")
                                flag=1
                        except ValueError:
                            messagebox.showerror(message = "Quantity needs to be an integer!!")
                            flag=1
                elif state == 0:
                    if not quan or not price1:
                        messagebox.showerror(message = "Fields Cannot be Empty!!")
                    else:
                        try:
                            quan = int(quan)
                            price1 = int(price1)
                            if quan < 0 or price1 < 0:
                                messagebox.showerror(message = "Entries Cant be Negative")
                                flag=1
                        except ValueError:
                            messagebox.showerror(message = "Entries needs to be an integer!!")
                            flag=1
                if flag==0:
                    if state == 1:
                        price = a3.cget('text')
                        name = a1.cget('text')
                        sym = a2.cget('text')
                        s_id = db.execute("""SELECT stock_id from stocks where stock_symbol=?""", sym).fetchone()
                        if s_id is None:
                            messagebox.showerror(message = "You dont own any shares of" + str(sym))
                            toplevel.destroy()
                        own = db.execute("""SELECT shares from owned where stock_id=? and user_id=?""", s_id[0], cur_id).fetchone()
                        if own is None:
                            messagebox.showerror(message = "You dont own any shares of" + str(sym))
                            toplevel.destroy()
                        if quan <= int(own[0]):
                            if(int(quan) == own[0]):
                                cash = db.execute("""SELECT cash from users where id=?""", cur_id).fetchone()
                                bal = (int(quan)*float(price))+float(cash[0])
                                time = datetime.datetime.now()
                                db.execute("""UPDATE users set cash=? where id=?""", int(bal), cur_id)
                                db.execute("""DELETE FROM owned WHERE stock_id=? AND user_id=?""", s_id[0], cur_id)
                                db.execute("""INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)""",
                                            s_id[0], cur_id, -int(quan), "sell", price, time)
                                controller.history("Watchlist_Window")
                                toplevel.destroy()
                            else:
                                shares = int(own[0]) - int(quan)
                                time = datetime.datetime.now()
                                cash = db.execute("""SELECT cash from users where id=?""", cur_id).fetchone()
                                bal = (int(quan)*float(price))+float(cash[0])
                                db.execute("UPDATE users set cash=? where id=?", int(bal), cur_id)
                                db.execute("UPDATE owned set shares=? where stock_id=? and user_id=?", int(shares), s_id[0], cur_id)
                                db.execute("INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)",
                                            s_id[0], cur_id, -int(quan), "sell", price, time)
                                controller.history("Watchlist_Window")
                                toplevel.destroy()
                        else:
                            messagebox.showerror(message = "You dont own enough shares of" + str(sym))
                            toplevel.destroy()
                    elif state == 0:
                        price = a3.cget('text')
                        name = a1.cget('text')
                        sym = a2.cget('text')
                        if price == price1:
                            if quan <= int(own[0]):
                                if(int(quan) == own[0]):
                                    cash = db.execute("""SELECT cash from users where id=?""", cur_id).fetchone()
                                    bal = (int(quan)*float(price))+float(cash[0])
                                    time = datetime.datetime.now()
                                    db.execute("""UPDATE users set cash=? where id=?""", int(bal), cur_id)
                                    db.execute("""DELETE FROM owned WHERE stock_id=? AND user_id=?""", s_id[0], cur_id)
                                    db.execute("""INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)""",
                                                s_id[0], cur_id, -int(quan), "sell", price, time)
                                    controller.history("Watchlist_Window")
                                    toplevel.destroy()
                                else:
                                    shares = int(own[0]) - int(quan)
                                    time = datetime.datetime.now()
                                    cash = db.execute("""SELECT cash from users where id=?""", cur_id).fetchone()
                                    bal = (int(quan)*float(price))+float(cash[0])
                                    db.execute("UPDATE users set cash=? where id=?", int(bal), cur_id)
                                    db.execute("UPDATE owned set shares=? where stock_id=? and user_id=?", int(shares), s_id[0], cur_id)
                                    db.execute("INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)",
                                                s_id[0], cur_id, -int(quan), "sell", price, time)
                                    controller.history("Watchlist_Window")
                                    toplevel.destroy()
                            else:
                                messagebox.showerror(message = "You dont own enough shares of  " + str(sym))
                                toplevel.destroy()
                        else:
                            s_id = db.execute("""SELECT stock_id from stocks where stock_symbol=?""", sym).fetchone()
                            own = db.execute("""SELECT shares from owned where stock_id=? and user_id=?""", s_id[0], cur_id).fetchone()
                            if s_id is None:
                                messagebox.showerror(message = "You dont own any shares of" + str(sym))
                                toplevel.destroy()
                            elif own is None:
                                messagebox.showerror(message = "You dont own any shares of" + str(sym))
                                toplevel.destroy()
                            else:
                                if quan <= int(own[0]):
                                    dict = {"price":price1,"sym":sym,"type":"SELL"}
                                    l.append(dict)
                                    controller.order("Watchlist_Window")
                                    toplevel.destroy()
                                else:
                                    messagebox.showerror(message = "You dont own enough shares of" + str(sym))
                                    toplevel.destroy()






            def test(event):
                    global state
                    if state == 1:
                        price_entry.delete(0,'end')
                        price_entry.config(state='normal')
                        winbtntest.config(image=winbtn1)
                        state = 0
                    else:
                        price_entry.delete(0,'end')
                        price_entry.config(disabledbackground="#131722",state='disabled')
                        winbtntest.config(image=winbtn0)
                        state = 1

            toplevel = tk.Toplevel()
            toplevel.geometry("605x364+381+254")
            toplevel.configure(bg="#131722")



            a1 = tk.Label(toplevel,text = price1[0]['name'],font=("Arial",15),fg="white",bg="#131722",anchor='w')
            a1.place(x=78,y=39,width=300,height=20)

            a2 = tk.Label(toplevel,text = price1[0]['symbol'],font=("Arial",10),fg="#4F5966",bg="#131722",anchor='w')
            a2.place(x=78,y=58,width=100,height=14)

            a3 = tk.Label(toplevel,text=price[row2],font=("Arial",18),fg="white",bg="#131722",anchor='w')
            a3.place(x=435,y=40,width=100,height=21)

            my_canvas1 = tk.Canvas(toplevel,width=605,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas1.pack(pady=87)

            price_label = tk.Label(toplevel,text="Price",font=("Arial",15),fg="#4F5966",bg="#131722",anchor='w')
            price_label.place(x=26,y=165,width=47,height=20)
            price_entry = tk.Entry(toplevel,font=("Arial",10),fg="white",bg="#131722",relief="flat")
            price_entry.place(x=26,y=193)
            my_canvas2 = tk.Canvas(toplevel,width=170,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas2.place(x=19,y=215)

            quantity_label = tk.Label(toplevel,text="Quantity",font=("Arial",15),fg="#4F5966",bg="#131722",anchor='w')
            quantity_label.place(x=265,y=105,width=75,height=20)
            quantity_entry = tk.Entry(toplevel,font=("Arial",10),fg="white",bg="#131722",relief="flat")
            quantity_entry.place(x=286,y=130)
            my_canvas3 = tk.Canvas(toplevel,width=170,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas3.place(x=215,y=150)

            winbtn0 = ImageTk.PhotoImage(file="market.png")
            winbtn1 = ImageTk.PhotoImage(file="limit.png")

            winbtntest = tk.Label(toplevel,image=winbtn1,bg="#131722")
            winbtntest.place(x=374,y=173)
            winbtntest.bind("<Button-1>",test)

            sellbtn1 = tk.Button(toplevel,text="SELL",font=("Arial",18),fg="white",bg="#FF231F",borderwidth=0,command=sell)
            sellbtn1.place(x=148,y=278,width=308,height=66)

        def clickAbout1():

            def buy():
                quan = quantity_entry.get()
                price1 = price_entry.get()
                flag=0
                if state == 1:
                    if not quan:
                        messagebox.showerror(message = "Quantity needed!!")
                    else:
                        try:
                            quan = int(quan)
                            if quan < 0:
                                messagebox.showerror(message = "Quantity Cant be Negative")
                                flag=1
                        except ValueError:
                            messagebox.showerror(message = "Quantity needs to be an integer!!")
                            flag=1
                elif state == 0:
                    if not quan or not price1:
                        messagebox.showerror(message = "Fields Cannot be Empty!!")
                    else:
                        try:
                            quan = int(quan)
                            price1 = int(price1)
                            if quan < 0 or price1 < 0:
                                messagebox.showerror(message = "Entries Cant be Negative")
                                flag=1
                        except ValueError:
                            messagebox.showerror(message = "Entries needs to be an integer!!")
                            flag=1
                if flag==0:
                    if state == 1:
                        price = a3.cget('text')
                        name = a1.cget('text')
                        sym = a2.cget('text')
                        bal = db.execute("""SELECT cash FROM users where id=?""", cur_id).fetchone()
                        if int(bal[0]) >= (int(price) * int(quan)):
                            stock = db.execute("SELECT *from stocks where stock_name= ?",name).fetchone()
                            if stock is None:
                                db.execute("""INSERT INTO stocks(stock_name,stock_symbol) VALUES(?,?)""", name, sym)
                                stock = db.execute("SELECT *from stocks where stock_name= ?",name).fetchone()
                            exist = db.execute("SELECT shares,price from owned where stock_id=? and user_id=?", stock[0], cur_id).fetchone()
                            if exist is None:
                                db.execute("INSERT INTO owned(stock_id,user_id,shares,price) VALUES(?,?,?,?)",
                                                                stock[0], cur_id, quan, price)
                            else:
                                new_price = (float(price*quan) + float(exist[0]*float(exist[1])))/(exist[0] + quan)
                                new_price = round(new_price,3)
                                exist[0] = exist[0] + quan
                                db.execute("UPDATE owned set shares=? where stock_id=? and user_id=?", exist[0], stock[0], cur_id)
                                db.execute("UPDATE owned set price=? where stock_id=? and user_id=?", new_price, stock[0], cur_id)
                            time = datetime.datetime.now()

                            db.execute("INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)",
                            stock[0], cur_id, quan, "buy", price, time)
                            bal = db.execute("SELECT cash from users where id = ?", cur_id).fetchone()
                            new_bal = int(bal[0]) - (int(price) * int(quan))
                            db.execute("""update users set cash=? where id=? """, new_bal, cur_id)
                            controller.history("Watchlist_Window")
                            toplevel.destroy()
                        else:
                            messagebox.showerror(message="Not sufficient balance!!")
                    elif state == 0:
                        price = a3.cget('text')
                        name = a1.cget('text')
                        sym = a2.cget('text')
                        if price == price1:
                            bal = db.execute("""SELECT cash FROM users where id=?""", cur_id).fetchone()
                            if int(bal[0]) >= (int(price) * int(quan)):
                                stock = db.execute("SELECT *from stocks where stock_name= ?",name).fetchone()
                                if stock is None:
                                    db.execute("""INSERT INTO stocks(stock_name,stock_symbol) VALUES(?,?)""", name, sym)
                                    stock = db.execute("SELECT *from stocks where stock_name= ?",name).fetchone()
                                exist = db.execute("SELECT shares from owned where stock_id=? and user_id=?", stock[0], cur_id).fetchone()
                                if exist is None:
                                    db.execute("INSERT INTO owned(stock_id,user_id,shares,price) VALUES(?,?,?,?)",
                                                                    stock[0], cur_id, quan, price)
                                else:
                                    new_price = (float(price*quan) + float(exist[0]*float(exist[1])))/(exist[0] + quan)
                                    new_price = round(new_price,3)
                                    exist[0] = exist[0] + quan
                                    db.execute("UPDATE owned set shares=? where stock_id=? and user_id=?", exist[0], stock[0], cur_id)
                                    db.execute("UPDATE owned set price=? where stock_id=? and user_id=?", new_price, stock[0], cur_id)
                                time = datetime.datetime.now()

                                db.execute("INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)",
                                stock[0], cur_id, quan, "buy", price, time)
                                bal = db.execute("SELECT cash from users where id = ?", cur_id).fetchone()
                                new_bal = int(bal[0]) - (int(price) * int(quan))
                                db.execute("""update users set cash=? where id=? """, new_bal, cur_id)
                                controller.history("Watchlist_Window")
                                toplevel.destroy()
                            else:
                                messagebox.showerror(message="Not sufficient balance!!")
                        else:
                            bal = db.execute("""SELECT cash FROM users where id=?""", cur_id).fetchone()
                            if int(bal[0]) >= (int(price) * int(quan)):
                                dict = {"price":price1,"sym":sym,"type":"BUY"}
                                l.append(dict)
                                controller.order("Watchlist_Window")
                                toplevel.destroy()
                            else:
                                messagebox.showerror(message="Not sufficient balanace!!")
                                toplevel.destroy()





            def test(event):
                    global state
                    if state == 1:
                        price_entry.delete(0,'end')
                        price_entry.config(state='normal')
                        winbtntest.config(image=winbtn1)
                        state = 0
                    else:
                        price_entry.delete(0,'end')
                        price_entry.config(disabledbackground="#131722",state='disabled')
                        winbtntest.config(image=winbtn0)
                        state = 1

            toplevel = tk.Toplevel()
            toplevel.geometry("605x364+381+254")
            toplevel.configure(bg="#131722")

            a1 = tk.Label(toplevel,text = price1[0]['name'],font=("Arial",15),fg="white",bg="#131722",anchor='w')
            a1.place(x=78,y=39,width=300,height=20)

            a2 = tk.Label(toplevel,text = price1[0]['symbol'],font=("Arial",10),fg="#4F5966",bg="#131722",anchor='w')
            a2.place(x=78,y=58,width=100,height=14)

            a3 = tk.Label(toplevel,text=price[row2],font=("Arial",18),fg="white",bg="#131722",anchor='w')
            a3.place(x=435,y=40,width=100,height=21)

            my_canvas1 = tk.Canvas(toplevel,width=605,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas1.pack(pady=87)

            price_label = tk.Label(toplevel,text="Price",font=("Arial",15),fg="#4F5966",bg="#131722",anchor='w')
            price_label.place(x=26,y=165,width=47,height=20)
            price_entry = tk.Entry(toplevel,font=("Arial",10),fg="white",bg="#131722",relief="flat")
            price_entry.place(x=26,y=193)
            my_canvas2 = tk.Canvas(toplevel,width=170,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas2.place(x=19,y=215)

            quantity_label = tk.Label(toplevel,text="Quantity",font=("Arial",15),fg="#4F5966",bg="#131722",anchor='w')
            quantity_label.place(x=265,y=105,width=75,height=20)
            quantity_entry = tk.Entry(toplevel,font=("Arial",10),fg="white",bg="#131722",relief="flat")
            quantity_entry.place(x=286,y=130)
            my_canvas3 = tk.Canvas(toplevel,width=170,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas3.place(x=215,y=150)

            winbtn0 = ImageTk.PhotoImage(file="market.png")
            winbtn1 = ImageTk.PhotoImage(file="limit.png")

            winbtntest = tk.Label(toplevel,image=winbtn1,bg="#131722")
            winbtntest.place(x=374,y=173)
            winbtntest.bind("<Button-1>",test)

            buybtn = tk.Button(toplevel,text="BUY",font=("Arial",18),fg="white",bg="#26DE81",borderwidth=0,command=buy)
            buybtn.place(x=148,y=278,width=308,height=66)

        buybtn = tk.Button(self,text="BUY",font=("Arial",25),fg="white",bg="#26DE81",borderwidth=0,command=clickAbout1)
        buybtn.place(x=700,y=640,width=250,height=77)


        sellbtn = tk.Button(self,text="SELL",font=("Arial",25),fg="white",bg="#FF231F",borderwidth=0,command=clickAbout)
        sellbtn.place(x=980,y=640,width=250,height=77)


        frame1 = tk.Frame(self,bg="#1C2030",highlightbackground="#2A2E39",highlightthickness=1)
        frame1.place(x=40,y=150,width=250,height=100)


        frame2 = tk.Frame(self,bg="#1C2030",highlightbackground="#2A2E39",highlightthickness=1)
        frame2.place(x=330,y=150,width=250,height=100)


        frame3 = tk.Frame(self,bg="#1C2030",highlightbackground="#2A2E39",highlightthickness=1)
        frame3.place(x=49,y=350,width=539.76,height=365)


        frame4 = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame4.place(x=619,y=250,width=680,height=365)

        a1 = tk.Label(frame1,text ='Nifty',font=("Arial",16,"bold"),fg="white",bg="#1C2030")
        a1.place(x=18,y=29,width=43,height=26)
        a6 = tk.Label(frame1,text='NSE INDEX',font=("Arial",10),fg="#4F5966",bg="#1C2030")
        a6.place(x=18,y=63,width=70,height=16)

        a2 = tk.Label(frame2,text ='Sensex',font=("Arial",16,"bold"),fg="white",bg="#1C2030")
        a2.place(x=18,y=29,width=73,height=26)
        a6 = tk.Label(frame2,text='BSE INDEX',font=("Arial",10),fg="#4F5966",bg="#1C2030")
        a6.place(x=18,y=63,width=70,height=16)

        data69 = yf.Ticker("^NSEI")

        a3 = tk.Label(frame1,text =data69.info['regularMarketPrice'],font=("Arial",10),fg="#4F5966",bg="#1C2030")
        a3.place(x=165,y=63,width=62,height=16)

        change1 = str(round((data69.info['regularMarketPrice']-data69.info['previousClose'])*100/data69.info['regularMarketPrice'],2))+"%"
        a4 = tk.Label(frame1,text=change1,font=("Arial",19),fg="#26DE81",bg="#1C2030")
        change1 = round((data69.info['regularMarketPrice']-data69.info['previousClose'])*100/data69.info['regularMarketPrice'],2)
        if change1 < 0 :
            a4.config(fg="#FF231F")
        a4.place(x=165,y=29,width=75,height=26)

        data = yf.Ticker("^BSESN")

        a3 = tk.Label(frame2,text =data.info['regularMarketPrice'],font=("Arial",10),fg="#4F5966",bg="#1C2030")
        a3.place(x=165,y=63,width=62,height=16)

        change1 = str(round((data.info['regularMarketPrice']-data.info['previousClose'])*100/data.info['regularMarketPrice'],2))+"%"
        a5 = tk.Label(frame2,text=change1,font=("Arial",19),fg="#26DE81",bg="#1C2030")
        change2 = round((data.info['regularMarketPrice']-data.info['previousClose'])*100/data.info['regularMarketPrice'],2)
        if change2 < 0 :
            a5.config(fg="#FF231F")
        a5.place(x=165,y=29,width=75,height=26)

        canvas = tk.Canvas(frame3,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        scrollbar = tk.Scrollbar(frame3, orient="vertical", command=canvas.yview,bg="light steel blue", troughcolor="steel blue")
        self.scrollable_frame = tk.Frame(canvas,bg="#131722")
        self.scrollable_frame.grid_columnconfigure(0, minsize=230)
        self.scrollable_frame.grid_columnconfigure(1,minsize=160)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        data1 = yf.download(
                tickers = "^NSEI",
                period = "1d",
                interval = "1m",
                auto_adjust = False,
                prepost = False,
                threads = True,
                proxy = None
            )

        data1['Adj Close'].plot()
        plt.title("NIFTY")
        plt.savefig('books_read.png')
        graph = Image.open('books_read.png')
        graph = graph.resize((680,350),Image.ANTIALIAS)
        self.photoimage2 = ImageTk.PhotoImage(graph)
        lblimg1 = tk.Label(self,image=self.photoimage2,bg="#131722",borderwidth=0)
        lblimg1.place(x=619,y=250,width=680,height=365)

        make_w()

        def func1():
            while 1:
                try:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(update_continous, symbol1)
                        return_value = future.result()
                        print(return_value)
                    print(self.scrollable_frame.grid_slaves(),len(self.scrollable_frame.grid_slaves()))
                    x1 = 0
                    return_value = return_value[::-1]
                    for label in self.scrollable_frame.grid_slaves():
                        if int(label.grid_info()['column']) == 1:
                            label.config(text=str(return_value[x1]))
                            price[x1] = return_value[x1]
                            x1 = x1+1
                    price.reverse()
                    time.sleep(10)
                except 	Exception as e:
                    print(e)
                    time.sleep(5)
        t1 = threading.Thread(target=func1,daemon=True)
        t1.start()



class Funds_Window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#131722')
        self.parent=parent
        self.controller = controller
        self.controller.title("Macs")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(5)

        frameb = tk.Frame(self, bg="#131722")
        frameb.place(x=0, y=0, width=200, height=94.72)

        logoimg1 = Image.open(r"logo.png")
        logoimg1 = logoimg1.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg1)
        lblimg1 = tk.Label(frameb,image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)



        Newsbtn = tk.Button(self,text="News",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("News_Window"))
        Newsbtn.place(x=265,y=52,width=88,height=41)


        Watchbtn = tk.Button(self,text="Watchlist",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Watchlist_Window"))
        Watchbtn.place(x=474,y=54,width=156,height=41)


        portbtn = tk.Button(self,text="Portfolio",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Portfolio_Window"))
        portbtn.place(x=769,y=52,width=136,height=41)


        ordbtn = tk.Button(self,text="Orders",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Orders_Window"))
        ordbtn.place(x=1011,y=52,width=104,height=41)







        img = Image.open("profile14.png")
        img = img.resize((60,60),Image.ANTIALIAS)

        self.photoImg =  ImageTk.PhotoImage(img)

        img1 = Image.open("profileicon2.png")
        img1 = img1.resize((35,35),Image.ANTIALIAS)

        self.profile =  ImageTk.PhotoImage(img1)

        img2 = Image.open(r"fund.png")
        img2 = img2.resize((30,30),Image.ANTIALIAS)

        self.fund =  ImageTk.PhotoImage(img2)

        self.profile =  ImageTk.PhotoImage(img1)

        img3 = Image.open(r"theme2.png")
        img3 = img3.resize((30,30),Image.ANTIALIAS)

        self.theme2 =  ImageTk.PhotoImage(img3)


        img4 = Image.open(r"logout2.png")
        img4 = img4.resize((30,30),Image.ANTIALIAS)

        self.logout =  ImageTk.PhotoImage(img4)



        mainmenu1 = tk.Menubutton(self, image=self.photoImg,bg="#131722",relief="flat")
        mainmenu1.place(x=1280,y=30.97,width=70,height=70)

        submenu1 = tk.Menu(mainmenu1,fg='white',font=("Roboto",18),bg="#131722",borderwidth=1,tearoff=0,activeborderwidth=7,activeforeground="blue",activebackground="#131722",relief="flat")
        #submenu1.place(x=1370,y=30.97,width=70,height=70)

#Where 0 is the index of the desired
        mainmenu1.config(menu=submenu1)



        #submenu1.config(bg="#131722")

        #submenu1.add_command(tk.Button="Option 1.1")


        submenu1.add_command(label="                           ",image=self.photoImg,compound='center')


        submenu1.add_command(label=namez[0],compound='top')
        submenu1.add_separator()

#
        submenu1.add_command(image=self.profile,label="     Profile",compound='left',command=lambda: controller.show_frame("Profile_Window"))
        submenu1.add_command(label="     Funds",image=self.fund,compound='left',)
        submenu1.add_command(label="     Theme",image=self.theme2,compound='left')
        submenu1.add_command(label="     Log Out",image=self.logout,compound='left',command=lambda: popup4(self,self.parent,self.controller))


        submenu1.entryconfig(6, activeforeground='red')

        submenu1.entryconfig(1, activeforeground='white')


        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)


        frame = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame.place(x=40,y=140,width=1280,height=500)
        get_str = tk.Label(frame,text="Funds",font=("Arial",25,"bold"),fg="#AFFAFF",bg="#131722")
        get_str.place(x=620,y=30,width=100,height=40.11)


        frame1 = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame1.place(x=109,y=220,width=1150,height=320)

        amarginlabel = tk.Label(self,text="Available margin to trade:",font=("Arial",14),bg="#1C2030",fg="white")
        amarginlabel.place(x=550,y=250,width=300,height=40)

        print(cur_id)
        amargin=db.execute("""SELECT cash from users where id=?""",cur_id).fetchone()
        amargin1label = tk.Label(self,text="₹" +str(amargin[0]),font=("Arial",30),bg="#1C2030",fg="white")
        amargin1label.place(x=550,y=285,width=300,height=100)


        umarginlabel = tk.Label(self,text="Used Margin:",font=("Arial",15),bg="black",fg="white")
        umarginlabel.place(x=500,y=450,width=200,height=70)


        umargin1label = tk.Label(self,text="₹ 5000",font=("Arial",15),bg="black",fg="red")
        umargin1label.place(x=700,y=450,width=200,height=70)


        def clickAbout():

            toplevel = tk.Toplevel()
            toplevel.geometry("605x364+381+254")
            toplevel.configure(bg="#131722")

            def check():
                Funds=self.txtuser.get()
                flag=0

                cur_funds = db.execute("""SELECT cash from users where id=?""",cur_id).fetchone()
                print(cur_funds)
                if not Funds:
                    messagebox.showerror(message = "Fields cannot be empty!!")
                    flag=1
                else:
                    try:
                        Funds = int(Funds)
                        if Funds < 0:
                            messagebox.showerror(message = "Funds Cant be negative")
                            flag=1
                            toplevel.destroy()
                        elif int(cur_funds[0]) > 1999:
                            messagebox.showerror(message = "You can only add more funds if your balance falls below 2000!!")
                            flag=1
                            toplevel.destroy()
                        elif Funds>8000:
                            messagebox.showerror(message = "You can only add maximum ₹ 8000 !!")
                            flag=1
                            toplevel.destroy()

                    except ValueError:
                        messagebox.showerror(message = "Funds needs to be an integer!!")
                        flag=1
                        toplevel.destroy()

                if flag==0:

                    db.execute("""update users set cash=cash+  ? where id =?""", Funds,cur_id)
                    amargin=db.execute("""SELECT cash from users where id=?""",cur_id).fetchone()

                    print(amargin)
                    amargin1label.config(text="₹" + str(amargin[0]))


                    toplevel.destroy()



            a1 = tk.Label(toplevel,text ="Add Funds",font=("Arial",20),fg="white",bg="#131722",anchor='w')
            a1.place(x=230,y=39,width=300,height=20)

            self.txtuser = Placeholder(toplevel,placeholder='  Funds',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
            self.txtuser.place(x=100,y=100,width=400,height=52.91)



            add1btn = tk.Button(toplevel,text="Add",font=("Arial",20,"bold"),activeforeground="white",activebackground="black",fg="white",bg="#007BFF",command=check)
            add1btn.place(x=130,y=200,width=350.99,height=52.91)





        addbtn = tk.Button(self,text="Add Funds",font=("Arial",18),fg="white",bg="#1C2030",borderwidth=0,command=clickAbout)
        addbtn.place(x=460,y=560,width=195,height=50)


        hisbtn = tk.Button(self,text="History",font=("Arial",18),fg="white",bg="#1C2030",borderwidth=0,command=lambda: controller.show_frame("History_Window"))
        hisbtn.place(x=784,y=560,width=195,height=50)

class News_Window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#131722')
        self.parent=parent
        self.controller = controller
        self.controller.title("Macs")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(6)



        logoimg = Image.open(r"logo.png")
        logoimg = logoimg.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg)
        lblimg1 = tk.Label(image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)


        Newsbtn = tk.Button(self,text="News",font=("Arial",25),fg="#007BFF",bg="#131722",borderwidth=0)
        Newsbtn.place(x=265,y=52,width=88,height=41)


        Watchbtn = tk.Button(self,text="Watchlist",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Watchlist_Window"))
        Watchbtn.place(x=474,y=54,width=156,height=41)


        portbtn = tk.Button(self,text="Portfolio",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Portfolio_Window"))
        portbtn.place(x=769,y=52,width=136,height=41)


        ordbtn = tk.Button(self,text="Orders",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Orders_Window"))
        ordbtn.place(x=1011,y=52,width=104,height=41)

        img = Image.open("profile14.png")
        img = img.resize((60,60),Image.ANTIALIAS)

        self.photoImg =  ImageTk.PhotoImage(img)

        img1 = Image.open("profileicon2.png")
        img1 = img1.resize((35,35),Image.ANTIALIAS)

        self.profile =  ImageTk.PhotoImage(img1)

        img2 = Image.open(r"fund.png")
        img2 = img2.resize((30,30),Image.ANTIALIAS)

        self.fund =  ImageTk.PhotoImage(img2)

        self.profile =  ImageTk.PhotoImage(img1)

        img3 = Image.open(r"theme2.png")
        img3 = img3.resize((30,30),Image.ANTIALIAS)

        self.theme2 =  ImageTk.PhotoImage(img3)


        img4 = Image.open(r"logout2.png")
        img4 = img4.resize((30,30),Image.ANTIALIAS)

        self.logout =  ImageTk.PhotoImage(img4)



        mainmenu1 = tk.Menubutton(self, image=self.photoImg,bg="#131722",relief="flat",activebackground="#131722")
        mainmenu1.place(x=1280,y=30.97,width=70,height=70)

        submenu1 = tk.Menu(mainmenu1,fg='white',font=("Roboto",18),bg="#131722",borderwidth=1,tearoff=0,activeborderwidth=7,activeforeground="blue",activebackground="#131722",relief="flat")
        #submenu1.place(x=1370,y=30.97,width=70,height=70)

#Where 0 is the index of the desired
        mainmenu1.config(menu=submenu1)



        #submenu1.config(bg="#131722")

        #submenu1.add_command(Button="Option 1.1")


        submenu1.add_command(label="                           ",image=self.photoImg,compound='center')


        submenu1.add_command(label=namez[0],compound='top')
        submenu1.add_separator()

#
        submenu1.add_command(image=self.profile,label="     Profile",compound='left',command=lambda: controller.show_frame("Profile_Window"))
        submenu1.add_command(label="     Funds",image=self.fund,compound='left',command=lambda: controller.show_frame("Funds_Window"))
        submenu1.add_command(label="     Theme",image=self.theme2,compound='left')
        submenu1.add_command(label="     Log Out",image=self.logout,compound='left',command=lambda: popup4(self,self.parent,self.controller))

        submenu1.entryconfig(6, activeforeground='red')

        submenu1.entryconfig(1, activeforeground='white')


        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)

        frame = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame.place(x=40,y=190,width=1280,height=500)
        get_str = tk.Label(frame,text="NEWS",font=("Arial",25,"bold"),fg="#AFFAFF",bg="#131722")
        get_str.grid(row=0,column=0,sticky='W',pady=10,padx=640)

        b1 = tk.Canvas(frame,width=1100,height=1,bg="#2A2E39",highlightthickness=0)
        b1.grid(row=1,sticky='W',padx=80)


        def callback(url):
            webbrowser.open_new(url)
        url = ('https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=8e374c366b5d4df6b5a4070b93779427')

        response = requests.get(url)
        response = response.json()

        a1 = tk.Label(frame,text = (unicodedata.normalize('NFKD',response['articles'][0]['title']).encode('ascii', 'ignore')).decode('utf-8'),font=("Arial",20),fg="white",bg="#131722", anchor='e' )
        a1.grid(row=2,column=0,sticky='W',pady=20)
        a1.bind("<Button-1>",lambda e,url=url:callback(response['articles'][0]['url']))

        b2 = tk.Canvas(frame,width=1100,height=1,bg="#2A2E39",highlightthickness=0)
        b2.grid(row=3,sticky='W',padx=80)

        a2 = tk.Label(frame,text = (unicodedata.normalize('NFKD',response['articles'][1]['title']).encode('ascii', 'ignore')).decode('utf-8'),font=("Arial",20),fg="white",bg="#131722", anchor='e' )
        a2.grid(row=4,column=0,sticky='W',pady=20)
        a2.bind("<Button-1>",lambda e,url=url:callback(response['articles'][1]['url']))

        b3 = tk.Canvas(frame,width=1100,height=1,bg="#2A2E39",highlightthickness=0)
        b3.grid(row=5,sticky='W',padx=80)

        a3 = tk.Label(frame,text = (unicodedata.normalize('NFKD',response['articles'][2]['title']).encode('ascii', 'ignore')).decode('utf-8'),font=("Arial",20),fg="white",bg="#131722", anchor='e' )
        a3.grid(row=6,column=0,sticky='W',pady=20)
        a3.bind("<Button-1>",lambda e,url=url:callback(response['articles'][2]['url']))

        b4 = tk.Canvas(frame,width=1100,height=1,bg="#2A2E39",highlightthickness=0)
        b4.grid(row=7,sticky='W',padx=80)

        a4 = tk.Label(frame,text = (unicodedata.normalize('NFKD',response['articles'][3]['title']).encode('ascii', 'ignore')).decode('utf-8'),font=("Arial",20),fg="white",bg="#131722", anchor='e' )
        a4.grid(row=8,column=0,sticky='W',pady=20)
        a4.bind("<Button-1>",lambda e,url=url:callback(response['articles'][3]['url']))

        b5 = tk.Canvas(frame,width=1100,height=1,bg="#2A2E39",highlightthickness=0)
        b5.grid(row=9,sticky='W',padx=80)

        a5 = tk.Label(frame,text = (unicodedata.normalize('NFKD',response['articles'][4]['title']).encode('ascii', 'ignore')).decode('utf-8'),font=("Arial",20),fg="white",bg="#131722", anchor='e' )
        a5.grid(row=10,column=0,sticky='W',pady=20)
        a5.bind("<Button-1>",lambda e,url=url:callback(response['articles'][4]['url']))

        b6 = tk.Canvas(frame,width=1100,height=1,bg="#2A2E39",highlightthickness=0)
        b6.grid(row=11,sticky='W',padx=80)



class Portfolio_Window(tk.Frame):

    def __init__(self,parent,controller):
        print(7)
        global used_marg
        def get_graph(event):
            global locate
            locate = event.widget.grid_info()['row']
            q=0

            for label in self.scrollable_frame.grid_slaves():
                if int(label.grid_info()['row'])==locate:
                    label.config(bg='red')
                    if label.grid_info()['column'] in [0,1,4]:
                        hist_data[q] = label['text']
                        q = q+1
                else:
                    label.config(bg='#1C2030')
        self.parent=parent
        tk.Frame.__init__(self,parent,bg="#131722")
        self.controller = controller
        self.controller.title("News")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        self.controller.configure(bg="#131722")


        logoimg = Image.open(r"logo.png")
        logoimg = logoimg.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg)
        lblimg1 = tk.Label(image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)


        Newsbtn = tk.Button(self,text="News",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("News_Window"))
        Newsbtn.place(x=265,y=52,width=88,height=41)


        Watchbtn = tk.Button(self,text="Watchlist",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Watchlist_Window"))
        Watchbtn.place(x=474,y=54,width=156,height=41)


        portbtn = tk.Button(self,text="Portfolio",font=("Arial",25),fg="#007BFF",bg="#131722",borderwidth=0,)
        portbtn.place(x=769,y=52,width=136,height=41)


        ordbtn = tk.Button(self,text="Orders",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Orders_Window"))
        ordbtn.place(x=1011,y=52,width=104,height=41)


        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)

        frame1 = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame1.place(x=20,y=144,width=1317,height=586)

        frame2 = tk.Frame(frame1,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame2.place(x=81,y=21,width=1165,height=420)

        def clickAbout():
            def sell():
                quan = quantity_entry.get()
                price1 = price_entry.get()
                flag=0
                if state == 1:
                    if not quan:
                        messagebox.showerror(message = "Quantity needed!!")
                    else:
                        try:
                            quan = int(quan)
                            if quan < 0:
                                messagebox.showerror(message = "Quantity Cant be Negative")
                                flag=1
                        except ValueError:
                            messagebox.showerror(message = "Quantity needs to be an integer!!")
                            flag=1
                elif state == 0:
                    if not quan or not price1:
                        messagebox.showerror(message = "Fields Cannot be Empty!!")
                    else:
                        try:
                            quan = int(quan)
                            price1 = int(price1)
                            if quan < 0 or price1 < 0:
                                messagebox.showerror(message = "Entries Cant be Negative")
                                flag=1
                        except ValueError:
                            messagebox.showerror(message = "Entries needs to be an integer!!")
                            flag=1
                if flag==0:
                    if state == 1:
                        print(locate)
                        print(port_table)

                        price = port_table[locate-1][3]
                        name = port_table[locate-1][1]
                        sym = port_table[locate-1][0]
                        s_id = db.execute("""SELECT stock_id from stocks where stock_symbol=?""", sym).fetchone()
                        if s_id is None:
                            messagebox.showerror(message = "You dont own any shares of" + str(sym))
                            toplevel.destroy()
                        own = db.execute("""SELECT shares from owned where stock_id=? and user_id=?""", s_id[0], cur_id).fetchone()
                        if own is None:
                            messagebox.showerror(message = "You dont own any shares of" + str(sym))
                            toplevel.destroy()
                        if quan <= int(own[0]):
                            if(int(quan) == own[0]):
                                cash = db.execute("""SELECT cash from users where id=?""", cur_id).fetchone()
                                bal = (int(quan)*float(price))+float(cash[0])
                                time = datetime.datetime.now()
                                db.execute("""UPDATE users set cash=? where id=?""", int(bal), cur_id)
                                db.execute("""DELETE FROM owned WHERE stock_id=? AND user_id=?""", s_id[0], cur_id)
                                db.execute("""INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)""",
                                            s_id[0], cur_id, -int(quan), "sell", price, time)
                                controller.history("Portfolio_Window")
                                toplevel.destroy()
                            else:
                                shares = int(own[0]) - int(quan)
                                time = datetime.datetime.now()
                                cash = db.execute("""SELECT cash from users where id=?""", cur_id).fetchone()
                                bal = (int(quan)*float(price))+float(cash[0])
                                db.execute("UPDATE users set cash=? where id=?", int(bal), cur_id)
                                db.execute("UPDATE owned set shares=? where stock_id=? and user_id=?", int(shares), s_id[0], cur_id)
                                db.execute("INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)",
                                            s_id[0], cur_id, -int(quan), "sell", price, time)
                                controller.history("Portfolio_Window")
                                toplevel.destroy()
                        else:
                            messagebox.showerror(message = "You dont own enough shares of" + str(sym))
                            toplevel.destroy()
                    elif state == 0:
                        price = port_table[locate-1][3]
                        name = port_table[locate-1][1]
                        sym = port_table[locate-1][0]
                        if price == price1:
                            if quan <= int(own[0]):
                                if(int(quan) == own[0]):
                                    cash = db.execute("""SELECT cash from users where id=?""", cur_id).fetchone()
                                    bal = (int(quan)*float(price))+float(cash[0])
                                    time = datetime.datetime.now()
                                    db.execute("""UPDATE users set cash=? where id=?""", int(bal), cur_id)
                                    db.execute("""DELETE FROM owned WHERE stock_id=? AND user_id=?""", s_id[0], cur_id)
                                    db.execute("""INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)""",
                                                s_id[0], cur_id, -int(quan), "sell", price, time)
                                    controller.history("Portfolio_Window")
                                    toplevel.destroy()
                                else:
                                    shares = int(own[0]) - int(quan)
                                    time = datetime.datetime.now()
                                    cash = db.execute("""SELECT cash from users where id=?""", cur_id).fetchone()
                                    bal = (int(quan)*float(price))+float(cash[0])
                                    db.execute("UPDATE users set cash=? where id=?", int(bal), cur_id)
                                    db.execute("UPDATE owned set shares=? where stock_id=? and user_id=?", int(shares), s_id[0], cur_id)
                                    db.execute("INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)",
                                                s_id[0], cur_id, -int(quan), "sell", price, time)
                                    controller.history("Portfolio_Window")
                                    toplevel.destroy()
                            else:
                                messagebox.showerror(message = "You dont own enough shares of  " + str(sym))
                                toplevel.destroy()
                        else:
                            s_id = db.execute("""SELECT stock_id from stocks where stock_symbol=?""", sym).fetchone()
                            own = db.execute("""SELECT shares from owned where stock_id=? and user_id=?""", s_id[0], cur_id).fetchone()
                            if s_id is None:
                                messagebox.showerror(message = "You dont own any shares of" + str(sym))
                                toplevel.destroy()
                            elif own is None:
                                messagebox.showerror(message = "You dont own any shares of" + str(sym))
                                toplevel.destroy()
                            else:
                                if quan <= int(own[0]):
                                    dict = {"price":price1,"sym":sym,"type":"SELL"}
                                    global l
                                    l.append(dict)
                                    controller.order("Portfolio_Window")
                                    toplevel.destroy()
                                else:
                                    messagebox.showerror(message = "You dont own enough shares of" + str(sym))
                                    toplevel.destroy()

            def test(event):
                    global state
                    if state == 1:
                        price_entry.delete(0,'end')
                        price_entry.config(state='normal')
                        winbtntest.config(image=winbtn1)
                        state = 0
                    else:
                        price_entry.delete(0,'end')
                        price_entry.config(disabledbackground="#131722",state='disabled')
                        winbtntest.config(image=winbtn0)
                        state = 1


            toplevel = tk.Toplevel()
            toplevel.geometry("605x364+381+254")
            toplevel.configure(bg="#131722")

            a1 = tk.Label(toplevel,text = hist_data[1],font=("Arial",15),fg="white",bg="#131722",anchor="w")
            a1.place(x=78,y=39,width=300,height=20)

            a2 = tk.Label(toplevel,text = hist_data[2],font=("Arial",10),fg="#4F5966",bg="#131722",anchor="w")
            a2.place(x=78,y=58,width=100,height=14)

            a3 = tk.Label(toplevel,text = hist_data[0],font=("Arial",18),fg="white",bg="#131722",anchor="w")
            a3.place(x=435,y=40,width=92,height=21)

            my_canvas1 = tk.Canvas(toplevel,width=605,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas1.pack(pady=87)

            price_label = tk.Label(toplevel,text="Price",font=("Arial",15),fg="#4F5966",bg="#131722",anchor="w")
            price_label.place(x=26,y=165,width=47,height=20)
            price_entry = tk.Entry(toplevel,font=("Arial",10),fg="white",bg="#131722",relief="flat")
            price_entry.place(x=26,y=193)
            my_canvas2 = tk.Canvas(toplevel,width=170,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas2.place(x=19,y=215)

            quantity_label = tk.Label(toplevel,text="Quantity",font=("Arial",15),fg="#4F5966",bg="#131722",anchor="w")
            quantity_label.place(x=265,y=105,width=75,height=20)
            quantity_entry = tk.Entry(toplevel,font=("Arial",10),fg="white",bg="#131722",relief="flat")
            quantity_entry.place(x=286,y=130)
            my_canvas3 = tk.Canvas(toplevel,width=170,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas3.place(x=215,y=150)

            winbtn0 = ImageTk.PhotoImage(file="market.png")
            winbtn1 = ImageTk.PhotoImage(file="limit.png")

            winbtntest = tk.Label(toplevel,image=winbtn0,bg="#131722")
            winbtntest.place(x=374,y=173)
            winbtntest.bind("<Button-1>",test)

            sellbtn1 = tk.Button(toplevel,text="SELL",font=("Arial",18),fg="white",bg="#FF231F",borderwidth=0,command=sell)
            sellbtn1.place(x=148,y=278,width=308,height=66)

        def clickAbout1():


            def buy():
                quan = quantity_entry.get()
                price1 = price_entry.get()
                flag=0
                if state == 1:
                    if not quan:
                        messagebox.showerror(message = "Quantity needed!!")
                    else:
                        try:
                            quan = int(quan)
                            if quan < 0:
                                messagebox.showerror(message = "Quantity Cant be Negative")
                                flag=1
                        except ValueError:
                            messagebox.showerror(message = "Quantity needs to be an integer!!")
                            flag=1
                elif state == 0:
                    if not quan or not price1:
                        messagebox.showerror(message = "Fields Cannot be Empty!!")
                    else:
                        try:
                            quan = int(quan)
                            price1 = int(price1)
                            if quan < 0 or price1 < 0:
                                messagebox.showerror(message = "Entries Cant be Negative")
                                flag=1
                        except ValueError:
                            messagebox.showerror(message = "Entries needs to be an integer!!")
                            flag=1
                if flag==0:
                    if state == 1:
                        price = port_table[locate-1][3]
                        name = port_table[locate-1][1]
                        sym = port_table[locate-1][0]
                        bal = db.execute("""SELECT cash FROM users where id=?""", cur_id).fetchone()
                        if int(bal[0]) >= (int(price) * int(quan)):
                            stock = db.execute("SELECT *from stocks where stock_name= ?",name).fetchone()
                            if stock is None:
                                db.execute("""INSERT INTO stocks(stock_name,stock_symbol) VALUES(?,?)""", name, sym)
                                stock = db.execute("SELECT *from stocks where stock_name= ?",name).fetchone()
                            exist = db.execute("SELECT shares,price from owned where stock_id=? and user_id=?", stock[0], cur_id).fetchone()
                            if exist is None:
                                db.execute("INSERT INTO owned(stock_id,user_id,shares,price) VALUES(?,?,?,?)",
                                                                stock[0], cur_id, quan, price)
                            else:
                                new_price = (float(price*quan) + float(exist[0]*float(exist[1])))/(exist[0] + quan)
                                new_price = round(new_price,3)
                                exist[0] = exist[0] + quan
                                db.execute("UPDATE owned set shares=? where stock_id=? and user_id=?", exist[0], stock[0], cur_id)
                                db.execute("UPDATE owned set price=? where stock_id=? and user_id=?", new_price, stock[0], cur_id)
                            time = datetime.datetime.now()

                            db.execute("INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)",
                            stock[0], cur_id, quan, "buy", price, time)
                            bal = db.execute("SELECT cash from users where id = ?", cur_id).fetchone()
                            new_bal = int(bal[0]) - (int(price) * int(quan))
                            db.execute("""update users set cash=? where id=? """, new_bal, cur_id)
                            controller.history("Portfolio_Window")
                            toplevel.destroy()
                        else:
                            messagebox.showerror(message="Not sufficient balance!!")
                    elif state == 0:
                        price = port_table[locate-1][3]
                        name = port_table[locate-1][1]
                        sym = port_table[locate-1][0]
                        if price == price1:
                            bal = db.execute("""SELECT cash FROM users where id=?""", cur_id).fetchone()
                            if int(bal[0]) >= (int(price) * int(quan)):
                                stock = db.execute("SELECT *from stocks where stock_name= ?",name).fetchone()
                                if stock is None:
                                    db.execute("""INSERT INTO stocks(stock_name,stock_symbol) VALUES(?,?)""", name, sym)
                                    stock = db.execute("SELECT *from stocks where stock_name= ?",name).fetchone()
                                exist = db.execute("SELECT shares from owned where stock_id=? and user_id=?", stock[0], cur_id).fetchone()
                                if exist is None:
                                    db.execute("INSERT INTO owned(stock_id,user_id,shares,price) VALUES(?,?,?,?)",
                                                                    stock[0], cur_id, quan, price)
                                else:
                                    new_price = (float(price*quan) + float(exist[0]*float(exist[1])))/(exist[0] + quan)
                                    new_price = round(new_price,3)
                                    exist[0] = exist[0] + quan
                                    db.execute("UPDATE owned set shares=? where stock_id=? and user_id=?", exist[0], stock[0], cur_id)
                                    db.execute("UPDATE owned set price=? where stock_id=? and user_id=?", new_price, stock[0], cur_id)
                                time = datetime.datetime.now()

                                db.execute("INSERT INTO transactions(stock_id,user_id,shares,type,price,transacted) VALUES(?,?,?,?,?,?)",
                                stock[0], cur_id, quan, "buy", price, time)
                                bal = db.execute("SELECT cash from users where id = ?", cur_id).fetchone()
                                new_bal = int(bal[0]) - (int(price) * int(quan))
                                db.execute("""update users set cash=? where id=? """, new_bal, cur_id)
                                controller.history("Portfolio_Window")
                                toplevel.destroy()
                            else:
                                messagebox.showerror(message="Not sufficient balance!!")
                        else:
                            bal = db.execute("""SELECT cash FROM users where id=?""", cur_id).fetchone()
                            if int(bal[0]) >= (int(price) * int(quan)):
                                dict = {"price":price1,"sym":sym,"type":"BUY"}
                                global l
                                l.append(dict)
                                controller.order("Portfolio_Window")
                                toplevel.destroy()
                            else:
                                messagebox.showerror(message="Not sufficient balanace!!")
                                toplevel.destroy()





            def test(event):
                    global state
                    if state == 1:
                        price_entry.delete(0,'end')
                        price_entry.config(state='normal')
                        winbtntest.config(image=winbtn1)
                        state = 0
                    else:
                        price_entry.delete(0,'end')
                        price_entry.config(disabledbackground="#131722",state='disabled')
                        winbtntest.config(image=winbtn0)
                        state = 1


            toplevel = tk.Toplevel()
            toplevel.geometry("605x364+381+254")
            toplevel.configure(bg="#131722")

            a1 = tk.Label(toplevel,text = hist_data[1],font=("Arial",15),fg="white",bg="#131722",anchor="w")
            a1.place(x=78,y=39,width=300,height=20)

            a2 = tk.Label(toplevel,text = hist_data[2],font=("Arial",10),fg="#4F5966",bg="#131722",anchor="w")
            a2.place(x=78,y=58,width=100,height=14)

            a3 = tk.Label(toplevel,text= hist_data[0],font=("Arial",18),fg="white",bg="#131722",anchor="w")
            a3.place(x=435,y=40,width=92,height=21)

            my_canvas1 = tk.Canvas(toplevel,width=605,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas1.pack(pady=87)

            price_label = tk.Label(toplevel,text="Price",font=("Arial",15),fg="#4F5966",bg="#131722",anchor="w")
            price_label.place(x=26,y=165,width=47,height=20)
            price_entry = tk.Entry(toplevel,font=("Arial",10),fg="white",bg="#131722",relief="flat")
            price_entry.place(x=26,y=193)
            my_canvas2 = tk.Canvas(toplevel,width=170,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas2.place(x=19,y=215)

            quantity_label = tk.Label(toplevel,text="Quantity",font=("Arial",15),fg="#4F5966",bg="#131722",anchor="w")
            quantity_label.place(x=265,y=105,width=75,height=20)
            quantity_entry = tk.Entry(toplevel,font=("Arial",10),fg="white",bg="#131722",relief="flat")
            quantity_entry.place(x=286,y=130)
            my_canvas3 = tk.Canvas(toplevel,width=170,height=1,bg="#2A2E39",highlightthickness=0)
            my_canvas3.place(x=215,y=150)

            winbtn0 = ImageTk.PhotoImage(file="market.png")
            winbtn1 = ImageTk.PhotoImage(file="limit.png")

            winbtntest = tk.Label(toplevel,image=winbtn0,bg="#131722")
            winbtntest.place(x=374,y=173)
            winbtntest.bind("<Button-1>",test)

            buybtn = tk.Button(toplevel,text="BUY",font=("Arial",18),fg="white",bg="#26DE81",borderwidth=0,command=buy)
            buybtn.place(x=148,y=278,width=308,height=66)


        buybtn = tk.Button(self,text="BUY",font=("Arial",25),fg="white",bg="#26DE81",borderwidth=0,command=clickAbout1)
        buybtn.place(x=420,y=620,width=200,height=70)


        sellbtn = tk.Button(self,text="SELL",font=("Arial",25),fg="white",bg="#FF231F",borderwidth=0,command=clickAbout)
        sellbtn.place(x=720,y=620,width=200,height=70)


        canvas = tk.Canvas(frame2,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        scrollbar = tk.Scrollbar(frame2, orient="vertical", command=canvas.yview,bg="light steel blue", troughcolor="steel blue")
        self.scrollable_frame = tk.Frame(canvas,bg="#131722")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        tab1_col = [{"SYMBOL","NAME","SHARES"},{"Avg. Buy\nPrice","CURRENT\nPRICE"},{"UL G/L","TOTAL"}]
        global port_table
        port_table=db.execute("SELECT stock_symbol,stock_name,shares,price,price*shares as total from users inner join owned  on users.id = owned.user_id join stocks on stocks.stock_id = owned.stock_id where id=?",cur_id).fetchall()
        print(port_table)
        x1=0
        l=[]
        for port in port_table:
            a = yf.Ticker(port[0])
            l.append(round(a.info['regularMarketPrice'],3))

        print(l)
        for row in range(len(port_table)+1):
            for column in range(7):
                if row==0:
                        label = tk.Label(self.scrollable_frame, text=tab1_col[column],bg="#1C2030", fg="white", padx=43, pady=15)
                        label.config(font=('Arial', 14))
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=8)
                        canvas.grid_columnconfigure(column, weight=1)
                else:
                        if column in [0,1,2,3,6]:
                            print(row-1,x1)
                            label=tk.Label(self.scrollable_frame,text=str(port_table[row-1][x1]),bg="#1C2030",fg="white",padx=3,pady=10)
                            x1=x1+1
                        elif column == 4:
                            label=tk.Label(self.scrollable_frame,text="₹"+ str(l[row-1]),bg="#1C2030",fg="white",padx=3,pady=10)
                        elif column == 5:
                            a = l[row-1]*float(port_table[row-1][2]) - float(port_table[row-1][2])*float(port_table[row-1][3])
                            a=round(a,3)

                            if a > 0:col = "#26DE81"
                            elif a<0:col = "#FF231F"
                            else:col = "#888"

                            label=tk.Label(self.scrollable_frame,text="₹"+str(a) ,bg="#1C2030",fg=col,padx=3,pady=10)
                        if column == 0:
                            label.bind('<Button-1>',get_graph)
                        label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                        canvas.grid_columnconfigure(column,weight=1)

            x1=0

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        '''
        scrollBar = Scrollbar(frame2)
        scrollBar.pack(side = RIGHT, fill = Y)

        tab1=Canvas(frame2,bg="#131722",yscrollcommand=scrollBar.set )
        tab1_col = ["SYMBOL","NAME","SHARES","Avg. Buy\nPrice","CURRENT\nPRICE","UL G/L","TOTAL"]
        for row in range(5):
            for column in range(7):
                if row==0:
                        label = Label(tab1, text=tab1_col[column],bg="#1C2030", fg="white", padx=3, pady=15)
                        label.config(font=('Arial', 14))
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=8)
                        tab1.grid_columnconfigure(column, weight=1)

                else:
                        label=Label(tab1,text="Data "+str(row)+" "+str(column),bg="#1C2030",fg="white",padx=3,pady=10)
                        label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                        tab1.grid_columnconfigure(column,weight=1)

        tab1.pack(fill="both")
        scrollBar.config(scrollregion=tab1.bbox("all"),command=tab1.yview)'''









        img = Image.open("profile14.png")
        img = img.resize((60,60),Image.ANTIALIAS)

        self.photoImg =  ImageTk.PhotoImage(img)

        img1 = Image.open("profileicon2.png")
        img1 = img1.resize((35,35),Image.ANTIALIAS)

        self.profile =  ImageTk.PhotoImage(img1)

        img2 = Image.open("fund.png")
        img2 = img2.resize((30,30),Image.ANTIALIAS)

        self.fund =  ImageTk.PhotoImage(img2)

        self.profile =  ImageTk.PhotoImage(img1)

        img3 = Image.open("theme2.png")
        img3 = img3.resize((30,30),Image.ANTIALIAS)

        self.theme2 =  ImageTk.PhotoImage(img3)


        img4 = Image.open("logout2.png")
        img4 = img4.resize((30,30),Image.ANTIALIAS)

        self.logout =  ImageTk.PhotoImage(img4)



        mainmenu1 = tk.Menubutton(self, image=self.photoImg,bg="#131722",relief="flat")
        mainmenu1.place(x=1280,y=30.97,width=70,height=70)

        submenu1 = tk.Menu(mainmenu1,fg='white',font=("Roboto",18),bg="#131722",borderwidth=1,tearoff=0,activeborderwidth=7,activeforeground="blue",activebackground="#131722",relief="flat")
        #submenu1.place(x=1370,y=30.97,width=70,height=70)

#Where 0 is the index of the desired
        mainmenu1.config(menu=submenu1)



        #submenu1.config(bg="#131722")

        #submenu1.add_command(Button="Option 1.1")


        submenu1.add_command(label="                           ",image=self.photoImg,compound='center')


        submenu1.add_command(label=namez[0],compound='top')
        submenu1.add_separator()

#
        submenu1.add_command(image=self.profile,label="     Profile",compound='left',command=lambda: controller.show_frame("Profile_Window"))
        submenu1.add_command(label="     Funds",image=self.fund,compound='left',command=lambda: controller.show_frame("Funds_Window"))
        submenu1.add_command(label="     Theme",image=self.theme2,compound='left')
        submenu1.add_command(label="     Log Out",image=self.logout,compound='left',command=lambda: popup4(self,self.parent,self.controller))


        submenu1.entryconfig(6, activeforeground='red')

        submenu1.entryconfig(1, activeforeground='white')

        refimg = Image.open(r"reload.png")
        refimg = refimg.resize((50,50),Image.ANTIALIAS)
        self.photoimage7 = ImageTk.PhotoImage(refimg)
        refbut = tk.Button(frame1,image=self.photoimage7,bg="#131722",borderwidth=0,command=lambda: controller.port())
        refbut.place(x=1100,y=500,width=50,height=50)



class History_Window(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#131722')
        self.parent=parent
        self.controller = controller
        self.controller.title("Macs")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(8)

        frameb = tk.Frame(self, bg="#131722")
        frameb.place(x=0, y=0, width=200, height=94.72)

        logoimg1 = Image.open(r"logo.png")
        logoimg1 = logoimg1.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg1)
        lblimg1 = tk.Label(frameb,image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)


        Newsbtn = tk.Button(self,text="News",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("News_Window"))
        Newsbtn.place(x=265,y=52,width=88,height=41)


        Watchbtn = tk.Button(self,text="Watchlist",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Watchlist_Window"))
        Watchbtn.place(x=474,y=54,width=156,height=41)


        portbtn = tk.Button(self,text="Portfolio",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Portfolio_Window"))
        portbtn.place(x=769,y=52,width=136,height=41)


        ordbtn = tk.Button(self,text="Orders",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Orders_Window"))
        ordbtn.place(x=1011,y=52,width=104,height=41)



        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)


        img = Image.open(r"profile14.png")
        img = img.resize((60,60),Image.ANTIALIAS)

        self.photoImg =  ImageTk.PhotoImage(img)

        img1 = Image.open(r"profileicon2.png")
        img1 = img1.resize((35,35),Image.ANTIALIAS)

        self.profile =  ImageTk.PhotoImage(img1)

        img2 = Image.open(r"fund.png")
        img2 = img2.resize((30,30),Image.ANTIALIAS)

        self.fund =  ImageTk.PhotoImage(img2)

        self.profile =  ImageTk.PhotoImage(img1)

        img3 = Image.open(r"theme2.png")
        img3 = img3.resize((30,30),Image.ANTIALIAS)

        self.theme2 =  ImageTk.PhotoImage(img3)


        img4 = Image.open(r"logout2.png")
        img4 = img4.resize((30,30),Image.ANTIALIAS)

        self.logout =  ImageTk.PhotoImage(img4)



        mainmenu1 = tk.Menubutton(self, image=self.photoImg,bg="#131722",relief="flat")
        mainmenu1.place(x=1280,y=30.97,width=70,height=70)

        submenu1 = tk.Menu(mainmenu1,fg='white',font=("Roboto",18),bg="#131722",borderwidth=1,tearoff=0,activeborderwidth=7,activeforeground="blue",activebackground="#131722",relief="flat")
        #submenu1.place(x=1370,y=30.97,width=70,height=70)

#Where 0 is the index of the desired
        mainmenu1.config(menu=submenu1)



        #submenu1.config(bg="#131722")

        #submenu1.add_command(tk.Button="Option 1.1")


        submenu1.add_command(label="                           ",image=self.photoImg,compound='center')


        submenu1.add_command(label=namez[0],compound='top')
        submenu1.add_separator()

#
        submenu1.add_command(image=self.profile,label="     Profile",compound='left',command=lambda: controller.show_frame("Profile_Window"))
        submenu1.add_command(label="     Funds",image=self.fund,compound='left',command=lambda: controller.show_frame("Funds_Window"))
        submenu1.add_command(label="     Theme",image=self.theme2,compound='left')
        submenu1.add_command(label="     Log Out",image=self.logout,compound='left',command=lambda: popup4(self,self.parent,self.controller))


        submenu1.entryconfig(6, activeforeground='red')

        submenu1.entryconfig(1, activeforeground='white')


        frame1 = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame1.place(x=20,y=144,width=1317,height=586)


        get_str = tk.Label(frame1,text="History",font=("Arial",25,"bold"),fg="#AFFAFF",bg="#131722")
        get_str.place(x=580,y=30,width=180,height=40.11)


        tab1=tk.Frame(frame1,bg="#131722")
        tab1.place(x=81,y=100,width=1165,height=420)


        canvas = tk.Canvas(tab1,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        scrollbar = tk.Scrollbar(tab1, orient="vertical", command=canvas.yview, highlightcolor="yellow", highlightbackground="black",troughcolor="blue")
        self.scrollable_frame = tk.Frame(canvas,bg="#131722")

        self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        hist_table = db.execute("""SELECT stocks.stock_symbol,stocks.stock_name,transactions.shares,transactions.price,transactions.transacted  from transactions inner join stocks on transactions.stock_id = stocks.stock_id where user_id=?""",cur_id).fetchall()
        print(hist_table)
        tab1_col = ["SYMBOL","NAME","SHARES","Price","Transaction time"]
        for row in range(len(hist_table)+1):
            for column in range(5):
                if row==0:
                        label = tk.Label(self.scrollable_frame, text=tab1_col[column],bg="#1C2030", fg="white", padx=74, pady=15)
                        label.config(font=('Arial', 14))
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=8)
                        tab1.grid_columnconfigure(column, weight=1)

                else:
                    if column == 3:
                        label=tk.Label(self.scrollable_frame,text="₹"+str(hist_table[row-1][column]),bg="#1C2030",fg="white",padx=3,pady=10)
                        label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                        tab1.grid_columnconfigure(column,weight=1)
                    else:
                        label=tk.Label(self.scrollable_frame,text=str(hist_table[row-1][column]),bg="#1C2030",fg="white",padx=3,pady=10)
                        label.grid(row=row,column=column,sticky="nsew",padx=1,pady=8)
                        tab1.grid_columnconfigure(column,weight=1)





        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class Orders_Window(tk.Frame):


    def __init__(self, parent, controller):
        self.parent=parent
        tk.Frame.__init__(self, parent,bg='#131722')
        self.controller = controller
        self.controller.title("Macs")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(9)


        price1 = []
        data = yf.Ticker("^NSEI")
        price1.append({'name':data.info['shortName'],'symbol':data.info['symbol'],'price':data.info['regularMarketPrice']})

        logoimg = Image.open(r"logo.png")
        logoimg = logoimg.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg)
        lblimg1 = tk.Label(self,image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)


        Newsbtn = tk.Button(self,text="News",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("News_Window"))
        Newsbtn.place(x=265,y=52,width=88,height=41)


        Watchbtn = tk.Button(self,text="Watchlist",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Watchlist_Window"))
        Watchbtn.place(x=474,y=54,width=156,height=41)


        portbtn = tk.Button(self,text="Portfolio",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Portfolio_Window"))
        portbtn.place(x=769,y=52,width=136,height=41)


        ordbtn = tk.Button(self,text="Orders",font=("Arial",25),fg="#007BFF",bg="#131722",borderwidth=0,)
        ordbtn.place(x=1011,y=52,width=104,height=41)



        img = Image.open(r"profile14.png")
        img = img.resize((60,60),Image.ANTIALIAS)

        self.photoImg =  ImageTk.PhotoImage(img)

        img1 = Image.open(r"profileicon2.png")
        img1 = img1.resize((35,35),Image.ANTIALIAS)

        self.profile =  ImageTk.PhotoImage(img1)

        img2 = Image.open(r"fund.png")
        img2 = img2.resize((30,30),Image.ANTIALIAS)

        self.fund =  ImageTk.PhotoImage(img2)

        self.profile =  ImageTk.PhotoImage(img1)

        img3 = Image.open(r"theme2.png")
        img3 = img3.resize((30,30),Image.ANTIALIAS)

        self.theme2 =  ImageTk.PhotoImage(img3)


        img4 = Image.open(r"logout2.png")
        img4 = img4.resize((30,30),Image.ANTIALIAS)

        self.logout =  ImageTk.PhotoImage(img4)



        mainmenu1 = tk.Menubutton(self, image=self.photoImg,bg="#131722",relief="flat",activebackground="#131722")
        mainmenu1.place(x=1280,y=30.97,width=70,height=70)

        submenu1 = tk.Menu(mainmenu1,fg='white',font=("Roboto",18),bg="#131722",borderwidth=1,tearoff=0,activeborderwidth=7,activeforeground="blue",activebackground="#131722",relief="flat")

        mainmenu1.config(menu=submenu1)



        #submenu1.config(bg="#131722")

        #submenu1.add_command(tk.Button="Option 1.1")


        submenu1.add_command(label="                           ",image=self.photoImg,compound='center')


        submenu1.add_command(label=namez[0],compound='top')
        submenu1.add_separator()


        submenu1.add_command(image=self.profile,label="     Profile",compound='left',command=lambda: controller.show_frame("Profile_Window"))
        submenu1.add_command(label="     Funds",image=self.fund,compound='left',command=lambda: controller.show_frame("Funds_Window"))
        submenu1.add_command(label="     Theme",image=self.theme2,compound='left',)
        submenu1.add_command(label="     Log Out",image=self.logout,compound='left',command=lambda: popup4(self,self.parent,self.controller))

        submenu1.entryconfig(6, activeforeground='red')

        submenu1.entryconfig(1, activeforeground='white')


        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)

        frame=tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame.place(x=70,y=150,width=1226,height=600)


        frame1 = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=3)
        frame1.place(x=400,y=190,width=650,height=520)

        #frame2 = Frame(self.root,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        #frame2.place(x=780,y=190,width=550,height=550)


        label1 = tk.Label(frame1,text="Pending orders",font=("Arial",30),fg="white",bg="#131722")
        label1.pack(pady=7)
        b2 = tk.Canvas(frame1,width=1000,height=1,bg="#2A2E39",highlightthickness=0)
        b2.pack(pady=10)
        global l
        if len(l)!=0:
            for list in l:
                frame3 = tk.Frame(frame1,bg='#131722',highlightbackground="#2A2E39",highlightthickness=2,height=60,width=570)
                frame3.pack(pady=10)
                frame3.pack_propagate(0)
                #frame3.minsize(600,40)
                print(l)
                if list['type']=="SELL":
                    get_str = tk.Button(frame3,text=str(list['type']),font=("Arial",25),fg="red",bg="#131722",borderwidth=0)
                    get_str.pack(side='left',padx=20)
                else:
                    get_str = tk.Button(frame3,text=str(list['type']),font=("Arial",25),fg="green",bg="#131722",borderwidth=0)
                    get_str.pack(side='left',padx=20)

                lbl1 = tk.Label(frame3,text=str(list['sym']),font=("Arial",25),fg="white",bg="#131722")
                lbl1.place(relx=0.5,rely=0.5,anchor='center')


                lbl2 = tk.Label(frame3,text="₹"+str(list["price"]),font=("Arial",25),fg="white",bg="#131722")
                lbl2.pack(side='right',padx=20)


class Profile_Window(tk.Frame):


    def __init__(self,parent,controller):
        self.parent=parent

        tk.Frame.__init__(self,parent,bg="#131722")
        self.controller = controller
        self.controller.title("News")
        self.controller.attributes('-fullscreen', True)
        self.controller.geometry("1366x768+0+0")
        print(10)


        frameb = tk.Frame(self, bg="#131722")
        frameb.place(x=0, y=0, width=200, height=94.72)

        logoimg1 = Image.open(r"logo.png")
        logoimg1 = logoimg1.resize((172,111),Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(logoimg1)
        lblimg1 = tk.Label(frameb,image=self.photoimage1,bg="#131722",borderwidth=0)
        lblimg1.place(x=17.08,y=5.97,width=163.16,height=94.72)





        Newsbtn = tk.Button(self,text="News",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("News_Window"))
        Newsbtn.place(x=265,y=52,width=88,height=41)


        Watchbtn = tk.Button(self,text="Watchlist",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Watchlist_Window"))
        Watchbtn.place(x=474,y=54,width=156,height=41)


        portbtn = tk.Button(self,text="Portfolio",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Portfolio_Window"))
        portbtn.place(x=769,y=52,width=136,height=41)


        ordbtn = tk.Button(self,text="Orders",font=("Arial",25),fg="white",bg="#131722",borderwidth=0,command=lambda: controller.show_frame("Orders_Window"))
        ordbtn.place(x=1011,y=52,width=104,height=41)


        my_canvas = tk.Canvas(self,width=1366,height=1,bg="#2A2E39",highlightthickness=0)
        my_canvas.pack(pady=100.69)


        def popup():
                def log_out():
                    toplevel.destroy()
                    controller.show_frame("Login_Window")


                def test(event):
                        global state
                        if state == 1:
                                winbtntest.config(image=winbtn0)
                                state = 0
                        else:
                                winbtntest.config(image=winbtn1)
                                state = 1

                def Close():
                        toplevel.destroy()



                toplevel = tk.Toplevel()
                toplevel.geometry("605x364+381+254")
                toplevel.configure(bg="#131722")



                a1 = tk.Label(toplevel,text ="Do you want to logout",font=("Arial",20),fg="white",bg="#131722",anchor="w")
                a1.place(x=150,y=100,width=300,height=30)


                btn1 = tk.Button(toplevel,text="Yes",font=("Arial",20,"bold"),activeforeground="white",activebackground="black",fg="white",bg="#007BFF",command=log_out)
                btn1.place(x=150,y=200,width=100,height=50)


                btn2 = tk.Button(toplevel,text="No",font=("Arial",20,"bold"),activeforeground="white",activebackground="black",fg="white",bg="#007BFF",command=Close)
                btn2.place(x=320,y=200,width=100,height=50)



        img = Image.open("profile14.png")
        img = img.resize((60,60),Image.ANTIALIAS)

        self.photoImg =  ImageTk.PhotoImage(img)

        img1 = Image.open("profileicon2.png")
        img1 = img1.resize((35,35),Image.ANTIALIAS)

        self.profile =  ImageTk.PhotoImage(img1)

        img2 = Image.open("fund.png")
        img2 = img2.resize((30,30),Image.ANTIALIAS)

        self.fund =  ImageTk.PhotoImage(img2)

        self.profile =  ImageTk.PhotoImage(img1)

        img3 = Image.open("theme2.png")
        img3 = img3.resize((30,30),Image.ANTIALIAS)

        self.theme2 =  ImageTk.PhotoImage(img3)


        img4 = Image.open("logout2.png")
        img4 = img4.resize((30,30),Image.ANTIALIAS)

        self.logout =  ImageTk.PhotoImage(img4)



        mainmenu1 = tk.Menubutton(self, image=self.photoImg,bg="#131722",relief="flat")
        mainmenu1.place(x=1280,y=30.97,width=70,height=70)

        submenu1 = tk.Menu(mainmenu1,fg='white',font=("Roboto",18),bg="#131722",borderwidth=1,tearoff=0,activeborderwidth=7,activeforeground="blue",activebackground="#131722",relief="flat")
                #submenu1.place(x=1370,y=30.97,width=70,height=70)

#Where 0 is the index of the desired
        mainmenu1.config(menu=submenu1)

                #submenu1.config(bg="#131722")

                #submenu1.add_command(Button="Option 1.1")


        submenu1.add_command(label="                           ",image=self.photoImg,compound='center')


        submenu1.add_command(label=namez[0],compound='top')
        submenu1.add_separator()

#
        submenu1.add_command(image=self.profile,label="     Profile",compound='left',)
        submenu1.add_command(label="     Funds",image=self.fund,compound='left',command=lambda: controller.show_frame("Funds_Window"))
        submenu1.add_command(label="     Theme",image=self.theme2,compound='left')
        submenu1.add_command(label="     Log Out",image=self.logout,compound='left',command=lambda: popup4(self,self.parent,self.controller) )



        submenu1.entryconfig(6, activeforeground='red')

        submenu1.entryconfig(1, activeforeground='white')


        frame = tk.Frame(self,bg="#131722",highlightbackground="#2A2E39",highlightthickness=1)
        frame.place(x=30,y=140,width=1300,height=600)


        get_str = tk.Label(frame,text="Profile",font=("Arial",25,"bold"),fg="#AFFAFF",bg="#131722")
        get_str.place(x=620,y=50,width=100,height=40.11)


        namelabel = tk.Label(self,text="Name",font=("Arial",18),bg="#1C2030",fg="white")
        namelabel.place(x=110,y=300,width=150,height=50)



        ucclabel = tk.Label(self,text="UCC",font=("Arial",18),bg="#1C2030",fg="white")
        ucclabel.place(x=110,y=355,width=150,height=50)


        panlabel = tk.Label(self,text="PAN",font=("Arial",18),bg="#1C2030",fg="white")
        panlabel.place(x=110,y=410,width=150,height=50)


        mobilelabel = tk.Label(self,text="Mobile",font=("Arial",18),bg="#1C2030",fg="white")
        mobilelabel.place(x=110,y=465,width=150,height=50)


        emaillabel = tk.Label(self,text="E-mail",font=("Arial",18),bg="#1C2030",fg="white")
        emaillabel.place(x=110,y=520,width=150,height=50)


        name1=db.execute("""Select * from users where id=?""",cur_id).fetchone()
        name1label = tk.Label(self,text=  str(name1[1]),font=("Arial",20),bg="#1C2030",fg="white",anchor="w")
        name1label.place(x=260,y=300,width=1000,height=50)


        print(cur_id)
        ucc1label = tk.Label(self,text= str(cur_id+100000),font=("Arial",18),bg="#1C2030",fg="white",anchor="w")
        ucc1label.place(x=260,y=355,width=1000,height=50)


        pan1=db.execute("""Select * from users where id=?""",cur_id).fetchone()
        pan1label = tk.Label(self,text= str(pan1[6]),font=("Arial",18),bg="#1C2030",fg="white",anchor="w")
        pan1label.place(x=260,y=410,width=1000,height=50)

        mob1=db.execute("""Select * from users where id=?""",cur_id).fetchone()
        mobile1label = tk.Label(self,text= str(mob1[3]),font=("Arial",18),bg="#1C2030",fg="white",anchor="w")
        mobile1label.place(x=260,y=465,width=1000,height=50)

        email1=db.execute("""Select * from users where id=?""",cur_id).fetchone()
        email1label = tk.Label(self,text= str(email1[2]),font=("Arial",18),bg="#1C2030",fg="white",anchor="w")
        email1label.place(x=260,y=520,width=1000,height=50)



        def popup1():


                def test(event):
                        global state
                        if state == 1:
                                winbtntest.config(image=winbtn0)
                                state = 0
                        else:
                                winbtntest.config(image=winbtn1)
                                state = 1

                def Close():
                        toplevel1.destroy()

                def check():
                    flag=0

                    pass1 = self.txtopass.get()
                    pass2 = self.txtnpass.get()
                    pass3 = self.txtcpass.get()


                    opass1 = db.execute("""SELECT * FROM users WHERE id = ?""", cur_id).fetchone()
                    print(type(opass1.hash1))
                    print( type(generate_password_hash(pass1)))




                    if not pass1 or not pass2 or not pass3:
                        messagebox.showerror(message = "Fields cannot be empty!!")
                        flag=1
                    elif pass2 != pass3:
                        messagebox.showerror(message = "Passwords Do not match!!")
                        flag=1
                    elif pass1 is None or not check_password_hash(opass1.hash1,pass1):
                        messagebox.showerror(message="Old password is incorrect")
                        flag=1

                    if flag==0:
                        pass1 = generate_password_hash(pass2)
                        db.execute("""update users set hash1=?""", pass1)
                    toplevel1.destroy()




                toplevel1 = tk.Toplevel()
                toplevel1.geometry("605x364+381+254")
                toplevel1.configure(bg="#131722")



                a1 = tk.Label(toplevel1,text ="Change Password",font=("Arial",20,"bold"),fg="#AFFAFF",bg="#131722",anchor="w")
                a1.place(x=150,y=20,width=300,height=30)


                self.txtopass = Placeholder(toplevel1,placeholder='  Old Password',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
                self.txtopass.place(x=92,y=70,width=350.99,height=52.91)

                self.txtnpass = Placeholder(toplevel1,placeholder='  New Password',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
                self.txtnpass.place(x=92,y=130,width=350.99,height=52.91)


                self.txtcpass = Placeholder(toplevel1,placeholder='  Confirm New Password',placeholdercolor='#4F5966',color='white',font=("Arial",20),bg="#2A2E39",relief='flat')
                self.txtcpass.place(x=92,y=190,width=350.99,height=52.91)



                btn2 = tk.Button(toplevel1,text="Change",font=("Arial",20,"bold"),fg="white",bg="#007BFF",command=check)
                btn2.place(x=200,y=290,width=150,height=50)



        changepbtn = tk.Button(self,text="Change Password",font=("Arial",12),fg="white",bg="#010000",borderwidth=0,command=popup1)
        changepbtn.place(x=137,y=650,width=300,height=60)


def popup4(self,parent,controller):

        def log_out():
            toplevel.destroy()
            controller.show_frame("Login_Window")


        def test(event):
                global state
                if state == 1:
                        winbtntest.config(image=winbtn0)
                        state = 0
                else:
                        winbtntest.config(image=winbtn1)
                        state = 1

        def Close():
                toplevel.destroy()



        toplevel = tk.Toplevel()
        toplevel.geometry("605x364+381+254")
        toplevel.configure(bg="#131722")



        a1 = tk.Label(toplevel,text ="Do you want to logout",font=("Arial",20),fg="white",bg="#131722",anchor="w")
        a1.place(x=150,y=100,width=300,height=30)


        btn1 = tk.Button(toplevel,text="Yes",font=("Arial",20,"bold"),fg="white",bg="#007BFF",command=log_out)
        btn1.place(x=150,y=200,width=100,height=50)


        btn2 = tk.Button(toplevel,text="No",font=("Arial",20,"bold"),fg="white",bg="#007BFF",command=Close)
        btn2.place(x=320,y=200,width=100,height=50)
        if len(symbol1) == 0:
            db.execute("""DELETE FROM Watchlist where user_id=?""",cur_id)
        else:
            for i in range(len(symbol1)):
                db.execute("""INSERT INTO Watchlist(user_id,stock,s_name) VALUES(?,?,?)""",cur_id,symbol1[i],name1[i] )

class Placeholder:
    def __init__(self,master,placeholder='',placeholdercolor='grey',color='black',**kwargs):
        self.e = tk.Entry(master,fg=placeholdercolor,**kwargs)
        self.e.bind('<FocusIn>',self.focus_in)
        self.e.bind('<FocusOut>',self.focus_out)
        self.e.insert(0, placeholder)
        self.placeholder = placeholder
        self.placeholdercolor=placeholdercolor
        self.color = color

    def pack(self,side=None,**kwargs):
        self.e.pack(side=side,**kwargs)

    def dell(self):
        self.e.delete(0,"end")

    def place(self,side=None,**kwargs):
        self.e.place(side=side,**kwargs)

    def get(self,**kwargs):
        return self.e.get()

    def grid(self,column=None,**kwargs):
        self.e.grid(column=column,**kwargs)

    def focus_in(self,e):
        if self.e.get() == self.placeholder:
            self.e.delete(0,'end')
        self.e.configure(fg=self.color)
        if "Password" in self.placeholder:
            self.e.configure(show="*")

    def focus_out(self,e):
        if self.e.get() == '':
            self.e.configure(fg=self.placeholdercolor)
            self.e.delete(0,'end')
            self.e.insert(0,self.placeholder)
            if "Password" in self.placeholder:
                self.e.configure(show="")

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()