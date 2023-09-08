import json
import os
import sys
import logging

class Blockchain:
    def __init__(self, new_chain=False):
        # We dont want to store in memory or are we crazy?
        self.logger = logging.getLogger(__name__)
        self.blocks_dir = os.path.dirname(os.path.realpath(__file__)) + "/blocks/"
        self.logger.info("Blocks directory set to: " + self.blocks_dir)
        self.difficulty = 2 # Number of leading zeroes in hash of block, we'll change this to reach a 10 minute block time dynamically
        
        if new_chain:
            self.createGenesisBlock()

    def createGenesisBlock(self):
        pass

    def addBlock(self, block):
        pass

    def getLastBlock(self):
        pass

    def getBlockByHash(self, hash):
        pass

    def getBlockByIndex(self, index):
        pass

