import csv
import sqlite3
import os.path
"""
nmeatokml.py - Converts an NMEA data file to a KML track

Uses lon/lat data fields from the NMEA sentences as location coordinates
for the KML track data set.

:Copyright: Copyright 2007 Dean Hall.  All rights reserved.
:Author: Dean Hall
:Revision: 0.1
:Date: 2007/12/10

:usage: nmeatokml.py nmeadatafilename
:usage: nmeatokml.py < filename.nmea > filename.kml
"""

KML_EXT = ".kml"


KML_TEMPLATE = \
"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>
  <name>NMEA to KML: %s</name>
  <Style id="dwhStyle000">
    <LineStyle id="dwhLineStyleRed6">
      <color>7f0000ff</color>
      <width>6</width>
    </LineStyle>
  </Style>
  <Placemark>
    <name>%s</name>
    <styleUrl>#dwhStyle000</styleUrl>
    <MultiGeometry>
      <LineString>
        <TimeStamp>
            <when></when>
        </TimeStamp>
        <coordinates>
        %s
        </coordinates>
      </LineString>
    </MultiGeometry>
  </Placemark>
</Document>
</kml>
"""




def FiletoCSV(NameFile):
    conn = sqlite3.connect("NMEA_DB.db") #open db
    cursor = conn.cursor() #cursor to the db
    cursor.execute('select * from '+NameFile) # execute a sql script
    
    if not os.path.exists('CSVfiles'):
        os.makedirs('CSVfiles')
        
    with open('CSVfiles\\'+NameFile+".csv",'w', newline='') as csv_file: #writing to csv
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description]) # write headers
        csv_writer.writerows(cursor)
        
    
def FiletoKML(NameFile):
    skip=5
    database = sqlite3.connect('NMEA_DB.db')
    pois = database.execute("SELECT * FROM " + str(NameFile))
    if not os.path.exists('KMLfiles'):
        os.makedirs('KMLfiles')
    
    file = 'KMLfiles\\' + str(NameFile) + '.kml'
    FILE = open(file, 'w')
    FILE.truncate(0)
    FILE.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
    FILE.write('<kml xmlns="http://earth.google.com/kml/2.0">\n')
    FILE.write('    <Document>\n')
    FILE.write('     <Folder>\n')
    FILE.write('     <name>Point Features</name>\n')
    FILE.write('     <description>Point Features</description>\n\n')
    j=0
    for poi in pois:
        if j%skip==0:
            FILE.write('<Placemark>\n')
            FILE.write('    <TimeStamp>\n')
            FILE.write('     <when>%s%s</when>\n' % (poi[11],poi[0]))
            FILE.write('    </TimeStamp>\n')
            lat = float(poi[1][:2]) + (float(poi[1][2:]) / 60)
            lon = float(poi[3][:3]) + (float(poi[3][3:]) / 60)
            FILE.write('    <description><![CDATA[Lat: %s <br> Lon: %s<br> Speed: %s <br>]]></description>\n' % (lat, lon,(poi[10])))
            FILE.write('    <Point>\n')

            FILE.write('        <coordinates>%s,%s,%s</coordinates>\n' % (str(lon), str(lat), poi[8]))
            FILE.write('    </Point>\n')
            FILE.write('</Placemark>\n')
            j=j+1
        else:
            j=j+1
    FILE.write('        </Folder>\n')
    FILE.write('    </Document>\n')
    FILE.write('</kml>\n')
    FILE.close()
    database.close()    

def loadDBtoCSV():
    DBtoCSV('NMEAfiles')
def DBtoCSV(dir_name):
    if os.path.isdir(dir_name):
        l = os.listdir(dir_name)
        for k in range(len(l)):
            l2 = str(l[k])
            listName = l2.split(sep='.')
            FiletoCSV(str(listName[0]))

def loadDBtoKML():
    DBtoKML('NMEAfiles')            
def DBtoKML(dir_name):
    if os.path.isdir(dir_name):
        l = os.listdir(dir_name)
        for k in range(len(l)):
            l2 = str(l[k])
            listName = l2.split(sep='.')
            FiletoKML(str(listName[0]))
