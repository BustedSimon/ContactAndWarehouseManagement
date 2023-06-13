#IMPORTS----------------------------------------------------------------------------------------#
import tkinter as tk # FOR GUI
from tkinter import ttk # FOR DATA TABLE
from tkinter import messagebox # FOR ERROR BOX WHEN LOGIN FAILS
from tkinter import simpledialog # FOR FIRST-TIME LOGIN

import sqlite3 # FOR DATABASE

import base64 # FOR EN-/DECODING

import datetime as dt # FOR COMPARING DATES

from dataTable import Table # OWN MODULE FOR CREATING DATA FRAME / TABLE
from header import Header # OWN MODULE FOR DISPLAYING THE HEADER

import logging # LOGGING ERRORS AND INFOS

import sys # TO EXIT PROGRAM

#ENCODING---------------------------------------------------------------------------------------#
def encode(plainPassword): # encrypts password
    plainBytes = plainPassword.encode("ascii")
    encodedBytes = base64.b64encode(plainBytes)
    encodedPassword = encodedBytes.decode("ascii")
    return encodedPassword

def decode(encodedPassword): # decrypts password
    decodedBytes = encodedPassword.encode("ascii")
    plainBytes = base64.b64decode(decodedBytes)
    decodedPassword = plainBytes.decode("ascii")
    return decodedPassword

#LOGIN------------------------------------------------------------------------------------------#
def validateLogin(): # checks login details
    username = usernameEntry.get()
    encodedPassword = encode(passwordEntry.get())

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM accounts WHERE password=? AND username=?", (encodedPassword, username))

    check = cursor.fetchone()

    if check is not None: # successful login (PW/Username right)
        welcomeLabel = tk.Label(master=numbersFrame, bg="#3B5498", fg="white", font=30, text="Welcome, " + username + "!", justify="center")
        welcomeLabel.place(x=580, y=30, anchor="center")

        mainWindow.deiconify()
        loginWindow.destroy()
        logger.info("Login as '" +  username + "' succeeded.")
    else: # test if username exsists
        cursor.execute("SELECT * FROM accounts WHERE password IS NULL AND username=?", (username,))
        checkUser = cursor.fetchone()

        if checkUser is None: # if not: error
            tk.messagebox.showerror(title="Login failed", message="The username or password you entered is incorrect.")
            logger.warning("Login as '" + username + "' failed: username or password is incorrect")
        else: # if there's a username without passsword
            try:
                newPassword = simpledialog.askstring(title="Sign up", prompt="Set your password:")
                cursor.execute("UPDATE accounts SET password=? WHERE username=? ", (encode(newPassword), username))

                welcomeLabel = tk.Label(master=numbersFrame, bg="#3B5498", fg="white", font=30,text="Welcome, " + username + "!", justify="center")
                welcomeLabel.place(x=580, y=30, anchor="center")

                logger.info("Password of new user '" + username + "' was set successfully!")
            except Exception as e: # in case of None as password
                logger.info("Sign up of new user '" + username + "' failed: " + str(e))

    connection.commit()
    connection.close()

def cancelLogin(): # if cancel button is pressed: program closes
    loginWindow.destroy()
    mainWindow.destroy()
    logger.info("Login was cancelled: program is closing")
    sys.exit()

#VISUALISATION----------------------------------------------------------------------------------#
def drawGraph(): # draws graph that visualizes the amount of customer contacts in the contacts data table
    global xPos
    global yPos
    global coordinates

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers")
    allCustomers = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    for customer in range(allCustomers): # allCustomers = number of entries
        xPos += 5
        yPos -= 2
        coordinates.append(xPos) # adds positions to list
        coordinates.append(yPos)

    graphLeft.create_line(coordinates, fill="#F4B800", width=2) # draws positions

def compareNumbers(): # shows comparison of customer numbers in dashboard (in comparison to the day before)
    try:
        memory = open("numbers.txt", "r") # numbers stored in txt file, which is opened here
        oldNumbers = memory.readline()
        oldDate = memory.readline()
        memory.close()

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        allCustomers = cursor.execute("SELECT * FROM customers")
        newNumbers = str(len(list(allCustomers)))

        connection.commit() # connection needs to be closed after every access, because the database is also being accessed by the dataTable module
        connection.close()

        difference = int(newNumbers) - int(oldNumbers)

        if newNumbers == oldNumbers:
            textNumbers = "Zahl der Kunden ist im Vergleich zum Vortag gleich geblieben um:\n" + str(newNumbers)
        else:
            if newNumbers > oldNumbers:
                textNumbers = "Zahl der Kunden ist im Vergleich zum Vortag gestiegen um:\n+ " + str(difference)
            else:
                textNumbers = "Zahl der Kunden ist im Vergleich zum Vortag gesunken um:\n " + str(difference)

        comparisonLabel = tk.Label(master=numbersFrame, text=textNumbers, bg="#3B5498", font="20", fg="white")
        comparisonLabel.place(x=580, y=85, anchor="center") # draws text/numbers

        now = dt.datetime.now()
        now2 = now.strftime("%Y-%m-%d")

        if now2 != oldDate: # if today's date != date in file, then write new date -> numbers change
            memory = open("numbers.txt", "w+") # date is stored in the txt file
            memory.write(newNumbers)
            memory.write("\n")
            memory.write(now.strftime("%Y-%m-%d"))
            memory.close()
            logger.info("Date has been updated.")
    except Exception as error:  # in case of missing numbers.txt file (file has to include an integer -> here at start 0)
        tk.messagebox.showerror(title="Error", message=str(error))
        logger.error("Error occurred: " + error)

def prop(n): # to draw pie chart
    return 360.0 * n / 1000

#VARIABLES--------------------------------------------------------------------------------------#
coordinates = [15, 340, 15, 340]
xPos = 15
yPos = 340

#INITIALISATION---------------------------------------------------------------------------------#
mainWindow = tk.Tk()
mainWindow.title("Contact and Warehouse Management System")
mainWindow.geometry("1200x800")
mainWindow.resizable(False, False)

loginWindow = tk.Toplevel()
loginWindow.title("Login")
loginWindow.resizable(False, False)
loginWindow.configure(background="#3B5498")

#LOGGING----------------------------------------------------------------------------------------#
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s |  %(levelname)s IN LINE %(lineno)s | %(funcName)s | %(message)s", filename="logs.txt", datefmt="%Y-%m-%d %H:%M:%S") # logging format
logger = logging.getLogger()
logger.info("-----------------------------------------------------------------------------------------------------------")
logger.info("Session started.")

#TAB-BAR----------------------------------------------------------------------------------------#
tabBar = ttk.Notebook(mainWindow) # initializing tabbar

dashboardTab = ttk.Frame(tabBar) # individual tabs
stockTab = ttk.Frame(tabBar)
contactTab = ttk.Frame(tabBar)
adminTab = ttk.Frame(tabBar)

tabBar.add(dashboardTab, text="Dashboard") # tabs added to tabbar
tabBar.add(stockTab, text="Stock")
tabBar.add(contactTab, text="Contacts")
tabBar.add(adminTab, text="Admin")

tabBar.pack(expand=1, fill="both")

style = ttk.Style() # styling tabs and background
style.theme_use("default") # pre-installed theme used -> more modern look
style.configure("TFrame", background="#263150")
style.configure("TNotebook", background="#2A2A2A")
style.configure("TNotebook.Tab", background="#F4B800")

#DB-CREATION------------------------------------------------------------------------------------#
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username VARCHAR(30), email VARCHAR(30), status VARCHAR(15), registration DATE, password VARCHAR(30))")
cursor.execute("CREATE TABLE IF NOT EXISTS stock (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(15), category VARCHAR(15), manufacturer VARCHAR(15), quantity VARCHAR(10))")
cursor.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, firstname VARCHAR(30), lastname VARCHAR(30), status VARCHAR(15), customersince DATE)")

#RUN-THIS-ONCE-TO-GET-ACCESS-PW:admin-USERNAME:admin----------------------------------------------#
#now = dt.datetime.now()
#now2 = now.strftime("%Y-%m-%d")
#cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)", (None, "admin", "admin", "admin", now2, encode("admin")))
#logger.info("First-startup-code was executed")
#-----------------------------------------------------------------------------------------------#

connection.commit()
connection.close()

#LOGIN-GUI--------------------------------------------------------------------------------------#
loginLabel = tk.Label(master=loginWindow, text="          Please login to access the program!         ", bg="#3B5498", fg="#F4B800", font=20).grid(row=1, columnspan=8)
usernameLabel = tk.Label(master=loginWindow, text="Username", bg="#3B5498", fg="white").grid(row=3, column=1)
passwordLabel = tk.Label(master=loginWindow, text="Password", bg="#3B5498", fg="white").grid(row=4, column=1)
usernameEntry = tk.Entry(master=loginWindow, bg="#2A2A2A", fg="white", justify="center")
usernameEntry.grid(row=3, column=2, columnspan=5)
passwordEntry = tk.Entry(master=loginWindow, bg="#2A2A2A", fg="white", show="*", justify="center")
passwordEntry.grid(row=4, column=2, columnspan=5)
loginButton = tk.Button(master=loginWindow, text="Login", command=lambda: [validateLogin()], bg="#2A2A2A", fg="white").grid(row=6, column=4)
cancelButton = tk.Button(master=loginWindow, text="Cancel", command=lambda: [cancelLogin()], bg="#2A2A2A", fg="white").grid(row=6, column=1)
spaceHolder1 = tk.Label(master=loginWindow, text="", bg="#3B5498").grid(row=0, columnspan=8)
spaceHolder2 = tk.Label(master=loginWindow, text="", bg="#3B5498").grid(row=2, columnspan=6)
spaceHolder3 = tk.Label(master=loginWindow, text="", bg="#3B5498").grid(row=5, columnspan=6)
spaceHolder4 = tk.Label(master=loginWindow, text="", bg="#3B5498").grid(row=7, columnspan=6)

#DASHBOARD-GUI----------------------------------------------------------------------------------#
Header(dashboardTab, "Dashboard")

numbersFrame = tk.Frame(dashboardTab, width=1164, height=200, bg="#3B5498", highlightcolor="white", highlightthickness=2)
compareNumbers()

graphLeft = tk.Canvas(master=dashboardTab, width=570, height=350, bg="#3B5498") # left graph showing amount of contacts in contacts table
graphLeft.create_line(15, 340, 400, 340, width=2, fill="white") #X-ACHSE
graphLeft.create_line(15, 25, 15, 340, width=2, fill="white") #Y-ACHSE
graphLeft.create_text(275, 15, text="Anzahl der Kunden", font=15, fill="white")

graphRight = tk.Canvas(master=dashboardTab, width=570, height=350, bg="#3B5498") # draw pie chart (not related to any data)
graphRight.create_arc((150, 100, 450, 400), fill="#00F466", outline="#00F466", start=prop(0), extent=prop(200))
graphRight.create_arc((150, 100, 450, 400), fill="#F4B800", outline="#F4B800", start=prop(200), extent=prop(400))
graphRight.create_arc((150, 100, 450, 400), fill="#E00022", outline="#E00022", start=prop(600), extent=prop(50))
graphRight.create_arc((150, 100, 450, 400), fill="#7A0871", outline="#7A0871", start=prop(650), extent=prop(200))
graphRight.create_arc((150, 100, 450, 400), fill="#294994", outline="#294994", start=prop(850), extent=prop(150))

numbersFrame.place(x=20, y=190)
graphLeft.place(x=20, y=410)
graphRight.place(x=610, y=410)

#STOCK-GUI--------------------------------------------------------------------------------------#
Header(stockTab, "Stock")

columns = ["ID", "name", "category", "manufacturer", "quantity"]
headings = ["ID", "Product Name", "Category", "Manufacturer", "Quantity"]
table = "stock"
text = "Stock"
stock = Table(stockTab, columns, headings, text, table)

#CONTACT-GUI------------------------------------------------------------------------------------#
Header(contactTab, "Contacts")

columns = ["ID", "first_name", "last_name", "status", "first_order"]
headings = ["ID", "First Name", "Last Name", "Status", "First Order"]
table = "customers"
text = "Contacts"
contacts = Table(contactTab, columns, headings, text , table)

#ADMIN-GUI--------------------------------------------------------------------------------------#
Header(adminTab, "Manage")

columns = ["ID", "username", "email", "status", "registration"]
headings = ["ID", "Username", "Email-Address", "Status", "Registration"]
table = "accounts"
text = "Accounts"
contacts = Table(adminTab, columns, headings, text, table)

#HIDE MAIN WINDOW UNTIL SUCCESSFUL LOGIN--------------------------------------------------------#
mainWindow.withdraw()

#SET ICONS--------------------------------------------------------------------------------------#
mainWindow.iconbitmap("icon.ico")
loginWindow.iconbitmap("icon.ico")

#CALL DEFs--------------------------------------------------------------------------------------#
drawGraph()
Header.displayTime

#MAINLOOP---------------------------------------------------------------------------------------#
mainWindow.mainloop()
logger.info("End of session.")