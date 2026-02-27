from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
from tkinter import ttk
import tkinter as tk
import ast
from datetime import *

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

    #Open the user file for each itteration to allow it to be constantly updated

    with open ("Users_file.txt") as file:
    #While eval is considered unsafe, litteral eval is considered safer and reads the file from the last time accessed
        userdict = ast.literal_eval(file.read())
    #print(userdict)

    def login():
        global UserID
        UserCount = 0
        boolean = False
        email_got = email.get().casefold()
        password_got = password.get()
        if email_got == userdict[0]["email"].casefold() and password_got == userdict[0]["password"]:
            UserID = 0
            screen.destroy()
            admin_home_screen()   
        else:
            for i in userdict.items():
                if userdict[UserCount]["email"].casefold() == email_got and userdict[UserCount]["password"] == password_got:
                    boolean = True
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
    Heading = Label(text="Welcome Molly", bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack()

    def new_book():
        screen.destroy()
        add_book()

    def book_list():
        screen.destroy()
        loans()

    def back():
        screen.destroy()
        login_screen()

    
    new_button = Button(screen, text="Add New Book", command = new_book, font=(None,20),bg="light blue") #command=
    new_button.pack()
    view_button = Button(screen, text="View Book List", command = book_list, font=(None,20),bg="light blue") #command=
    view_button.pack()
    back_button = Button(screen, text="back", command = back, font=(None,20),bg="light blue") #command=
    back_button.pack()
    screen.mainloop()

def user_main_screen(): #Displays the main screen for non admin users that will be the centre for or other parts of the programme

    with open ("Users_file.txt") as file:
        userdict = ast.literal_eval(file.read())

    with open("Books_file.txt") as file:
        bookdict = ast.literal_eval(file.read())

    with open("Loans_file.txt") as file:
        loandict = ast.literal_eval(file.read())

    screen = tk.Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    Heading = Label(text="Welcome " + userdict[UserID]["name"],bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack()


    treeview = ttk.Treeview(columns=("author","due"))
    treeview.heading("#0", text="Title")
    treeview.heading("author", text="Author")
    treeview.heading("due", text="Due Date")

    def trees():

        with open ("Users_file.txt") as file:
            userdict = ast.literal_eval(file.read())

        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())

        with open("Loans_file.txt") as file:
            loandict = ast.literal_eval(file.read())

        treeview.delete(*treeview.get_children())
        
        LoanCount = 0
        for i in loandict:
            if loandict[LoanCount]["user"] == UserID and bookdict[loandict[LoanCount]["book"]]["loaned"] == True:
                treeview.insert("", tk.END, text=bookdict[loandict[LoanCount]["book"]]["title"], values=(bookdict[loandict[LoanCount]["book"]]["first name"]+" "+bookdict[loandict[LoanCount]["book"]]["last name"],loandict[LoanCount]["loan"])        )
            LoanCount = LoanCount + 1
            
    y_scrollbar = ttk.Scrollbar(screen, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = ttk.Scrollbar(screen, orient=tk.HORIZONTAL, command=treeview.xview)
    treeview.configure(xscrollcommand=x_scrollbar.set)

    y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    x_scrollbar.pack(side=tk.TOP, fill=tk.X)

    treeview.pack()
    
    def loan_list():
        screen.destroy()
        loans()

    def review_book():
        selected_item = treeview.focus()
        screen.destroy()
        review()

    def back():
        screen.destroy()
        login_screen()

    def check_in():

        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())

        selected_item = treeview.focus() # Get the ID of the selected item
        print(selected_item)
        if selected_item == "":
            messagebox.showerror("Error", "Nothing to return")
        else:
            item_index = treeview.index(selected_item)

            bookdict[item_index]["loaned"] = False

            with open ("Books_file.txt","w") as file:
                file.write(str(bookdict))
                file.close()
            messagebox.showinfo("Success", "You have returned " + bookdict[item_index]["title"])
        
            trees()

    
    loan_button = Button(screen, text="Loan", command = loan_list, bg="light blue") #command=
    loan_button.pack()
    review_button = Button(screen, text="Review", command = review_book, bg="light blue") #command=
    review_button.pack()
    return_button = Button(screen, text="Return", command = check_in, bg="light blue") #command=
    return_button.pack()
    back_button = Button(screen, text="Back", command = back ,bg="light blue") #command=
    back_button.pack()

    trees()

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

    #Open the user file for each itteration to allow it to be constantly updated

    with open ("Users_file.txt") as file:
    #While eval is considered unsafe, litteral eval is considered safer and reads the file from the last time accessed
        userdict = ast.literal_eval(file.read())
    #print(userdict)
    
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
        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())
        BookCount = 0
        boolean = False
        title_got = title.get().casefold()
        FN_got = authorFN.get().casefold()
        LN_got = authorLN.get().casefold()
        Cost_got = cost.get()
        for i in bookdict.items():
                if bookdict[BookCount]["title"] == title_got and bookdict[BookCount]["first name"] == FN_got and bookdict[BookCount]["last name"] == LN_got:
                    #this will check if the book already exists
                    boolean = True
                if not bookdict[BookCount]["title"] == "":
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

    def back():
        screen.destroy()
        admin_home_screen()

    Add_button = Button(screen, text="Add Book", command = add,font = (None,15),bg = "light blue")
    Add_button.place(x=40,y=350)
    #Button to bring the user back to the login page
    Back_button = Button(screen, text = "Back", command = back, font = (None,15),bg = "light blue") #command =
    Back_button.place(x=270,y=350)
    screen.mainloop()

#This makes loans

def loans():

    with open("Users_file.txt") as file:
        userdict = ast.literal_eval(file.read())

    screen = tk.Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    Heading = Label(text="List of Books",bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack() 

    treeview = ttk.Treeview(columns=("author","cost","loan"))
    treeview.heading("#0", text="Title")
    treeview.heading("author", text="Author")
    treeview.heading("cost", text="Cost")
    treeview.heading("loan", text="On Loan")   


    def trees():
        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())

        with open("Loans_file.txt") as file:
            loandict = ast.literal_eval(file.read())

        treeview.delete(*treeview.get_children())
        BookCount = 0
        for i in bookdict:
            treeview.insert("", tk.END, text=bookdict[BookCount]["title"], values=(bookdict[BookCount]["first name"]+" "+bookdict[BookCount]["last name"],"£"+str(bookdict[BookCount]["cost"]/100), bookdict[BookCount]["loaned"]))
            BookCount = BookCount + 1
            
    y_scrollbar = ttk.Scrollbar(screen, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = ttk.Scrollbar(screen, orient=tk.HORIZONTAL, command=treeview.xview)
    treeview.configure(xscrollcommand=x_scrollbar.set)

    y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    x_scrollbar.pack(side=tk.TOP, fill=tk.X)

    treeview.pack()

    def select_loan():

        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())

        with open("Loans_file.txt") as file:
            loandict = ast.literal_eval(file.read())

        selected_item = treeview.focus() # Get the ID of the selected item
        item_index = treeview.index(selected_item)
        
        loandays = timedelta(days = 20)

        today = date.today()
        loan = today + loandays

        if bookdict[item_index]["loaned"] == False:

            LoanCount = 0
            
            for i in loandict:
                LoanCount = LoanCount + 1

            loandict[LoanCount] = {
                    "user" : UserID,
                    "book" : item_index,
                    "current": str(today),
                    "loan" : str(loan)
                }
            with open ("Loans_file.txt","w") as file:
                file.write(str(loandict))
                file.close()
                
            bookdict[item_index]["loaned"] = True

            with open ("Books_file.txt","w") as file:
                file.write(str(bookdict))
                file.close()
            messagebox.showinfo("Success", "You have " + bookdict[item_index]["title"] + " for 20 days")

        else:
            messagebox.showerror("Unsuccessful","This book is aleady on loan")

        trees()

    def buy():
        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())
        selected_item = treeview.focus() # Get the ID of the selected item
        item_index = treeview.index(selected_item)
        if userdict[UserID]["admin?"] == False:
            buying = askyesno(title="Checking", message="Are you sure that you want to buy " + bookdict[item_index]["title"] + " for " + "£" + str(bookdict[item_index]["cost"]/100) + "?")
        else:
            deleting = askyesno(title="Checking", message="Are you sure that you want to delete " + bookdict[item_index]["title"] + "?")
        if buying:
            del bookdict[item_index]
            with open ("Books_file.txt","w") as file:
                file.write(str(bookdict))
            trees()


    def back():
        screen.destroy()
        if userdict[UserID]["admin?"] == True:
            admin_home_screen()
        else:
            user_main_screen()

    if userdict[UserID]["admin?"] == False:
        loan_button = Button(screen, text="Loan", command = select_loan, bg="light blue") #command=
        loan_button.pack()
    #The buy button won't collect any details of payment, its based on a trust system
    if userdict[UserID]["admin?"] == True:
        Delete_button = Button(screen, text="Delete", command = buy, bg="light blue")
        Delete_button.pack()
    else:
        buy_button = Button(screen, text="Buy", command = buy, bg="light blue") #command=
        buy_button.pack()
    back_button = Button(screen, text="Back", command = back, bg="light blue") #command=
    back_button.pack()

    trees()

def review():
    print(selcted_item)


#This opens to the login page, starting the programme

#TableFrame = tk.Frame(self)

#loans()

login_screen()

#add_book()

#user_main_screen()
