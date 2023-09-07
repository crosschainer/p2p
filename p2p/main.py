import threading
import logging
from p2p.webserver import WebServer
from p2p.structures.peers import Peers

class P2P():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = Peers()
        self.webserver = WebServer(self.host, self.port, self.peers)

def boot():
    logging.basicConfig(level=logging.INFO)
    p2p = P2P("0.0.0.0", 5000)
    # User input loop
    while True:
        command = input("Enter a command: ")
        if command == "peers":
            print(p2p.peers.getAll())
        else:
            print("Invalid command")

if __name__ == "__main__":
    boot()
