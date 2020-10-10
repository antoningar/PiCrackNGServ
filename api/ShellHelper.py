#!/usr/bin/env python

import logging
import time
import os
from subprocess import Popen,PIPE

ROOT_PASSWORD = "grandmastersplinter"

def command(command):
    print("%------"+command+"------%")
    logging.info(" [COMMAND] %s",command)
    os.system(command)

#Do a command as sudo
def commandAsRoot(command):
    print("%------"+command+"------%")
    logging.info(" [COMMAND] %s",command)
    p = Popen(["sudo","-S"] + command.split(),stdin=PIPE,stdout=PIPE,stderr=PIPE,universal_newlines=True)
    r = p.communicate(ROOT_PASSWORD + "\n")
    if r[0] != '':
        logging.info(" [STDERR] %s",r[0])
    return r

#Do a command as sudo with timeout
def commandAsRootWithTimeout(command, timeout):
    print("%------"+command+"------%")
    logging.info(" [COMMAND] %s",command)
    p=Popen(["sudo","-S"] + command.split(),stdin=PIPE,stdout=PIPE,stderr=PIPE,universal_newlines=True)
    r=p.communicate(ROOT_PASSWORD + "\n")
    time.sleep(timeout)
    if r[0] != '':
        logging.info(" [STDERR] %s",r[0])
    return r

#do a normal command
def command(command):   
    p = Popen(command.split(),stdin=PIPE,stdout=PIPE,stderr=PIPE,universal_newlines=True)
    return p.communicate()

#stop monitoring
def stopInterface():
    return commandAsRoot("airmon-ng stop wlan1mon")

#rm csv,xml
def rmOutputs():
    if os.path.exists("airodump-01.kismet.csv"):
        os.remove("airodump-01.kismet.csv")
        
    if os.path.exists("./output/-01.log.csv"):
        os.remove("./output/-01.log.csv")
    if os.path.exists("./output/-01.kismet.netxml"):
        os.remove("./output/-01.kismet.netxml")
    if os.path.exists("./output/-01.kismet.csv"):
        os.remove("./output/-01.kismet.csv")
    if os.path.exists("./output/-01.csv"):
        os.remove("./output/-01.csv")
        
def rmHandshake():
    if os.path.exists("./output/-01.cap"):
        os.remove("./output/-01.cap") 

def main():
    rmOutputs()

if __name__ == "__main__":
    main()

