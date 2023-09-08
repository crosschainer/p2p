import time
import hashlib
import logging

class Block():

    def __init__(self, index, previous_hash, data=None):
        self.logger = logging.getLogger(__name__)
        self.index = index
        self.timestamp = None # We'll set this later when mining
        self.data = data # If no transactions, data is None. We still create blocks for mining rewards.
        self.previous_hash = previous_hash
        self.nonce = None # We'll set this later when mining
        self.hash = None # We'll set this later when mining
        self.miner = None # We'll set this later when mining and we know who mined it
        
    def calculateHash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode("utf-8")).hexdigest()

    def mineBlock(self, difficulty):
        # Proof of work that doesnt rely on leading zeros in hash but instead on the amount of zeros in general so we can change difficulty more accurately
        while self.hash is None:
            # Calculate hash

            mine_hash = self.calculateHash()
            # Get amount of zeros in hash
            zeros = 0
            for char in self.hash:
                if char == "0":
                    zeros += 1
                else:
                    break

            # If amount of zeros is less than difficulty, increment nonce and try again
            if zeros < difficulty:
                self.nonce += 1

            # If amount of zeros is equal to difficulty, we have a valid hash
            elif zeros == difficulty:
                self.hash = mine_hash
                self.timestamp = int(time.time())
                self.nonce = self.nonce
        
        self.logger.info("Mined block: " + self.hash)
        return self.hash

