#!/usr/bin/env python

import Client
import logging
import xml.etree.ElementTree as ET

def getClientMac(file):
    print("%------Reading " + file + "------%")
    logging.info(" [READING] %s",file)
    clients = []
    wireless_client = ''
    try:
        wireless_network = ET.parse(file).getroot()[0]
        for cn in wireless_network:
            if cn.tag == "wireless-client":
                wireless_client = cn
        if wireless_client != '':
            for cc in wireless_client:
                client = Client.Client()
                if cc.tag == "client-mac":
                    client.setMAC(cc.text)
                elif cc.tag == "client-manuf":
                    client.setManuf(cc.text)
                    logging.info("Client find : %s",client)
                    clients.append(client)
            return clients
    except ET.ParseError as err:
        logging.error("Error when parsing XML : %s", err)
        raise
    except FileNotFoundError as err:
        logging.error("Can't find file : %s", file)
        raise
    logging.info(" No devices connected on network.")
    print("No devices connected on network.")
    return -1