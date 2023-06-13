# IMPORTS
import tkinter as tk # FOR GUI

import time # FOR DISPLAYING DATE & TIME
import datetime as dt

# VARIABLES
timeX = ""

#HEADER-CLASS-----------------------------------------------------------------------------------#
class Header():
    def __init__(self, master = None, text=None):
        self.Master = master
        self.Text = text
        self.createWidgets()
        self.displayTime()

    def createWidgets(self):
        self.headerFrame = tk.Frame(master=self.Master, width=1200, height=35, bg="#263150")
        self.tabName = tk.Label(master=self.headerFrame, text=self.Text, font="20", bg="#263150", fg="white")
        self.timeModule = tk.Label(master=self.headerFrame, font="20", bg="#263150", fg="white")
        self.dateModule = tk.Label(master=self.headerFrame, text=f"{dt.datetime.now():%A, %B, %d, %Y}", font="20", bg="#263150", fg="white") # draws date

        self.headerFrame.place(x=0, y=0)
        self.tabName.place(x=595, y=17, anchor="center")
        self.timeModule.place(x=1120, y=5)
        self.dateModule.place(x=5, y=5)

    def displayTime(self):
        global timeX

        timeY = time.strftime("%H:%M:%S") # get time

        if timeY != timeX:
            timeX = timeY
            self.timeModule.config(text=timeY) # draws time update

        self.timeModule.after(200, self.displayTime) # runs displayTime() every 200 ticks