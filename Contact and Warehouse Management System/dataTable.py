# IMPORTS
import tkinter as tk # FOR GUI
from tkinter import messagebox # FOR ERROR BOX WHEN E.G. SEARCH FAILS

from tkinter import ttk # FOR DATA TABLE

import sqlite3 # FOR DATABASE

import logging # LOGGING ERRORS

#LOGGING----------------------------------------------------------------------------------------#
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s |  %(levelname)s IN LINE %(lineno)s | %(funcName)s | %(message)s", filename="logs.txt", datefmt="%Y-%m-%d %H:%M:%S") # logging format
logger = logging.getLogger()

#TABLE-CLASS------------------------------------------------------------------------------------#
class Table():

    def __init__(self, master=None, columns=None, headings=None, text=None, table=None, options=None):
        self.master = master
        self.columns = columns
        self.headings = headings
        self.text = text
        self.table = table
        self.options = options

        #WIDGET-CREATION--------------------------------------------------------------------------------#
        self.tableFrame = tk.Frame(master=self.master, width=1160, height=685, bg="white", highlightcolor="white", highlightthickness=2)
        self.managingFrame = tk.Frame(master=self.master, width=1164, height=125, bg="#3B5498", highlightcolor="white", highlightthickness=2)
        self.manageText = tk.Label(master=self.managingFrame, text="Manage " + str(self.text), bg="#3B5498", fg="white", justify="center")

        self.entryOne = tk.Entry(master=self.managingFrame, width=37, bg="#2A2A2A", fg="white", justify="center")
        self.entryTwo = tk.Entry(master=self.managingFrame, width=38, bg="#2A2A2A", fg="white", justify="center")
        self.entryThree = tk.Entry(master=self.managingFrame, width=38, bg="#2A2A2A", fg="white", justify="center")
        self.entryFour = tk.Entry(master=self.managingFrame, width=38, bg="#2A2A2A", fg="white", justify="center")
        self.entryFive = tk.Entry(master=self.managingFrame, width=41, bg="#2A2A2A", fg="white", justify="center")

        self.modeOne = tk.Button(master=self.managingFrame, width=20, bg="#2A2A2A", fg="white", text="Add", command=self.addEntry)
        self.modeTwo = tk.Button(master=self.managingFrame, width=20, bg="#2A2A2A", fg="white", text="Remove selected", command=self.removeSelected)
        self.modeThree = tk.Button(master=self.managingFrame, width=20, bg="#2A2A2A", fg="white", text="Overwrite selected (no ID)", command=self.overwriteSelected)
        self.modeFour = tk.Button(master=self.managingFrame, width=20, bg="#2A2A2A", fg="white", text="Search (by Keyword ->)", command=self.searchEntry)

        self.searchText = tk.Entry(master=self.managingFrame, bg="#2A2A2A", fg="white", justify="center", font=8)
        self.searchText["relief"] = "raised"

        self.tableFrame.place(x=20, y=55)
        self.managingFrame.place(x=20, y=633)
        self.manageText.place(x=64, y=100)

        self.entryOne.place(x=0, y=0)
        self.entryTwo.place(x=225, y=0)
        self.entryThree.place(x=455, y=0)
        self.entryFour.place(x=685, y=0)
        self.entryFive.place(x=910, y=0)

        self.modeOne.place(x=38, y=25)
        self.modeTwo.place(x=270, y=25)
        self.modeThree.place(x=502, y=25)
        self.modeFour.place(x=724, y=25)

        self.searchText.place(x=940, y=27)

        self.dataTable = ttk.Treeview(master=self.tableFrame, columns=self.columns, show="headings", height=28)

        #TABLE-STYLE-CONFIG-----------------------------------------------------------------------------#
        style = ttk.Style(self.master) # Treeview (data table) styling
        style.configure("Treeview", background="#3B5498", foreground="white") # Treeview background style
        style.configure("Treeview.Heading", background="#2A2A2A", foreground="white") # style of headings
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        #TABLE-CREATION---------------------------------------------------------------------------------#
        k = 0
        for column in self.columns:
            self.dataTable.column(self.columns[k], width=229, minwidth=229, stretch="no", anchor="center")
            k += 1

        l = 0
        for heading in self.headings:
            self.dataTable.heading(self.columns[l], text=self.headings[l])
            l += 1

        #INSERT-DATA------------------------------------------------------------------------------------#
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        m = 0
        query = "SELECT * FROM " + str(self.table)
        entries = cursor.execute(query)
        for entrie in entries:
            self.dataTable.insert("", "end", values=entrie)
            m += 1

        connection.close()

        self.dataTable.pack(side="left")

        #ADD-SCROLLBAR----------------------------------------------------------------------------------#
        self.scrollbar = ttk.Scrollbar(self.tableFrame, orient=tk.VERTICAL, command=self.dataTable.yview)
        self.dataTable.config(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

    def refresh(self): # displays data table with new data
        self.dataTable.delete(*self.dataTable.get_children())

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        m = 0
        entries = cursor.execute("SELECT * FROM " + str(self.table))
        for entrie in entries:
            self.dataTable.insert("", "end", values=entrie)
            m += 1

        connection.close()

        self.dataTable.pack(side="left")

        table = self.table
        logger.info("The data table '" + table + "' was updated.")

    def clearEntries(self):
        self.entryOne.delete("0", "end")
        self.entryTwo.delete("0", "end")
        self.entryThree.delete("0", "end")
        self.entryFour.delete("0", "end")
        self.entryFive.delete("0", "end")

    #BUTTON-COMMANDS--------------------------------------------------------------------------------#
    def addEntry(self):
        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            enteredID = self.entryOne.get()
            cursor.execute("SELECT * FROM " + str(self.table) + " WHERE id=?", (enteredID,))
            check = cursor.fetchone()

            if check is None: # if ID was not already assigned:
                if str(self.table) == "accounts": # test if current data table is the accounts data table, because it has one value more than the others (password)
                    cursor.execute("INSERT INTO " + str(self.table) + " VALUES (?, ?, ?, ?, ?, ?)", (self.entryOne.get(), self.entryTwo.get(), self.entryThree.get(), self.entryFour.get(), self.entryFive.get(), None))
                    table = self.table
                    entry = [self.entryOne.get(), self.entryTwo.get(), self.entryThree.get(), self.entryFour.get(), self.entryFive.get()]
                    logger.info("An entry was added to the '" + table + "' data table: [" + str(entry) + "]")
                else: # if not data table: add info to table
                    cursor.execute("INSERT INTO " + str(self.table) + " VALUES (?, ?, ?, ?, ?)", (self.entryOne.get(), self.entryTwo.get(), self.entryThree.get(), self.entryFour.get(), self.entryFive.get()))
                    table = self.table
                    entry = [self.entryOne.get(), self.entryTwo.get(), self.entryThree.get(), self.entryFour.get(), self.entryFive.get()]
                    logger.info("An entry was added to the '" + table + "' data table: [" + str(entry) + "]")
            else: # if check is not None: ID was already assigned
                tk.messagebox.showerror(title="Action failed", message="ID was already assigned: \n" + str(check))
                table = self.table
                logger.info("Adding an entry to the data table '" + table + "' failed: ID was already assigned")

            connection.commit()
            connection.close()

            self.clearEntries()
            self.refresh() # show data table with new data

        except: # ID was not specified
            tk.messagebox.showerror(title="Action failed", message="An input value is missing. At least the ID must be specified!")
            table = self.table
            logger.info("Adding an entry to the data table '" + table + "' failed: missing input value(s).")

    def searchEntry(self): # searches Treeview for keyword, highlights findings
        keyword = self.searchText.get()

        if keyword == "": # Keyword cannot be None
            tk.messagebox.showerror(title="Action failed", message="You need to enter a keyword.")
            logger.info("Search failed: no keyword was entered")

        else:
            findings = []
            for item in self.dataTable.get_children(): # scan Treeview for findings
                if keyword in self.dataTable.item(item)["values"]:
                    findings.append(item) # add findings to list

            if len(findings) == 0: # if no findings:
                tk.messagebox.showerror(title="Action failed", message="No entries with the keyword '" + str(self.searchText.get()) + "' were found.")
                table = self.table
                logger.info("Search succeded but no entries with the keyword '" + self.searchText.get() + "' were found in the data table '" + table + "'.")
            else: # if smth was found:
                self.dataTable.selection_set(findings) # highlights findings
                tk.messagebox.showinfo(title="Success", message=str(len(findings)) + " entries with the keyword '" + str(self.searchText.get()) + "' were found and highlighted.")
                table = self.table
                logger.info("Search for keyword '" + self.searchText.get() + "' succeded. Following items have been found in the '" + table + "' data table: " + str(findings))

    def overwriteSelected(self): # overwrites by user selected items with by user given input (without changing ID)
        try:
            selection = self.dataTable.item(self.dataTable.focus()) # get by user selected items
            selectedID = selection["values"][0] # gets data table ID of selected item

            if self.table == "accounts" and selectedID == 1: # check if data table is account table and selected ID == 1, account with ID == 1 is admin account -> should not be deleted
                tk.messagebox.showerror(title="Action failed", message="Admin account cannot be overwritten.")
            else:
                connection = sqlite3.connect("data.db")
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM " + str(self.table))
                headers = [i[0] for i in cursor.description] # gets column headers of the data table

                cursor.execute("UPDATE {table} SET {header}=? WHERE id=?".format(table=self.table, header=headers[1]), (self.entryTwo.get(), selectedID)) # didn't know how to add all strings together
                cursor.execute("UPDATE {table} SET {header}=? WHERE id=?".format(table=self.table, header=headers[2]), (self.entryThree.get(), selectedID)) # so I did it 1 by 1
                cursor.execute("UPDATE {table} SET {header}=? WHERE id=?".format(table=self.table, header=headers[3]), (self.entryFour.get(), selectedID))
                cursor.execute("UPDATE {table} SET {header}=? WHERE id=?".format(table=self.table, header=headers[4]), (self.entryFive.get(), selectedID))

                connection.commit()
                connection.close()

                self.refresh()
                self.clearEntries()

                table = self.table
                entry = [self.entryOne.get(), self.entryTwo.get(), self.entryThree.get(), self.entryFour.get(), self.entryFive.get()]
                logger.info("An Entry (ID: " + str(selectedID) + ") from the '" + table + "' data table was overwritten. New data: [" + str(entry) + "]")
        except: # in case no item is selected
            tk.messagebox.showerror(title="Action failed", message="You need to select an item first.")

    def removeSelected(self): # removes by user selected item from database
        try:
            selection = self.dataTable.item(self.dataTable.focus()) # gets user selection (highlighted)
            selectedID = selection["values"][0] # gets the data table ID of the selection

            if self.table == "accounts" and selectedID == 1: # tests if to be removed account is the admin account
                tk.messagebox.showerror(title="Action failed", message="Admin account cannot be deleted.")
            else:
                connection = sqlite3.connect("data.db")
                cursor = connection.cursor()
                cursor.execute("DELETE FROM " + str(self.table) + " WHERE id=?", (selectedID,)) # deletes entry with the ID
                connection.commit()
                connection.close()

                self.refresh()

                table = self.table
                logger.info("Entry (ID: " + str(selectedID) + ") was removed from the '" + table + "' data table.")

        except: # in case no item is selected
            tk.messagebox.showerror(title="Action failed", message="You need to select an item first.")
