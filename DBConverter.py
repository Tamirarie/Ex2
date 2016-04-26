import csv
import sqlite3
import NmeaToDB

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

import nmeagram


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


def nmeaFileToCoords(lines):
    """Read a file full of NMEA sentences and return a string of lat/lon/z
    coordinates.  'z' is often 0.
    """
    data = []
    for line in lines:
        if line[:6] in ("$GPGGA", "$GPGLL"):
            nmeagram.parseLine(line)
            data.append(str(nmeagram.getField("UtcTime")))
            data.append(",")
            data.append(str(nmeagram.getField("Longitude")))
            data.append(",")
            data.append(str(nmeagram.getField("Latitude")))
            data.append(",0 ")
    return str.join('',data)  

def DBtoCSV(NameFile):
    conn = sqlite3.connect("example.db") #open db
    cursor = conn.cursor() #cursor to the db
    cursor.execute('select * from '+NameFile) # execute a sql script

    with open(NameFile+".csv",'w', newline='') as csv_file: #writing to csv
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description]) # write headers
        csv_writer.writerows(cursor)
        
def DBtoKML(NameFile):
    conn = sqlite3.connect("example.db") #open db
    cursor = conn.cursor() #cursor to the db
    lines = cursor.execute('select * from '+NameFile) # execute a sql script

    fo = open(NameFile + KML_EXT, 'w')
    fo.write(KML_TEMPLATE % (NameFile, NameFile, nmeaFileToCoords(lines)))
    
def create_kml(i):
    skip=5
    database = sqlite3.connect('example.db')
    pois = database.execute("SELECT * FROM " + str(i))
    file = 'file' + str(i) + '.kml'
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
            print('%s : %s, %s' % (poi, poi[2], poi[1],))
            FILE.write('<Placemark>\n')
            FILE.write('    <TimeStamp>\n')
            FILE.write('     <when>%s%s</when>\n' % (NmeaToDB.Createdate(poi[11]),NmeaToDB.Createtime(poi[0])))
            FILE.write('    </TimeStamp>\n')
            lat = float(poi[2]) + (float(poi[2]) / 60)
            lon = float(poi[4][:4]) + (float(poi[4][4:]) / 60)
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


create_kml('stockholm_walk')