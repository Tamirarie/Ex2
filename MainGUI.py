import tkinter
import NmeaToDB
import DBConverter
import sqlite3
from sqlite3 import OperationalError
import datetime, time

def OpenDB():
    print()
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
    
 
        


root = tkinter.Tk()
root.title("NMEA TO CSV PROGRAM")
root.geometry("350x250")
app = tkinter.Frame(root)
app.grid()

NmeaRunButton = tkinter.Button(app , text = "Click to convert!" , command= NmeaToDB.load_dir)
NmeaRunButton.pack()



ConvertToCSVbutton = tkinter.Button(app , text = "Convert This NMEA to CSV!" , command = DBConverter.loadDBtoCSV)
ConvertToCSVbutton.pack()

ConvertToKMLbutton = tkinter.Button(app ,text = "Convert This NMEA to KML!"  , command = DBConverter.loadDBtoKML)
ConvertToKMLbutton.pack()

GoogleEbutton = tkinter.Button(app , text = "Show on Google Earth")
GoogleEbutton.pack()

QueryButton = tkinter.Button(app, text="Click To run Queries:", command = executeScriptsFromFile)
QueryButton.pack()


tkinter.mainloop()
