#!/usr/bin/env python

class Client:
    def __init__(self):
        self.mac = ""
        self.manuf = ""

    def setMAC(self, mac):
        self.mac = mac

    def setManuf(self, manuf):
        self.manuf = manuf

    #override toString
    def __str__(self):
        return "Client | Manuf : " + self.manuf + " | Mac: " + self.mac + "\n"

    