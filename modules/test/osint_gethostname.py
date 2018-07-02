import socket

from core.actionModule import actionModule
from core.keystore import KeyStore as kb


class scan_gethostname(actionModule):
    def __init__(self, config, display, lock):
        super(scan_gethostname, self).__init__(config, display, lock)
        self.title = "Determine the hostname for each IP"
        self.shortName = "GetHostname"
        self.description = "execute [gethostbyaddr(ip)] on each target"

        self.requirements = []
        self.triggers = ["newIP"]

        self.safeLevel = 5

    def getTargets(self):
        #get all hosts
        self.targets = kb.get('osint/ip/')

    def process(self):
        # load any targets we are interested in
        self.getTargets()

        # loop over each target
        for t in self.targets:
            # verify we have not tested this host before
            if not self.seentarget(t):
                # add the new IP to the already seen list
                self.addseentarget(t)
                self.display.verbose(self.shortName + " - Connecting to " + t)
                try:
                    results = socket.gethostbyaddr(t)
                    self.fire("newHostname")
                    kb.add('host/' + t + '/hostname/' + results[0])
                except:
                    pass

        return
