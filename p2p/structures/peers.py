import json
import threading
import logging
import requests
import random
import time
from p2p.structures.peer import Peer


class Peers(dict):
    def __init__(self, bootnode=None):
        self.logger = logging.getLogger(__name__)
        self.peers = []
        if bootnode is not None:
            bootnode = bootnode.split(":")
            bootnode = Peer(bootnode[0], int(bootnode[1]))
            self.add(bootnode)

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
        if isinstance(peer, str):
            peer = Peer.fromJson(peer)
        if peer in self.peers:
            return
        self.peers.append(peer)
        self.logger.info("Peer added: {}:{}".format(peer.host, peer.port))

    def remove(self, peer):
        self.peers.remove(peer)
        self.logger.info("Peer removed: {}:{}".format(peer.host, peer.port))

    def get(self, index):
        return self.peers[index]

    def getAll(self):
        return [str(peer) for peer in self.peers]

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
        while True:
            time.sleep(5)
            randomPeer = self.getRandom()
            if randomPeer is None:
                continue
            if randomPeer.checkAvailability() is False:
                self.remove(randomPeer)

    def discoverPeers(self):
        while True:
            time.sleep(5)
            randomPeer = self.getRandom()
            if randomPeer is None:
                continue
            try:
                response = requests.get("http://{}:{}/peers".format(randomPeer.host, randomPeer.port))
                if response.status_code == 200:
                    data = json.loads(response.text)
                    for peer in data:
                        host = peer.split(":")[0]
                        port = int(peer.split(":")[1])
                        self.add(Peer(host, port))
            except requests.exceptions.ConnectionError:
                continue


    def toJson(self):
        data = {
            "peers": [peer.toJson() for peer in self.peers]
        }
        return json.dumps(data)

    @staticmethod
    def fromJson(json_str):
        data = json.loads(json_str)
        peers = Peers()
        for peer in data["peers"]:
            peers.add(Peer.fromJson(peer))
        return peers