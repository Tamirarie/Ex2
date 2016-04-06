#! /usr/bin/env python
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


import os, sys
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
        <coordinates>
        %s
        </coordinates>
      </LineString>
    </MultiGeometry>
  </Placemark>
</Document>
</kml>
"""


def nmeaFileToCoords(f):
    """Read a file full of NMEA sentences and return a string of lat/lon/z
    coordinates.  'z' is often 0.
    """
    data = []
    for line in f.readlines():
        if line[:6] in ("$GPGGA", "$GPGLL"):
            nmeagram.parseLine(line)
            data.append(str(nmeagram.getField("Longitude")))
            data.append(",")
            data.append(str(nmeagram.getField("Latitude")))
            data.append(",0 ")
    return str.join('',data)  


def main():
    # If no args given, assume stdio
    if len(sys.argv) == 1:
        sys.stdout.write(KML_TEMPLATE % ("stdio", "stdio", nmeaFileToCoords(sys.stdin)))

    # If filename is given, use it
    elif len(sys.argv) == 2:

        # The input file should exist
        fn = sys.argv[1]
        assert os.path.exists(fn)

        # Create the KML output file
        fo = open(fn + KML_EXT, 'w')
        fi = open(fn, 'r')
        fo.write(KML_TEMPLATE % (fn, fn, nmeaFileToCoords(fi)))
        fi.close()
        fo.close()

    else:
        sys.stderr.write(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()