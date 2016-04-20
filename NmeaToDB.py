import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS stocks 
             (date text, trans text, symbol text, qty real, price real)''')

##c.execute('''CREATE TABLE IF NOT EXISTS nmea
 ##            (time text,latitude text,north text,longitude text,east text,
 ##            fix_quality text,numOfSat text,hdop text,altitude text,
  ##           meters text, heightOfGeoid text, timeLU text, checkSum text )''')
  
c.execute('''CREATE TABLE IF NOT EXISTS nmea
             (time text,latitude text,north text,longitude text,east text,
             fix_quality text,numOfSat text,hdop text,altitude text,
            meters text, heightOfGeoid text, timeLU text, checkSum text )''')


# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()