import threading
import logging
import argparse
import requests
from p2p.webserver import WebServer
from p2p.structures.peers import Peers
from p2p.chain.blockchain import Blockchain
from p2p.structures.transaction import Transaction

class P2P():
    def __init__(self, host, port, bootnode=None, new_chain=False):
        self.host = host
        self.port = port
        self.peers = Peers(bootnode, host, port)
        self.webserver = WebServer(self.host, self.port, self.peers)
        self.blockchain = Blockchain(new_chain)

def get_my_public_ip():
    req = requests.get("https://api.ipify.org?format=json")
    return req.json()["ip"]

def boot():
    parser = argparse.ArgumentParser(description="P2P Network")
    parser.add_argument("--bootnode", required=False, help="Bootnode address", type=str)
    parser.add_argument("--new-chain", required=False, help="Start a new chain", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    host = get_my_public_ip()
    if args.bootnode is None:
        logging.info("No bootnode specified, starting new network")
        p2p = P2P(host, 5000, None, args.new_chain)
    else:
        p2p = P2P(host, 5000, args.bootnode)
    # User input loop
    while True:
        command = input()
        if command == "peers":
            print(p2p.peers.getAll())
        elif command == "pending_tx":
            print(p2p.webserver.pendingTransactions)
        elif command == "create_tx":
            sender = input("Sender: ")
            amount = input("Amount: ")
            receiver = input("Receiver: ")
            p2p.webserver.receive_transaction(Transaction(sender, receiver, amount))
        else:
            print("Invalid command")

if __name__ == "__main__":
    boot()