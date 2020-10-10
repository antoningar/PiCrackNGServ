#!/usr/bin/env python

class Network:
    def __init__(self, essid, bssid, channel, encryption):
        self.essid = essid
        self.bssid = bssid
        self.channel = channel
        self.encryption = encryption


    #override toString
    def __str__(self):
        return "Network | ESSID: " + self.essid + " | BSSID: " + self.bssid + " | Channel: " + self.channel + " | Encryption: " + self.encryption + "\n"

    