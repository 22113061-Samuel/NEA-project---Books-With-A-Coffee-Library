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
    screen.resizable(False,False)

    #generate headings for the inputs
    Heading = Label(text="Login",bg="light grey",width="25",height="2",font=(None,20))
    Heading.pack()
    Email = Label(screen, text="Email",font=(None,15))
    Email.place(x=0,y=80)
    Password = Label(screen, text="Password",font=(None,15))
    Password.place(x=0,y=160)

    #declair variables that I will be working with
    email = StringVar()
    password = StringVar()

    #generate entry buttons for users to input into
    Email_entry = Entry(textvariable = email, width = "30",font=(None,15))
    Email_entry.place(x=25,y=120)
    Password_entry = Entry(textvariable = password, width = "30",font=(None,15),show = "*")
    Password_entry.place(x=25,y=200)

    #Open the user file as this allows for the program to check against current profiles
    with open ("Users_file.txt") as file:
    #While eval is considered unsafe, litteral eval is considered safer and reads the file from the last time accessed
    #The data is saved as a dictionary to operate from
        userdict = ast.literal_eval(file.read())

    #this will try to log the user in
    def login():
        global UserID
        UserCount = 0
        boolean = False
        email_got = email.get().casefold()
        password_got = password.get()
        #This will first check if the user is the admin account
        if email_got == userdict[0]["email"].casefold() and password_got == userdict[0]["password"]:
            UserID = 0
            screen.destroy()
            admin_home_screen()   
        else:
            for i in userdict.items():
                #This will check each one of the entries in the customer dictionary
                if userdict[UserCount]["email"].casefold() == email_got and userdict[UserCount]["password"] == password_got:
                    boolean = True
                    UserID = UserCount
                UserCount = UserCount + 1
            #If the details given are not the same as stored, an error is outputted
            if boolean == False:
                messagebox.showerror("Error", "User does not exist")
            #This will happen if the login is successful
            else:
                screen.destroy()
                user_main_screen()

    #This takes the user to the customer create screen to create a new account
    def create():
        screen.destroy()
        create_screen()

    Login_button = Button(screen, text="Login", command=login,font=(None,20),bg="light blue")
    Login_button.place(x=40,y=275)
    Create_button = Button(screen, text="Create", command=create,font=(None,20),bg="light blue")
    Create_button.place(x=230,y=275)

    screen.mainloop()

#This will be used if the user inputs the admin account details
def admin_home_screen():

    #Initialises main screen screen
    screen = Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    Heading = Label(text="Welcome Molly", bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack()

    #This structuers a table to input loan details into
    treeview = ttk.Treeview(columns=("name","email","title","author","taken","due"))
    treeview.heading("#0", text="Loan ID")    
    treeview.heading("name", text="Name")
    treeview.heading("email", text="Email")
    treeview.heading("title", text="Title")
    treeview.heading("author", text="Author")
    treeview.heading("taken", text="Taken")
    treeview.heading("due", text="Due")

    #This opens all files that willl be neccesary to access
    with open ("Users_file.txt") as file:
        userdict = ast.literal_eval(file.read())

    with open("Books_file.txt") as file:
        bookdict = ast.literal_eval(file.read())

    with open("Loans_file.txt") as file:
        loandict = ast.literal_eval(file.read())

    #This shows the admin acount all the current loans
    LoanCount = 0
    temp_list = []
    for i in loandict:
        if bookdict[loandict[LoanCount]["book"]]["loaned"] == True and loandict[LoanCount]["book"] not in temp_list:
            temp_list.append(loandict[LoanCount]["book"])
        LoanCount = LoanCount + 1
    for i in range(LoanCount):
        LoanCount = LoanCount - 1
        if loandict[LoanCount]["book"] in temp_list:
            treeview.insert("", tk.END, text=LoanCount, values=(userdict[loandict[LoanCount]["user"]]["name"],userdict[loandict[LoanCount]["user"]]["email"],bookdict[loandict[LoanCount]["book"]]["title"],bookdict[loandict[LoanCount]["book"]]["first name"]+" "+bookdict[loandict[LoanCount]["book"]]["last name"],loandict[LoanCount]["current"],loandict[LoanCount]["loan"]))
            temp_list.remove(loandict[LoanCount]["book"])


    #While I did not impliment a search, this allows you to scroll through the entries       
    y_scrollbar = ttk.Scrollbar(screen, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = ttk.Scrollbar(screen, orient=tk.HORIZONTAL, command=treeview.xview)
    treeview.configure(xscrollcommand=x_scrollbar.set)

    y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    x_scrollbar.pack(side=tk.TOP, fill=tk.X)

    treeview.pack()

    #This function takes the admin to a page to add a new book to the system
    def new_book():
        screen.destroy()
        add_book()

    #This function takes the admin to the same page as the users to see all the books
    def book_list():
        screen.destroy()
        loans()

    #This logs the user out of the system
    def back():
        screen.destroy()
        login_screen()

    
    new_button = Button(screen, text="Add Book", command = new_book, font=(None,15),bg="light blue") 
    new_button.place(x=20,y=330)
    view_button = Button(screen, text="View Books", command = book_list, font=(None,15),bg="light blue") 
    view_button.place(x=140,y=330)
    back_button = Button(screen, text="Back", command = back, font=(None,15),bg="light blue") 
    back_button.place(x=280,y=330)
    screen.mainloop()

#Displays the main screen for non admin users that will be the centre for or other parts of the program
def user_main_screen():

    with open ("Users_file.txt") as file:
        userdict = ast.literal_eval(file.read())

    #Initialises the screen
    screen = tk.Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    screen.resizable(False,False)
    #Welcomes the user with their name
    Heading = Label(text="Welcome " + userdict[UserID]["name"],bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack()

    #Creates a table to show the user's current loans
    treeview = ttk.Treeview(columns=("title","author","due"))
    treeview.heading("#0", text="Book ID")
    treeview.heading("author", text="Author")
    treeview.heading("title", text="Title")
    treeview.heading("due", text="Due Date")

    #Shows any loans and updates it when any of the status will change
    def trees():
        #Opens all relevant files that are being worked on

        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())

        with open("Loans_file.txt") as file:
            loandict = ast.literal_eval(file.read())

        treeview.delete(*treeview.get_children())        
        LoanCount = 0
        temp_list = []
        for i in loandict:
            if loandict[LoanCount]["user"] == UserID and bookdict[loandict[LoanCount]["book"]]["loaned"] == True and loandict[LoanCount]["book"] not in temp_list:
                temp_list.append(loandict[LoanCount]["book"])
            LoanCount = LoanCount + 1
        #Displays the loans from most recent to last on that is due
        for i in range(LoanCount):
            LoanCount = LoanCount - 1
            if loandict[LoanCount]["book"] in temp_list:
                treeview.insert("", tk.END, text=loandict[LoanCount]["book"], values=(bookdict[loandict[LoanCount]["book"]]["title"],bookdict[loandict[LoanCount]["book"]]["first name"]+" "+bookdict[loandict[LoanCount]["book"]]["last name"],loandict[LoanCount]["loan"]))
                temp_list.remove(loandict[LoanCount]["book"])


    #I used a scrollbar so that users could scroll instead of a search function  
    y_scrollbar = ttk.Scrollbar(screen, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = ttk.Scrollbar(screen, orient=tk.HORIZONTAL, command=treeview.xview)
    treeview.configure(xscrollcommand=x_scrollbar.set)

    y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    x_scrollbar.pack(side=tk.TOP, fill=tk.X)

    treeview.pack()

    #This command brings the user to the list of library books
    def loan_list():
        screen.destroy()
        loans()

    #This command will allow a user to review a book as long as they current have it on loan
    def review_book():
        selected_item = treeview.focus()
        #Returns an error if nothing is present
        if selected_item == "":
            #Shows an error in another pop up window
            messagebox.showerror("Error", "Nothing to review")
        else:
            item_index = treeview.item(selected_item,"text")
            screen.destroy()
            #This takes the user to another page to reviw the book
            review(item_index)

    #This logs the user out
    def back():
        screen.destroy()
        login_screen()

    #This is the command to return a book
    def check_in():

        #This will re-open the book file to make sure that it does not try and return a book multiple times
        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())

        selected_item = treeview.focus()
        item_index = treeview.item(selected_item,"text") 

        #If nothing is selected then an error
        if selected_item == "":
            messagebox.showerror("Error", "Nothing to return")
        else:
            #This saves the book as not on loan so others can loan it
            bookdict[item_index]["loaned"] = False
            with open ("Books_file.txt","w") as file:
                file.write(str(bookdict))
                file.close()
            #Displays that the book was returned
            messagebox.showinfo("Success", "You have returned " + bookdict[item_index]["title"])
        
            trees()

    
    loan_button = Button(screen, text="Loan", command = loan_list, font = (None,15), bg="light blue")
    loan_button.place(x=20,y=330)
    review_button = Button(screen, text="Review", command = review_book, font = (None,15), bg="light blue")
    review_button.place(x=120,y=330)
    return_button = Button(screen, text="Return", command = check_in, font = (None,15), bg="light blue")
    return_button.place(x=220,y=330)
    back_button = Button(screen, text="Back", command = back, font = (None,15), bg="light blue")
    back_button.place(x=320,y=330)

    trees()

    screen.mainloop()

#Creates a new acount without admin privilages
def create_screen():

    #Initialise screen, creating all the headings telling people where to input data
    screen = Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    screen.resizable(False,False)
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

    #Initialising local variables
    
    name = StringVar()
    email = StringVar()
    password = StringVar()
    newpass = StringVar()

    #Creates entry points for data to be added
    Name_entry = Entry(textvariable = name, width = "38",font=(None,12))
    Name_entry.place(x=25,y=105)
    Email_entry = Entry(textvariable = email, width = "38",font=(None,12))
    Email_entry.place(x=25,y=170)
    Password_entry = Entry(textvariable = password, width = "38",font=(None,12), show = "*")
    Password_entry.place(x=25,y=235)
    Verify_Password_entry = Entry(textvariable = newpass, width = "38",font=(None,12),show = "*")
    Verify_Password_entry.place(x=25,y=300)

    #Open the user file to verify that the user does not already exist
    with open ("Users_file.txt") as file:
    #While eval is considered unsafe, litteral eval is considered safer and reads the file from the last time accessed
        userdict = ast.literal_eval(file.read())
    
    def newuser():
        UserCount = 0
        namer = name.get()
        emailer = email.get()
        passer = password.get()
        newpasser = newpass.get()
        boolean = True
        
        if not passer == "" and not namer == "" and not emailer == "" and passer == newpasser and "@" in emailer and "." in emailer:
            #Read from file
            for i in userdict.items():
                if userdict[UserCount]["email"].casefold() == emailer.casefold():
                    boolean = False
                UserCount = UserCount + 1
            #If the user does not already exist in the file, a new ID is created and saved
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
            #An error is given if the user does alredy exist
            else:
                messagebox.showerror("Error", "User already exists by this email")    
        #If any of the boxes are not filled in or the email adress does not have a "." and "@" the it will produce an error
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

    #Initialises screen

    screen = Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    screen.resizable(False,False)
    
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
                BookCount = BookCount + 1
        #If the book already exists an error is given
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
            #The book is then saved to a new ID
            with open ("Books_file.txt","w") as file:
                file.write(str(bookdict))
            messagebox.showinfo("Saved","Book added to system")
        else:
            messagebox.showerror("Error","please check the fields")
    
    #Button to bring the user back to the login page
    def back():
        screen.destroy()
        admin_home_screen()

    Add_button = Button(screen, text="Add Book", command = add,font = (None,15),bg = "light blue")
    Add_button.place(x=40,y=350)

    Back_button = Button(screen, text = "Back", command = back, font = (None,15),bg = "light blue") #command =
    Back_button.place(x=270,y=350)
    screen.mainloop()

#This page displays the books availalbe for taking on loan and puchasing
def loans():

    with open("Users_file.txt") as file:
        userdict = ast.literal_eval(file.read())

    #Intialises screen
    screen = tk.Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    screen.resizable(False,False)
    Heading = Label(text="List of Books",bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack() 

    treeview = ttk.Treeview(columns=("title","author","cost","loan"))
    treeview.heading("#0", text="Book ID")
    treeview.heading("title", text="Title")
    treeview.heading("author", text="Author")
    treeview.heading("cost", text="Cost")
    treeview.heading("loan", text="On Loan")

    #Trees is the function that displays all the books available
    def trees():
        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())

        with open("Loans_file.txt") as file:
            loandict = ast.literal_eval(file.read())

        treeview.delete(*treeview.get_children())
        BookCount = 0
        for i in bookdict:
            if not bookdict[BookCount]["title"] == "":
                treeview.insert("", tk.END, text=BookCount, values=(bookdict[BookCount]["title"],bookdict[BookCount]["first name"]+" "+bookdict[BookCount]["last name"],"£"+str(bookdict[BookCount]["cost"]/100), bookdict[BookCount]["loaned"]))
            BookCount = BookCount + 1

    #While I did not impliment a search, this allows you to scroll through the entries       
    y_scrollbar = ttk.Scrollbar(screen, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = ttk.Scrollbar(screen, orient=tk.HORIZONTAL, command=treeview.xview)
    treeview.configure(xscrollcommand=x_scrollbar.set)

    y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    x_scrollbar.pack(side=tk.TOP, fill=tk.X)

    treeview.pack()

    #This function creates a loan for twenty days time
    def select_loan():

        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())

        with open("Loans_file.txt") as file:
            loandict = ast.literal_eval(file.read())

        selected_item = treeview.focus()
        #An error is given if nothing is selected
        if selected_item == "":
            messagebox.showerror("Error", "Nothing to review")
        else:
            item_index = treeview.item(selected_item,"text")
        
            loandays = timedelta(days = 20)

            #This gets the current date
            today = date.today()
            #This finds that date that it due back
            loan = today + loandays

            #This checks to see if the book is already on loan and cannot be taken out
            if bookdict[item_index]["loaned"] == False:

                #This creats a new ID for the next loan
                LoanCount = 0            
                for i in loandict:
                    LoanCount = LoanCount + 1

                loandict[LoanCount] = {
                    "user" : UserID,
                    "book" : item_index,
                    "current": str(today),
                    "loan" : str(loan)
                }

                #This documents the book that is on loan
                with open ("Loans_file.txt","w") as file:
                    file.write(str(loandict))
                    file.close()
                    
                #The book is then saved as being on loan
                bookdict[item_index]["loaned"] = True
                with open ("Books_file.txt","w") as file:
                    file.write(str(bookdict))
                    file.close()
                messagebox.showinfo("Success", "You have " + bookdict[item_index]["title"] + " for 20 days")
            #This produces an error if the book is already on loan
            else:
                messagebox.showerror("Unsuccessful","This book is aleady on loan")
        #The table is then reloaded to insure that all data is up-to-date
        trees()

    #While it says buy, this command is used to delete a book from the dictionary
    def buy():
        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())
        selected_item = treeview.focus()
        #This gives an error if nothing is selected
        if selected_item == "":
            messagebox.showerror("Error", "Nothing to review")
        else:
            item_index = treeview.item(selected_item,"text")
            #Different messages are given but they will both end up deleting an entry if yes is pressed
            if userdict[UserID]["admin?"] == False:
                #A yes or no pop up will be issued, deleting the book if yes but just closing itself if no is pressed
                buying = askyesno(title="Checking", message="Are you sure that you want to buy " + bookdict[item_index]["title"] + " for " + "£" + str(bookdict[item_index]["cost"]/100) + "?")
            else:
                #A yes or no pop up will be issued, deleting the book if yes but just closing itself if no is pressed
                buying = askyesno(title="Checking", message="Are you sure that you want to delete " + bookdict[item_index]["title"] + "?")
            #This removes the book from the dictionary by making all fields blank but it keeps the unique ID so books don't get assinged the wrong value
            if buying:
                bookdict[item_index]["title"] = ""
                bookdict[item_index]["first name"] = ""
                bookdict[item_index]["last name"] = ""
                bookdict[item_index]["cost"] = ""
                bookdict[item_index]["loaned"] = ""
                with open ("Books_file.txt","w") as file:
                    file.write(str(bookdict))
                trees()

    #This function allows users to go to page to look at reviews for a book
    def reviews():
        with open("Books_file.txt") as file:
            bookdict = ast.literal_eval(file.read())
        selected_item = treeview.focus()
        item_index = treeview.item(selected_item,"text")
        #If nothing is selected, an error is outputted
        if selected_item == "":
            messagebox.showerror("Error", "Nothing to view")
        #If a book is selected, it will take the user to the page for those reviews
        else:
            screen.destroy()
            view_reviews(item_index)

    #This takes the user back to their home screen
    def back():
        screen.destroy()
        #If the user is on the admin acount they are taken to the admin home screen
        if userdict[UserID]["admin?"] == True:
            admin_home_screen()
        #If the user is not an admin then they are taken back to the user main screen
        else:
            user_main_screen()

    #A loan button is displayed if the user is not an admin
    if userdict[UserID]["admin?"] == False:
        loan_button = Button(screen, text="Loan", command = select_loan, font = (None,15), bg="light blue")
        loan_button.place(x=20,y=330)
    #A different button is shown if the user is an admin but they have essentialy the same function
    if userdict[UserID]["admin?"] == True:
        Delete_button = Button(screen, text="Delete", command = buy, font = (None,15), bg="light blue")
        Delete_button.place(x=20,y=330)
    else:
        #The buy button won't collect any details of payment, its based on a trust system
        buy_button = Button(screen, text="Buy", command = buy, font = (None,15), bg="light blue")
        buy_button.place(x=95,y=330)
    view_button = Button(screen, text="View Reviews", command = reviews, font = (None,15), bg="light blue")
    if userdict[UserID]["admin?"] == True:
        view_button.place(x=130,y=330)
    else:
        view_button.place(x=160,y=330)
    back_button = Button(screen, text="Back", command = back,font = (None,15), bg="light blue")
    if userdict[UserID]["admin?"] == True:
        back_button.place(x=300,y=330)
    else:
        back_button.place(x=320,y=330)
    trees()

#This is the page that allows for users to create reviews
def review(item_index):

    with open("Books_file.txt") as file:
        bookdict = ast.literal_eval(file.read())

    with open ("Users_file.txt") as file:
        userdict = ast.literal_eval(file.read())

    #Initialises the screen
    screen = tk.Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    screen.resizable(False,False)
    Heading = Label(text="Reviewing Book",bg="light grey",width="25",height="2",font=(None,20)) #Hello user? #+ name
    Heading.pack()

    name = StringVar()
    title = StringVar()
    review = StringVar()

    Reviewing = Label(screen, text="Reviewing: " + bookdict[item_index]["title"],font=(None,15))
    Reviewing.place(x=0,y=80)

    Name = Label(screen, text="Name:",font=(None,15))
    Name.place(x=0,y=110)
    Name_entry = Entry(textvariable = name, width = "25",font=(None,15))
    Name_entry.place(x=75,y=110)

    Title = Label(screen, text="Review Title:",font=(None,15))
    Title.place(x=0,y=140)
    Title_entry = Entry(textvariable = title, width = "20",font=(None,15))
    Title_entry.place(x=125,y=140)

    Title = Label(screen, text="Review:",font=(None,15))
    Title.place(x=0,y=170)
    Review_entry = Entry(textvariable = review, width = "54", font=(None,10))
    Review_entry.place(x=10,y=200)

    #This function will check and then allow the review if it is applicable.
    def publish():
        with open ("Reviews_file.txt") as file:
            reviewdict = ast.literal_eval(file.read())
        name_got = name.get()
        title_got = title.get()
        review_got = review.get()
        #This checks to see if any of the tables are blank and gives an error if they are
        if review_got == "" or title_got == "" or name == "":
            messagebox.showerror("Unsuccessful","One of the fields are not filled in")
        else:
            ReviewCount = 0
            #This creates a new review ID
            for i in reviewdict:
                ReviewCount = ReviewCount + 1
            reviewdict[ReviewCount] = {
                "user" : UserID,
                "name" : name_got,
                "book" : item_index,
                "title": title_got,
                "review" : review_got
            }

        with open("Reviews_file.txt","w") as file:
            file.write(str(reviewdict))

    #This takes the non admin user back to the main user screen
    def back():
        screen.destroy()
        user_main_screen()

    publish_button = Button(screen, text="Publish", command = publish, font = (None,20), bg="light blue") 
    publish_button.place(x=40,y=275)
    back_button = Button(screen, text="Back", command = back, font = (None,20), bg="light blue") 
    back_button.place(x=230,y=275)

#This views the reviews given of the book that was selected
def view_reviews(item_index):

    screen = tk.Tk()
    screen.title("Books with a Coffee Library")
    screen.geometry("400x400")
    screen.resizable(False,False)
    Heading = Label(text="Displating User Reviews",bg="light grey",width="25",height="2",font=(None,20))
    Heading.pack() 

    with open("Users_file.txt") as file:
         userdict = ast.literal_eval(file.read())
         
    with open("Books_file.txt") as file:
         bookdict = ast.literal_eval(file.read())

    treeview = ttk.Treeview(columns=("name","title"))
    treeview.heading("#0", text="Review")
    treeview.heading("name", text="Name")
    treeview.heading("title", text="Review Title")

    #This allows for any updates to the reviews, namely if they are deleted the table will refresh
    def trees():
        with open("Reviews_file.txt") as file:
            reviewdict = ast.literal_eval(file.read())
        treeview.delete(*treeview.get_children())
        ReviewCount = 0
        #This displays all reviews of this book
        for i in reviewdict:
            if reviewdict[ReviewCount]["book"] == item_index:
                treeview.insert("", tk.END, text=ReviewCount, values=(reviewdict[ReviewCount]["name"],reviewdict[ReviewCount]["title"]))
            ReviewCount = ReviewCount + 1
            
    y_scrollbar = ttk.Scrollbar(screen, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = ttk.Scrollbar(screen, orient=tk.HORIZONTAL, command=treeview.xview)
    treeview.configure(xscrollcommand=x_scrollbar.set)

    y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    x_scrollbar.pack(side=tk.TOP, fill=tk.X)

    treeview.pack()

    #This will display a review that is chosen
    
    def look():
        with open("Reviews_file.txt") as file:
            reveiwdict = ast.literal_eval(file.read())
        selected_item = treeview.focus()
        item_index = treeview.item(selected_item,"text") # Get the ID of the selected item
        #If nothing is selected then it will reutrn an error
        if selected_item == "":
            messagebox.showerror("Error", "Nothing to return")
        #This will output the title of the review and the review itself in a pop up window
        else:
            messagebox.showinfo(reviewdict[item_index]["title"], reviewdict[item_index]["review"])

    #This is only allowed be used by admin
    #This effictively deltes any review that the staff deems inopropriate
    def delete():
        with open("Reviews_file.txt") as file:
            reviewdict = ast.literal_eval(file.read())
        selected_item = treeview.focus()
        #If nothing is selected then an error will be displayed
        if selected_item == "":
            messagebox.showerror("Error", "Nothing selected")
        else:
            item_index = treeview.item(selected_item,"text")
            #A yes and no prompt is issued and will check that the admin wants to delete the review
            deleting = askyesno(title="Checking", message="Are you sure that you want to delete this review?")
            if deleting: 
                reveiwdict[item_index]["user"] = ""
                reveiwdict[item_index]["name"] = ""
                reveiwdict[item_index]["book"] = ""
                reveiwdict[item_index]["title"] = ""
                reveiwdict[item_index]["review"] = ""
                #This is saved into the review file to make sure that it is up to date
                with open ("Reviews_file.txt","w") as file:
                    file.write(str(reveiwdict))
                trees()

    #This takes the user back to the list of books available for loan
    def back():
        screen.destroy()
        loans()

    trees()

    look_button = Button(screen, text="View", command = look, font = (None,20), bg="light blue") 
    look_button.place(x=40,y=330)
    #This will only show if the user is an admin
    if userdict[UserID]["admin?"] == True:
        delete_button = Button(screen, text="Delete", command = delete, font = (None,20), bg="light blue") 
        delete_button.place(x=140,y=330)
    back_button = Button(screen, text="Back", command = back, font = (None,20), bg="light blue") 
    back_button.place(x=260,y=330)

#This opens to the login page, starting the program
login_screen()
