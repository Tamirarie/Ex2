try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    
import pynmea2

TEST_DATA = """$GPRMC,181031.576,V,3926.276,N,07739.361,W,99.7,18.30,250915,,E*79
$GPGGA,181032.576,3926.276,N,07739.361,W,0,00,,,M,,M,,*5F
$GPGLL,3926.276,N,07739.361,W,181033.576,V*3E
$GPRMC,181034.576,V,3949.797,N,07809.854,W,18.8,34.66,250915,,E*75
$GPGGA,181035.576,3949.797,N,07809.854,W,0,00,,,M,,M,,*5A
$GPGLL,3949.797,N,07809.854,W,181036.576,V*39
$GPRMC,181037.576,V,4040.018,N,07808.022,W,32.9,16.43,250915,,E*77
$GPGGA,181038.576,4040.018,N,07808.022,W,0,00,,,M,,M,,*58
$GPGLL,4040.018,N,07808.022,W,181039.576,V*39
$GPRMC,181040.576,V,4133.618,N,07725.034,W,96.8,44.47,250915,,E*7F"""

INPUT_FILENAME = 'test.nmea'

# open the input file in read mode
with open(INPUT_FILENAME, 'r') as input_file:
   
    nmeafile = pynmea2.NMEAFile(input_file)
    nmea_strings = nmeafile.read()
    print(nmea_strings ,' ')
    
    

