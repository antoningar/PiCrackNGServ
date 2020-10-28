#!/usr/bin/env python

import csv
import codecs
import Network

#parse csv
#NEE TOO CHECK WPA
def parseCSV(file):
    print("%------Parsing " + file + "------%")
    try:
        with open(file,'r') as csvfile:
            CSVreader = csv.reader((x.replace('\0', '') for x in csvfile), delimiter=';')
            networks = []
            header = True
            for row in CSVreader:
                if header:
                    essidIndex, bssidIndex, channelIndex, encryptionId = getHeaderIndex(row)
                    header = False
                else:
                    network = Network.Network(row[essidIndex],row[bssidIndex],row[channelIndex],row[encryptionId])
                    networks.append(network)
    except IOError:
        print(" Can't open file %s",file)
        raise
    except csv.Error as e:
        print(" Can't read %s, line %s : %s", (file,CSVreader.line_num,e))
        raise

    return networks

#index of headers into csv
def getHeaderIndex(row):
    i = 0
    for value in row:
        if(value == "ESSID"):
            essidIndex = i
        if(value == "BSSID"):
            bssidIndex = i
        if(value == "Channel"):
            channelIndex = i
        if(value == "Encryption"):
            encryptionIndex = i
        i+=1
    return essidIndex,bssidIndex,channelIndex,encryptionIndex

def main():
    networks = parseCSV("airodump-01.kismet.csv")
    for n in networks:
        print(n)

if __name__ == "__main__":
    main()