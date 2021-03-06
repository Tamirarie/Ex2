import tkinter
import NmeaToDB
import DBConverter
import sqlite3
from sqlite3 import OperationalError
import os,subprocess
import time

"""
MainGUI.py - a program to present a nice UI using the methods
of NmeaToDB.py and DBConverter

:Author: Tamir Arie
:Revision: 0.1
:Date: 2016/05/03

"""


def showGoogleEarth():
    if os.path.isdir('KMLfiles'):
        l = os.listdir('KMLfiles')
        for k in range(len(l)):
            l2 = str(l[k])
            os.startfile('KMLfiles\\'+l2)
            time.sleep(5)
    
def OpenDB():
    database = 'NMEA_DB.db'
    sqlitebrowser = r'C:\Program Files\SqliteBrowser3\bin\sqlitebrowser.exe'
    subprocess.Popen("%s %s" % (sqlitebrowser,database))
##################################

    
def executeScriptsFromFile():
    conn = sqlite3.connect('NMEA_DB.db')
    c = conn.cursor()
    # Open and read the file as a single buffer
    fd = open('Query.sql', 'r')
    sqlFile = fd.read()
    fd.close()
    file = 'QueryOut.txt'
    FILE = open(file, 'w')
    FILE.truncate(0)
    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        if(command == ''): break
        try:
            result = c.execute(command)

    # Get all rows.
            rows = result.fetchall();
            index = command.find("from")
            tableName = command[index:]
    # \n represents an end-of-line
            FILE.write("\n--- TABLE ")
            FILE.write(tableName)
            FILE.write("\n")
    # This will print the name of the columns, padding each name up
    # to 22 characters. Note that comma at the end prevents new lines
            for desc in result.description:
                FILE.write(desc[0].rjust(22, ' '),)

    # End the line with column names
            FILE.write("\n")
            for row in rows:
                for value in row:
            # Print each value, padding it up with ' ' to 22 characters on the right
                    FILE.write (str(value).rjust(22, ' '),)
        # End the values from the row
                FILE.write("\n")

        except OperationalError:
            print ('Command skipped') 
            
    c.close()
    conn.close()
    
 
        
######################################################################

root = tkinter.Tk()
root.title("NMEA TO DB Program")
root.geometry("400x400")
app = tkinter.Frame(root)
app.grid()

NmeaRunButton = tkinter.Button(app , text = "Click to convert!" , command= NmeaToDB.load_dir)
NmeaRunButton.pack()



ConvertToCSVbutton = tkinter.Button(app , text = "Convert This DB to CSV!" , command = DBConverter.loadDBtoCSV)
ConvertToCSVbutton.pack()

ConvertToKMLbutton = tkinter.Button(app ,text = "Convert This DB to KML!"  , command = DBConverter.loadDBtoKML)
ConvertToKMLbutton.pack()

GoogleEbutton = tkinter.Button(app , text = "Show on Google Earth",command = showGoogleEarth)
GoogleEbutton.pack()

QueryButton = tkinter.Button(app, text="Click To run Queries:\n (Opening Query.sql and creating QueryOut.txt)", command = executeScriptsFromFile)
QueryButton.pack()

OpenDBbutton = tkinter.Button(app, text="Click To Open DB:\n (only if having sqlitebrowser)", command = OpenDB)
OpenDBbutton.pack()

NmeaRunButton.config(height = '3', width = '50')
ConvertToCSVbutton.config(height = '3', width = '50')
ConvertToKMLbutton.config(height = '3', width = '50')
GoogleEbutton.config(height = '3', width = '50')
QueryButton.config(height = '3', width = '50')
OpenDBbutton.config(height = '3', width = '50')
tkinter.mainloop()
