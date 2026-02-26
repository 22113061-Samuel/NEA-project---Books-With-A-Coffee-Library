from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import ast
from datetime import *

#loandict = {}

#loandict[0] = {
#                    "user" : 0,
 #                   "book" : 0,
 #                   "current": "26/02/2026",
  #                  "loan" : "27/02/2026"
   #             }

#with open ("Loans_file.txt","w") as file:
    #file.write(str(loandict))

with open ("Users_file.txt") as file:
    #While eval is considered unsafe, litteral eval is considered safer and reads the file from the last time accessed
    userdict = ast.literal_eval(file.read())
print(userdict)
    
with open("Books_file.txt") as file:
    bookdict = ast.literal_eval(file.read())
print(bookdict)

with open("Loans_file.txt") as file:
    loandict = ast.literal_eval(file.read())
print(loandict)

    #This is the screen that takes us to the loging menu, then we can either login or create a new acount

def login_screen():

    #initialise screen
    
    screen = Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")

    Heading = Label(text="Login",bg="light grey",width="25",height="2",font=(None,20))
    Heading.pack()
    Email = Label(screen, text="Email",font=(None,15))
    Email.place(x=0,y=80)
    Password = Label(screen, text="Password",font=(None,15))
    Password.place(x=0,y=160)

    email = StringVar()
    password = StringVar()

    Email_entry = Entry(textvariable = email, width = "30",font=(None,15))
    Email_entry.place(x=25,y=120)
    Password_entry = Entry(textvariable = password, width = "30",font=(None,15),show = "*")
    Password_entry.place(x=25,y=200)

    def login():
        UserCount = 0
        boolean = False
        email_got = email.get()
        password_got = password.get()
        if email_got == userdict[0]["email"] and password_got == userdict[0]["password"]:
            screen.destroy()
            admin_home_screen()   
        else:
            for i in userdict.items():
                if userdict[UserCount]["email"].casefold() == email_got.casefold() and userdict[UserCount]["password"] == password_got:
                    boolean = True
                    global UserID
                    UserID = UserCount
                UserCount = UserCount + 1
            if boolean == False:
                messagebox.showerror("Error", "User does not exist")
            else:
                screen.destroy()
                user_main_screen()

    def create():
        screen.destroy()
        create_screen()

    Login_button = Button(screen, text="Login", command=login,font=(None,20),bg="light blue")
    Login_button.place(x=40,y=275)
    Create_button = Button(screen, text="Create", command=create,font=(None,20),bg="light blue")
    Create_button.place(x=230,y=275)

    screen.mainloop()

    #main

def admin_home_screen(): #Screen in use for the admin acount

    #initialise main screen screen
    
    screen = Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    Heading = Label(text="Welcome "+userdict[0]["name"],bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack()
    button = Button(screen, text="Login",font=(None,20),bg="light blue") #command=
    button.place(x=40,y=275)
    screen.mainloop()

def user_main_screen(): #Displays the main screen for non admin users that will be the centre for or other parts of the programme

    screen = Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    Heading = Label(text="Welcome " + userdict[UserID]["name"],bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack()
    treeview = ttk.Treeview(columns=("first name","last name","cost","status"))
    treeview.heading("#0", text="loandict[][]")
    treeview.heading("first name", text="loandict[][]")
    treeview.heading("last name", text="loandict[][]")
    treeview.heading("cost", text="loandict[][]")
    treeview.heading("status", text="loandict[][]")    
    treeview.insert(
        "",
        Tk.END,
        text="loandict",
        values=("i","I","i","I")        
    )
    treeview.pack()
    button = Button(screen, text="Login",font=(None,20),bg="light blue") #command=
    button.place(x=40,y=275)
    screen.mainloop()

def create_screen(): #creates a new acount without admin privilages

    #initialise screen

    screen = Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    Heading = Label(text="New User",bg="light grey",width="25",height="2",font=(None,20))
    Heading.pack()
    Name = Label(screen, text="Name",font=(None,12))
    Name.place(x=0,y=75)
    Email = Label(screen, text="Email",font=(None,12))
    Email.place(x=0,y=140)
    Password = Label(screen, text="Password",font=(None,12))
    Password.place(x=0,y=205)
    Verify_Password = Label(screen, text="Verify Password",font=(None,12))
    Verify_Password.place(x=0,y=270)

    #initialising local variables
    
    name = StringVar()
    email = StringVar()
    password = StringVar()
    newpass = StringVar()

    Name_entry = Entry(textvariable = name, width = "38",font=(None,12))
    Name_entry.place(x=25,y=105)
    Email_entry = Entry(textvariable = email, width = "38",font=(None,12))
    Email_entry.place(x=25,y=170)
    Password_entry = Entry(textvariable = password, width = "38",font=(None,12), show = "*")
    Password_entry.place(x=25,y=235)
    Verify_Password_entry = Entry(textvariable = newpass, width = "38",font=(None,12),show = "*")
    Verify_Password_entry.place(x=25,y=300)

    #This is a form of verification
    
    def newuser():
        UserCount = 0
        namer = name.get()
        emailer = email.get()
        passer = password.get()
        newpasser = newpass.get()
        boolean = True
        
        if not passer == "" and not namer == "" and not emailer == "" and passer == newpasser and "@" in emailer:
            #read from file
            #https://www.w3schools.com/python/python_dictionaries_nested.asp
            for i in userdict.items():
                if userdict[UserCount]["email"].casefold() == emailer.casefold():
                    boolean = False
                UserCount = UserCount + 1
            if boolean == True:
                userdict[UserCount] = {
                    "name" : namer,
                    "email" : emailer,
                    "password": passer,
                    "admin?" : False
                }
                global UserID
                UserID = UserCount
                with open ("Users_file.txt","w") as file:
                    file.write(str(userdict))
                screen.destroy()
                user_main_screen()
            else:
                messagebox.showerror("Error", "User already exists by this email")
        #elif userdict[][]:
            
        else:   
            messagebox.showerror("Error", "Please check that all your boxes are filled in and passwords is the same both times that it is entered")

    #This is the command for the button to bring the user back to the login page

    def back():
        screen.destroy()
        login_screen()

    Login_button = Button(screen, text="Create", command=newuser,font=(None,15),bg="light blue")
    Login_button.place(x=40,y=350)

    Back_button = Button(screen, text="Back", command=back,font=(None,15),bg="light blue")
    Back_button.place(x=270,y=350)
    screen.mainloop()

    #This allows an admin to add a new book to the system

def add_book():

    #initialise screen

    screen = Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    
    Heading = Label(text="New Book",bg="light grey",width="25",height="2",font=(None,20))
    Heading.pack()
    Title = Label(screen, text="Book Title",font=(None,15))
    Title.place(x=0,y=75)
    AuthorFN = Label(screen, text="Author (First name)",font=(None,15))
    AuthorFN.place(x=0,y=140)
    AuthorLN = Label(screen, text="Author (Last name)",font=(None,15))
    AuthorLN.place(x=0,y=205)
    Cost = Label(screen, text="Cost (In pence)",font=(None,15))
    Cost.place(x=0,y=270)

    #initialising local variables

    title = StringVar()
    authorFN = StringVar()
    authorLN = StringVar()
    cost = IntVar()

    Title_entry = Entry(textvariable = title, width = "38",font=(None,12))
    Title_entry.place(x=25,y=105)
    AuthorFN_entry = Entry(textvariable = authorFN, width = "38",font=(None,12))
    AuthorFN_entry.place(x=25,y=170)
    AuthorLN_entry = Entry(textvariable = authorLN, width = "38",font=(None,12))
    AuthorLN_entry.place(x=25,y=235)
    Cost_entry = Entry(textvariable = cost, width = "38",font=(None,12))
    Cost_entry.place(x=25,y=300)


    #This command adds a book to the system if all the fields are valid

    def add():
        BookCount = 0
        boolean = False
        title_got = title.get()
        FN_got = authorFN.get()
        LN_got = authorLN.get()
        Cost_got = cost.get()
        for i in bookdict.items():
                if bookdict[BookCount]["title"] == title_got and bookdict[BookCount]["first name"] == FN_got and bookdict[BookCount]["last name"] == LN_got:
                    boolean = True
                BookCount = BookCount + 1
        if boolean == True:
            messagebox.showerror("Error","This book already exists")
        elif not title_got == "" and not FN_got == "" and not LN_got == "" and not Cost_got == 0:
            bookdict[BookCount] = {
                "title" : title_got,
                "first name" : FN_got,
                "last name": LN_got,
                "cost" : Cost_got,
                "loaned" : False
            }
            with open ("Books_file.txt","w") as file:
                file.write(str(bookdict))
            messagebox.showinfo("Saved","Book added to system")
        else:
            messagebox.showerror("Error","please check the fields")

    Add_button = Button(screen, text="Add Book", command = add,font = (None,15),bg = "light blue")
    Add_button.place(x=40,y=350)
    #Button to bring the user back to the login page
    Back_button = Button(screen, text = "Back", font = (None,15),bg = "light blue") #command =
    Back_button.place(x=270,y=350)
    screen.mainloop()

#This makes loans

def loans():

    loandays = timedelta(days = 20)

    today = date.today()
    loan = today + loandays

    print(tomorrow)

    loandict[LoanCount] = {
                    "user" : userdict,
                    "book" : bookdict,
                    "current": today,
                    "loan" : loan
                }
    

#This opens to the login page, starting the programme

#TableFrame = tk.Frame(self)

login_screen()

#add_book()

#user_main_screen()
