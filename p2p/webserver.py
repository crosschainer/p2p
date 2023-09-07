from flask import Flask, send_from_directory, jsonify
import flask.cli
import logging
import threading

class WebServer():
    def __init__(self, host, port, peers):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.peers = peers
        self.logger = logging.getLogger(__name__)
        self.app.add_url_rule("/ping", "ping", self.ping, methods=["GET"])
        self.app.add_url_rule("/peers/add", "addPeer", self.peers.add, methods=["POST"])
        self.app.add_url_rule("/peers", "getPeers", self.peers.getAll, methods=["GET"])
        self.webserverThread = threading.Thread(target=self.start)
        self.webserverThread.daemon = True
        self.webserverThread.start()
        self.logger.info("Webserver thread started")
        flask.cli.show_server_banner = lambda *args: None
        logging.getLogger("werkzeug").disabled = True

    def start(self):
        self.app.run(host=self.host, port=self.port)

    def ping(self):
        # If pinged by another node, add it to the list of peers if it's not already there
        host = flask.request.remote_addr
        port = 5000
        peer = self.peers.getByHost(host)
        if peer is None:
            self.peers.add(json.dumps({"host": host, "port": port}))
            self.logger.info("Peer added: {}:{}".format(host, port))
        return "pong"