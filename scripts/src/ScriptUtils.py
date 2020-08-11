#!/usr/bin/env python

import logging
import time
from subprocess import Popen,PIPE,DEVNULL

ROOT_PASSWORD = "grandmastersplinter"

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
    return commandAsRoot("airmon-ng stop wlp2s0mon")

#rm csv,xml
def rmOutputs():
    commandAsRoot("sh ./reset.sh")