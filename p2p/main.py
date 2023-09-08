import threading
import logging
import argparse
from p2p.webserver import WebServer
from p2p.structures.peers import Peers

class P2P():
    def __init__(self, host, port, bootnode=None):
        self.host = host
        self.port = port
        self.peers = Peers(bootnode, host, port)
        self.webserver = WebServer(self.host, self.port, self.peers)

def get_my_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json()["ip"]
    except:
        return None

def boot():
    parser = argparse.ArgumentParser(description="P2P Network")
    parser.add_argument("--bootnode", required=False, help="Bootnode address", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.bootnode is None:
        logging.info("No bootnode specified, starting new network")
        p2p = P2P(get_my_public_ip(), 5000)
    else:
        p2p = P2P(get_my_public_ip(), 5000, args.bootnode)
    # User input loop
    while True:
        command = input()
        if command == "peers":
            print(p2p.peers.getAll())
        else:
            print("Invalid command")

if __name__ == "__main__":
    boot()