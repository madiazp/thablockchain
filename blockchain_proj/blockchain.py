import hashlib, json, sys
from flask import Flask, jsonify, request
from urllib.parse import urlparse
from time import time
import requests, os
app = Flask(__name__)

class Blocky():

    def __init__(self):
        self.chain = []
        self.current = []
        self.nodes = set()
        if len(self.chain) == 0:
            self.prev_hash=0
            self.prev_nonce=0
            self.current.append({
                "sender":"conejin",
                "recipient":"1",
                "amount": 100
                })
            self.next_block()



    def next_block(self):
        ind=len(self.chain)+1
        next_preblock = self.preblockify(ind,time(),self.current, self.prev_hash,self.prev_nonce)
        block_hash,nonce= self.hashing(next_preblock)
        block=next_preblock
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
            print(l_block)
            print(blk)
            print("\n ----------------- \n")
            ind=l_block["index"]
            tim=l_block["time"]
            txx=l_block["tx"]
            ph=l_block["prev_hash"]
            pno=l_block["prev_nonce"]

            pl_block = self.preblockify(ind,tim,txx,ph,pno)
            print(pl_block)
            l_hash, l_nonce = self.hashing(pl_block)
            print("\n--------------\n")
            print(l_hash)
            print(l_nonce)
            print(blk["prev_hash"])
            print(blk["prev_nonce"])
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

        print(near_nodes)
        for nod in near_nodes:

            with app.app_context():
                urls= 'http://{nodef}/chain'.format(nodef=nod)

                os.environ['NO_PROXY'] = 'localhost'
                response = requests.get(urls)
                #response = request.form.get()


            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

            self.validation_b(chain)
            if length >  m_lenght  and self.validation_b(chain):
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
    @staticmethod
    def preblockify(ind,tim,txx,ph,pn):
        preblocked= {"index":ind,
                "time": tim,
                "tx": txx,
                "prev_hash": ph,
                "prev_nonce": pn
            }
        return preblocked
