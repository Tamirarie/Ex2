import os.path
import sqlite3
import csv
from datetime import datetime
import math

def Createtime(value):
    hour = value[:2]
    minute = value[2:4]
    second = value[4:6]
    timeval = hour + ":" + minute + ":" + second
    return timeval

def Createdate(value):
    day = value[:2]
    month = value[2:4]
    year = value[4:6]
    dateval = "20"+year+"-"+month+"-"+day+"T"
    return dateval

def getRMCdata(row):
    warning = row[2]
    if warning == 'V':
        return
   # time = row[1]
    speed = row[7]
    date =  row[9]
    date = Createdate(date)
    # merge the time and date columns into one Python datetime object (usually more convenient than having both separately)
    # date_and_time = datetime.strptime(date + ' ' + time, '%d%m%y %H%M%S.%f')

    # convert the Python datetime into your preferred string format, see http://www.tutorialspoint.com/python/time_strftime.htm for futher possibilities
    #   date_and_time = date_and_time.strftime('%y-%m-%d %H:%M:%S.%f')[:-3] # [:-3] cuts off the last three characters (trailing zeros from the fractional seconds)
    # speed is given in knots, you'll probably rather want it in km/h and rounded to full integer values.
    # speed has to be converted from string to float first in order to do calculations with it.
    # conversion to int is to get rid of the tailing ".0".
    speed = int(round(float(speed) * 1.852, 0))
    listRMC = [speed,date]
    
    return listRMC

def getGGAdata(row):
    
    time = row[1]
    lat = row[2]
    lat_direction = row[3]
    lon = row[4]
    lon_direction = row[5]
    fix_quality = row[6]
    numOfSat = row[7]
    hdop = row[8]
    altitude = row[9]
    meters =  row[10]
    heightofGeoid = row[11]
    
    time = Createtime(time)
    # lat and lon values in the $GPRMC nmea sentences come in an rather uncommon format. for convenience, convert them into the commonly used decimal degree format which most applications can read.
    # the "high level" formula for conversion is: DDMM.MMMMM => DD + (YY.ZZZZ / 60), multiplicated with (-1) if direction is either South or West
    # the following reflects this formula in mathematical terms.
    # lat and lon have to be converted from string to float in order to do calculations with them.
    # you probably want the values rounded to 6 digits after the point for better readability.
                
                
    if isinstance( lat, ( int, float )):
                    lat = round(math.floor(float(lat) / 100) + (float(lat) % 100) / 60, 6)
                    if lat_direction == 'S':
                        lat = lat * -1
                    
    if isinstance( lon, ( int, float )):
                    lon = round(math.floor(float(lon) / 100) + (float(lon) % 100) / 60, 6)
                    if lon_direction == 'W':
                        lon = lon * -1
                        
                        
    listGGA = [time,lat,lat_direction,lon,lon_direction,fix_quality,numOfSat,hdop,altitude,meters,heightofGeoid]
    return listGGA


def checkLine(line):                         # checkLine Function - Fix the line to start with '$'
    if (line[0] != '$'):
        j = 0
        while line[j] != '$':
            j = j + 1
        line1 = line[j:]
        return line1
    return line
def find_GA(list1,index):
    while "GPGGA" not in list1[index] and index<len(list1)-2:
        index=index+1
    if index >= len(list1) - 1:
        return -1
    string=list1[index].split(",")
    if (string[1]==''):
        return find_GA(list1,index+1)

    return index
def findMC(list,index):
    while "GPRMC" not in list[index] and index<len(list)-2:
        index=index+1
    if index>=len(list)-1:
        return -1
    str=list[index].split(",")
    if (str[1]==''):
        return find_GA(list,index+1)
    return index


def nmeaGGA(INPUT,TableName):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    l = str(TableName)
    listName = l.split(sep='.')
    print(list)
    # Create table
    c.execute('drop table if exists ' + str(listName[0]) )
    c.execute('''CREATE TABLE '''+ str(listName[0]) + '''
             (time text,latitude text,north text,longitude text,east text,
             fix_quality text,numOfSat text,hdop text,altitude text,
            meters text, heightOfGeoid text, speed text, date text )''')
    
    with open(INPUT, 'r') as input_file:
        print(input_file)
        reader = csv.reader(input_file)
        # iterate over all the rows in the nmea file
        for row in reader:
            
        # skip all lines that do not start with $GPRMC
        ## if not row[0].startswith('$GPGGA'):
            if "RMC" in row[0]:
                listRMC = getRMCdata(row)
                if( listRMC!= None):
                    c.execute("INSERT INTO " + str(listName[0]) + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (' ',' ',' ',' ',' ',' '
                         ,' ',' ',' ',' ',' ',
                         listRMC[0],listRMC[1])
                        )
                
            elif "GGA" in row[0] :
                listGGA = getGGAdata(row)
                c.execute("INSERT INTO " + str(listName[0]) + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (listGGA[0],listGGA[1],listGGA[2],listGGA[3],listGGA[4],listGGA[5],
                         listGGA[6],listGGA[7],listGGA[8],listGGA[9],listGGA[10],
                         '','')
                        )
            
#             c.execute("INSERT INTO " + str(listName[0]) + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
#                         (listGGA[0],listGGA[1],listGGA[2],listGGA[3],listGGA[4],listGGA[5],
#                          listGGA[6],listGGA[7],listGGA[8],listGGA[9],listGGA[10],
#                          listRMC[0],listRMC[1])
#                         )

        # Save (commit) the changes
        conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
        conn.close()

def read_dir(dir_name):
    if os.path.isdir(dir_name):
        l = os.listdir(dir_name)
        for k in range(len(l)):
                nmeaGGA(dir_name + "\\"+l[k],l[k])
                
                


def dropAll():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    tables = list(c.execute("select name from sqlite_master where type is 'table'"))

    c.executescript(';'.join(["drop table if exists %s" % i for i in tables]))    
    
    
INPUT = 'NMEAfiles'
dropAll()
##nmeaGGA(INPUT+"\FlightLog.nmea",'FlightLog')

read_dir(INPUT)

##nmeaGGA(INPUT)
##nmeaRMC(INPUT)

