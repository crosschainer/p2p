from flask import Flask, send_from_directory, jsonify, request
import flask.cli
import logging
import threading
import json
import requests
from p2p.structures.peer import Peer
from p2p.structures.transaction import Transaction

class WebServer():
    def __init__(self, host, port, peers):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.peers = peers
        self.pendingTransactions = []
        self.logger = logging.getLogger(__name__)
        self.app.add_url_rule("/ping", "ping", self.ping, methods=["GET"])
        self.app.add_url_rule("/peers", "getPeers", self.peers.getAll, methods=["GET"])
        self.app.add_url_rule("/transactions/pending", "getTransactions", self.pendingTransactions, methods=["GET"])
        self.app.add_url_rule("/transactions/add", "addTransaction", self.receive_transaction, methods=["POST"])
        self.webserverThread = threading.Thread(target=self.start)
        self.webserverThread.daemon = True
        self.webserverThread.start()
        self.logger.info("Webserver thread started")
        flask.cli.show_server_banner = lambda *args: None
        logging.getLogger("werkzeug").disabled = True

    def start(self):
        self.app.run(host=self.host, port=self.port)

    def broadcast_transaction(self, transaction):
        transaction = transaction.toJson()
        if len(self.peers) == 0:
            return
        self.logger.info("Broadcasting to peers")
        for peer in self.peers.peers:
            try:
                response = requests.post("http://{}:{}/transactions/add".format(peer.host, peer.port), json=transaction)
                if response.status_code != 200:
                    self.peers.remove(peer)
            except:
                self.peers.remove(peer)

    def receive_transaction(self, transaction = None):
        if transaction is None:
            transaction = request.get_json()
        if isinstance(transaction, str):
            transaction = Transaction.fromJson(transaction)
        if transaction not in self.pendingTransactions:
            self.logger.info("Received new transaction: {}".format(transaction)) 
            self.pendingTransactions.append(transaction)
            self.broadcast_transaction(transaction)
        return "Transaction received"


    def ping(self):
        # If pinged by another node, add it to the list of peers if it's not already there
        host = flask.request.remote_addr
        port = 5000
        peer = self.peers.getByHost(host)
        if peer is None:
            self.peers.add(Peer(host, port))
        return "pong"