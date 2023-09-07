import threading
import logging
import argparse
from p2p.webserver import WebServer
from p2p.structures.peers import Peers

class P2P():
    def __init__(self, host, port, bootnode=None):
        self.host = host
        self.port = port
        self.peers = Peers(bootnode)
        self.webserver = WebServer(self.host, self.port, self.peers)

def boot():
    parser = argparse.ArgumentParser(description="P2P Network")
    parser.add_argument("--bootnode", required=False, help="Bootnode address", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.bootnode is None:
        logging.info("No bootnode specified, starting new network")
        p2p = P2P("0.0.0.0", 5000)
    else:
        p2p = P2P("0.0.0.0", 5000, args.bootnode)
    # User input loop
    while True:
        command = input("Enter a command: ")
        if command == "peers":
            print(p2p.peers.getAll())
        else:
            print("Invalid command")

if __name__ == "__main__":
    boot()