import json
import requests

class Peer(dict):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def checkAvailability(self):
        try:
            response = requests.get("http://{}:{}/ping".format(self.host, self.port))
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def __str__(self):
        return f"{self.host}:{self.port}"

    def __eq__(self, other):
        return self.host == other.host and self.port == other.port

    def toJson(self):
        data = {
            "host": self.host,
            "port": self.port
        }
        return json.dumps(data)

    @staticmethod
    def fromJson(json_str):
        data = json.loads(json_str)
        return Peer(data["host"], data["port"])