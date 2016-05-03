# NMEA to CSV and KML using python
EX2 is a project that focus on detailed and accurate planning of library program.  working with Python and test the program on Benchmark.

In this project we created a system that allows us to convert NMEA files log into CSV and KML files in python.
the system allows :
upload NMEA files , select and filter data from the NMEA log file and choosing which file to enter in the database.

[[EX2 pdf link]](http://moodlearn.ariel.ac.il/pluginfile.php/1003605/mod_assign/introattachment/0/Ex2_V0.0.pdf?forcedownload=1)
# Overview

###NMEA-"The National Marine Electronics Association"
The National Marine Electronics Association (NMEA) has developed a specification that defines the interface between various pieces of marine electronic equipment. The standard permits marine electronics to send information to computers and to other marine equipment. A full copy of this standard is available for purchase at their web site. None of the information on this site comes from this standard and I do not have a copy. Anyone attempting to design anything to this standard should obtain an official copy.

GPS receiver communication is defined within this specification. Most computer programs that provide real time position information understand and expect data to be in NMEA format. This data includes the complete PVT (position, velocity, time) solution computed by the GPS receiver. The idea of NMEA is to send a line of data called a sentence that is totally self contained and independent from other sentences. There are standard sentences for each device category and there is also the ability to define proprietary sentences for use by the individual company. All of the standard sentences have a two letter prefix that defines the device that uses that sentence type. (For gps receivers the prefix is GP.) which is followed by a three letter sequence that defines the sentence contents. In addition NMEA permits hardware manufactures to define their own proprietary sentences for whatever purpose they see fit. All proprietary sentences begin with the letter P and are followed with 3 letters that identifies the manufacturer controlling that sentence. For example a Garmin sentence would start with PGRM and Magellan would begin with PMGN.



#####FreeNMEA:
Using FreeNMEA tool we can parse online NMEA log, and extract different information from NMEA sentences. 
Supported NMEA message types: RMC, GGA, GLL, FSA, GSV, VTG, ZDA, VHW, VBW


#####SatGen NMEA:
is a free GPS Simulation software from Racelogic that allows you to create and generate real-time NMEA serial streams.
SatGen NMEA allows you to use the software to stream synthesised NMEA data into your target device, replacing the serial output from a GPS engine.You can create a driving/flying scenario anywhere in the world, at any height, and at any speed, and test your device with realistic data.
It is easy to create NMEA data by sketching out a route anywhere in the world in Google Earth, and then importing the Google Earth KML file into the SatGen software. The software will then turn your rough sketch into a fully realistic journey, filling in any gaps and smoothing out any sharp corners.


#####VisualGPS:
VisualGPS Its purpose is to display graphically specific NMEA 0183 sentences and show the effects of selective availability 
Features:
           Azimuth and Elevation Graph - View all satellites that are in view. Each satellite identifies its pseudo random number (PRN) and its azimuth and elevation. Also plot and print  the physical mask angle.
           Survey - The survey window displays both position and xDOP (HDOP and VDOP) parameters. The ability for user selectable HDOP/VDOP color thresholds for position averaging make a great utility. Also monitor Standard Deviation and effects of Selective Availability. That's not all - print the results graphically.
           Signal Quality/SNR Window - Monitor satellite signal to noise ratios and see them graphically on the screen. The signal quality window will grow or shrink to accommodate number of satellites in view
           Navigation - Monitor latitude, longitude and altitude
		NMEA Command Monitor - View NMEA sentences as they are received

### the system:
The system allows us to uload NMEA files converting them into CSV and/or KML files and saving them into a database.

##Resources:
http://deanandara.com/Argonaut/Sensors/Gps/Scripts.html
http://www.labsat.co.uk/index.php/en/free-gps-nmea-simulator-software
http://www.visualgps.net/visualgps/
http://freenmea.net/decoder

## Authors:
* Raphael Zanzouri
* Tamir Arie
* Almog Avital
