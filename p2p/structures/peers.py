import json
import threading
import logging
import requests
import random
from p2p.structures.peer import Peer


class Peers():
    def __init__(self, bootnode=None):
        self.peers = []
        if bootnode is not None:
            self.add(bootnode)
        self.logger = logging.getLogger(__name__)

        # Check availability of peers every 5 seconds
        self.checkAvailabilityThread = threading.Thread(target=self.checkAvailability)
        self.checkAvailabilityThread.daemon = True
        self.checkAvailabilityThread.start()
        self.logger.info("Check availability thread started")

        # Discover peers every 5 seconds
        self.discoverPeersThread = threading.Thread(target=self.discoverPeers)
        self.discoverPeersThread.daemon = True
        self.discoverPeersThread.start()
        self.logger.info("Discover peers thread started")

    def __getitem__(self, index):
        return self.peers[index]

    def __setitem__(self, index, value):
        self.peers[index] = value

    def __len__(self):
        return len(self.peers)

    def __str__(self):
        return str(self.peers)

    def __eq__(self, other):
        return self.peers == other.peers

    def add(self, peer):
        peer = Peer.fromJson(peer)
        if peer in self.peers:
            return
        self.peers.append(peer)

    def remove(self, peer):
        self.peers.remove(peer)

    def get(self, index):
        return self.peers[index]

    def getAll(self):
        return self.peers

    def getByHost(self, host):
        for peer in self.peers:
            if peer.host == host:
                return peer
        return None

    def getRandom(self):
        if len(self.peers) == 0:
            return None
        return random.choice(self.peers)

    def checkAvailability(self):
        randomPeer = self.getRandom()
        if randomPeer is None:
            return
        if randomPeer.checkAvailability() is False:
            self.remove(randomPeer)

    def discoverPeers(self):
        randomPeer = self.getRandom()
        if randomPeer is None:
            return
        try:
            response = requests.get("http://{}:{}/peers".format(randomPeer.host, randomPeer.port))
            if response.status_code == 200:
                data = json.loads(response.text)
                for peer in data["peers"]:
                    self.add(peer)
        except requests.exceptions.ConnectionError:
            return


    def toJson(self):
        data = {
            "peers": [peer.toJson() for peer in self.peers]
        }
        return json.dumps(data)

    @staticmethod
    def fromJson(json):
        data = json.loads(json)
        peers = Peers()
        for peer in data["peers"]:
            peers.add(Peer.fromJson(peer))
        return peers