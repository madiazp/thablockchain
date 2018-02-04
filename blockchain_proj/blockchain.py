import hashlib, json, sys
from flask import Flask, jsonify, request
from urlparse import urlparse
from time import time


class Blocky():

    def __init__(self):
        self.chain = []
        self.current = []
        self.nodes = set()
        if len(self.chain) == 0:
            self.first_block()

    def first_block(self):
        self.prev_hash=0
        self.prev_nonce=0
        self.current.append({
            "sender":"conejin",
            "recipient":"1",
            "amount": 100
        })
        self.chain.append({
        "index": 1,
        "time": time(),
        "tx":self.current,
        "prev_hash": 0,
        "hash": 0000,
        "nonce": 0
        })

    def next_preblock(self):
        preblock= {"index": len(self.chain)+1,
                "time": time(),
                "tx": self.current,
                "prev_hash": self.prev_hash,
                "prev_nonce": self.prev_nonce
                }
        return preblock

    def next_block(self):
        block_hash,nonce= self.hashing(self.next_preblock())
        block=self.next_preblock()
        block.update(
        {"hash": block_hash,
        "nonce": nonce
        })
        self.prev_hash = block_hash
        self.prev_nonce = nonce
        self.chain.append(block)
        self.current = []
        return block

    def transaction(self, tx_addr, rx_addr, amount):
        self.current.append({
            "sender": tx_addr,
            "recipient": rx_addr,
            "amount": amount
        })
    def node_registry(self, addr):
        parsed_url = urlparse(addr)
        self.nodes.add(parsed_url.netloc)


    def validation_b(self, chain):
        l_block = chain[0]
        current_index=1
        while current_index < len(chain):
            blk= chain[current_index]
            print l_block
            print blk
            print "\n ----------------- \n"
            l_hash, l_nonce = self.hashing(l_block)

            if blk['prev_hash'] != l_hash:
                return False
            if blk['prev_nonce'] != l_nonce:
                return False

            l_block = blk
            current_index += 1
        return True

    def resolv(self):
        near_nodes = self.nodes
        new_chain = None
        m_lenght = len(self.chain)


        for nod in near_nodes:

            response = request.args.get('http://{nodef}/chain'.format(nodef=nod))
            print response
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

            if length >  m_lenght and self.validation_b(chain):
                m_lenght = length
                new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True

    @staticmethod
    def hashing(ablock):
        jblock=json.dumps(ablock,sort_keys=True).encode()
        nonce=0
        guess = hashlib.sha256(jblock*nonce).hexdigest()
        while (guess[:2] == "00") is False :
            nonce += 1
            guess = hashlib.sha256(jblock*nonce).hexdigest()
        return guess,nonce
