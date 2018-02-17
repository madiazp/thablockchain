#Este archivo define la clase de la blockchain
import hashlib, json, sys
from urllib.parse import urlparse
from time import time
import requests, os
from transactions import *
#definimos la clase
class Blocky():
#inicializamos la clase

    def __init__(self):
        self.chain = [] # aca deben estar todos los bloques
        self.current = [] #aca deben estar todas las transacciones por bloque
        self.nodes = set() #aca los nodos que minaran la blockchain, los peers
        self.transy = Transy(self.chain)
        if len(self.chain) == 0: # si no existe un bloque generamos uno, el bloque genesis
            self.prev_hash=0
            self.prev_nonce=0
            self.current.append({
                "sender":"conejin",
                "recipient":"1",
                "amount": 100
                })
            self.next_block()


    #el metodo que creara un nuevo bloque
    def next_block(self):
        ind=len(self.chain)+1 #avanzamos al siguiente indice, la id del bloque
        block = self.preblockify(ind,time(),self.current, self.prev_hash,self.prev_nonce) #creamos un prebloque con informacion que excluye al confirmacion del bloque
        block_hash,nonce= self.hashing(block) #minamos el prebloque generando el hash del bloque y el nonce(la prueba de trabajo)

        block.update(
        {"hash": block_hash,
        "nonce": nonce
        }) #agregamos el hash y el nonce al prebloque, generando un bloque entero minado (y confirmado al menos una vez)
        self.prev_hash = block_hash #definimos el hash previo para el siguiente bloque
        self.prev_nonce = nonce #definimos la prueba de trabajo para el siguiente bloque
        self.chain.append(block) #agregamos el bloque a la cadena de bloques
        self.transy.db = self.chain
        self.current = [] #reiniciamos las transacciones, las transacciones son unicas en cada bloque
        return block

    #metodo que agrega transacciones a un bloque , el payload del bloque
    def transaction(self, input_form, output_form, fee):
        if fee:
            TX = self.transy.make_fee(output_form)
        else:
            TX = self.transy.make_entry(input_form, output_form)

        self.current.append(TX)
        return TX
    #metodo que agrega nodos que minaran nuestra blockchain
    def node_registry(self, addr):
        parsed_url = urlparse(addr) #obtenemos la direccion de nuestro minero
        self.nodes.add(parsed_url.netloc) #agregamos la direccion de nuestro minero

    # metodo que valida la blockchain entera
    def validation_b(self, chain):
        #inicializamos en el primer bloque
        l_block = chain[0] #last block
        current_index=1  #la id del bloque actual (siguiente a l_block)
        #recorremos toda nuestra cadena de bloque
        while current_index < len(chain):
            blk= chain[current_index]
            print(l_block)
            print(blk)
            print("\n ----------------- \n")
            #recreamos el bloque previo
            ind=l_block["index"]
            tim=l_block["time"]
            txx=l_block["tx"]
            ph=l_block["prev_hash"]
            pno=l_block["prev_nonce"]

            pl_block = self.preblockify(ind,tim,txx,ph,pno)
            l_hash, l_nonce = self.hashing(pl_block)
            # si el hash previo recalculado coincide con el hash previo en el nuevo bloque entonces puede ser valido
            if blk['prev_hash'] != l_hash:
                return False
            #si el nonce previo recalculado coincide con el nonce previo en el nuevo bloque entonces verificamos el bloque
            if blk['prev_nonce'] != l_nonce:
                return False
            #pasamos al siguiente bloque previo
            l_block = blk
            #pasamos al siguiente bloque
            current_index += 1
        #si todo esta ok la cadena de bloque es valida
        return True
    #metodo de consenso, todos los mineros deben minar el mayor bloque de la red
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
