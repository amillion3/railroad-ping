import csv
import time, datetime
import urllib2
import xml.etree.ElementTree as ET
import logging

print "hello"

def main_query():

    myKey="INSERT YOUR GOOGLE MAPS API KEY HERE"
    myOriginLat=35.827583  ##SAMPLE POINT
    myOriginLong=-86.394047  ##SAMPLE POINT
    myDestLat=35.827360  ##SAMPLE POINT
    myDestLong=-86.391940  ##SAMPLE POINT
    url = "blank"


    url = "https://maps.googleapis.com/maps/api/distancematrix/xml?units=imperial&origins=" + str(myOriginLat) + "," + str(myOriginLong) + "&destinations=" + str(myDestLat) + "," + str(myDestLong) + "&key=" + myKey + "&departure_time=now"
    print url

    #begin Google Maps Distance Matrix API Ping
    ## import XML and save it out
    ##url = "https://maps.googleapis.com/maps/api/distancematrix/xml?units=imperial&origins=&destinations=&key=&departure_time=now"
    s = urllib2.urlopen(url)
    contents = s.read()
    file = open('export.xml', 'w')   #this export.xml will be saved locally & overwritten each time
    file.write(contents)
    file.close()

    ## extracts distance & duration from XML
    element_tree = ET.parse("export.xml")
    root = element_tree.getroot()
    durationSeconds = root.find('.//duration/value').text
    distanceFeet = root.find('.//distance/value').text
    durationMinutes = root.find('.//duration/text').text
    distanceMiles = root.find('.//distance/text').text
    durationInTrafficSeconds = root.find('.//duration_in_traffic/value').text
    durationInTrafficMinutes = root.find('.//duration_in_traffic/text').text

    print "XML Read complete, current travel time is " + str(durationInTrafficSeconds) + " seconds" + "  or  " + str(durationInTrafficMinutes)

    if float(durationInTrafficSeconds) >= (float(durationSeconds) * 1.30):    #if the travel time WITH traffic is greater than 30% difference than the average time, write to CSV
        print "Write to CSV"
        fd = open('record.csv','a')   # open CSV in append mode only
        fd.write('\n')
        fd.write(time.strftime('%Y-%m-%d %H:%M:%S') + ',' + str(i+1) + ',significant change,')   #timestamp
        fd.write(durationSeconds + ',' + durationMinutes + ',' + distanceFeet + ',' + distanceMiles + ',' +  durationInTrafficSeconds + ',' +  durationInTrafficMinutes)
        fd.close()
    else:
        print "Not enough change"
        fd = open('record.csv','a')   # open CSV in append mode only
        fd.write('\n')
        fd.write(time.strftime('%Y-%m-%d %H:%M:%S') + ',' + str(i+1) + ',normal,')   #timestamp
        fd.write(durationSeconds + ',' + durationMinutes + ',' + distanceFeet + ',' + distanceMiles + ',' +  durationInTrafficSeconds + ',' +  durationInTrafficMinutes)
        fd.close()
        # writes to CSV for tracking/logging purposes

    ## Final message of completion, output to terminal
    currentTimestamp = str(datetime.datetime.now() )    # converts current date/time to string
    print "Completed at: " +  currentTimestamp  # end Google Maps Distance Matrix API Ping

main_query()
