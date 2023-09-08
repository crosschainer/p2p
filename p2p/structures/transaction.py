import json
import time
import hashlib

class Transaction():
    def __init__(self, sender, receiver, amount, timestamp=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.sender) + str(self.receiver) + str(self.amount) + str(self.timestamp)).encode()).hexdigest()

    def __str__(self):
        return "Transaction: " + self.hash

    def __eq__(self, other):
        return self.hash == other.hash

    def toJson(self):
        data = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.hash
        }
        return json.dumps(data)

    @staticmethod
    def fromJson(json_str):
        data = json.loads(json_str)
        transaction = Transaction(data["sender"], data["receiver"], data["amount"])
        return transaction
    