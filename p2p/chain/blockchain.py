import json
import os
import sys
import logging
import threading
from p2p.chain.block import Block
import time

class Blockchain:
    def __init__(self, new_chain=False, webserver=None):
        # We dont want to store in memory or are we crazy?
        self.logger = logging.getLogger(__name__)
        self.blocks_dir = os.path.dirname(os.path.realpath(__file__)) + "/blocks/"
        if not os.path.exists(self.blocks_dir):
            os.makedirs(self.blocks_dir)

        self.last_block = None
        self.logger.info("Blocks directory set to: " + self.blocks_dir)
        self.difficulty = 1 # Number of zeroes in hash of block, we'll change this to reach a 10 minute block time dynamically
        self.webserver = webserver

        validationThread = threading.Thread(target=self.validationThread)
        validationThread.daemon = True
        validationThread.start()
        self.logger.info("Validation thread started")

        miningThread = threading.Thread(target=self.miningThread)
        miningThread.daemon = True
        miningThread.start()
        self.logger.info("Mining thread started")

        if new_chain:
            self.createGenesisBlock()

    def miningThread(self):
        while True:
            if len(self.webserver.pendingTransactions) > 0:
                mining_reward = Transaction("0", self.webserver.host, 1, int(time.time()))
                block = Block(len(self.blocks), self.blocks[-1].hash, self.webserver.pendingTransactions + [mining_reward])
                block.mineBlock(self.difficulty)
                self.webserver.broadcast_new_block(block)
                self.validateBlock(block)

    def validationThread(self):
        while True:
            time.sleep(1)
            if len(self.webserver.pendingBlocks) > 0:
                block = self.webserver.pendingBlocks.pop()
                self.validateBlock(block)

    def createGenesisBlock(self):
        self.logger.info("Creating genesis block")
        genesis_block = Block(0, "0", [])
        genesis_block.mineBlock(self.difficulty)
        with open(self.blocks_dir + "0.json", "w") as f:
            f.write(genesis_block.toJson())

    def addBlock(self, block):
        self.logger.info("Adding block: {}".format(block))
        with open(self.blocks_dir + str(block.index) + ".json", "w") as f:
            f.write(block.toJson())
        self.logger.info("Emptying pending transactions")
        for transaction in block.data:
            self.webserver.pendingTransactions.remove(transaction)
        self.last_block = block

    def getLastBlock(self):
        if self.last_block is None:
            blocks_dir = os.listdir(self.blocks_dir)
            blocks_dir.sort()
            with open(self.blocks_dir + blocks_dir[-1], "r") as f:
                self.last_block = Block.fromJson(f.read())
        return self.last_block

    def getBlockByIndex(self, index):
        with open(self.blocks_dir + str(index) + ".json", "r") as f:
            return Block.fromJson(f.read())

    def validateBlock(self, block):
        self.logger.info("Validating new block: {}".format(block))
        if isinstance(block, str):
            block = Block.fromJson(block)
        if block.index != len(self.blocks):
            self.logger.error("Block index is not correct")
            return False
        if block.previous_hash != self.blocks[-1].hash:
            self.logger.error("Block previous hash is not correct")
            return False
        if block.calculateHash() != block.hash:
            self.logger.error("Block hash is not correct")
            return False
        if block.hash[:self.difficulty] != "0" * self.difficulty:
            self.logger.error("Block hash does not meet difficulty requirements")
            return False
        self.addBlock(block)
        return True

