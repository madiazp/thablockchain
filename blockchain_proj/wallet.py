import rsa
import hashlib
from base64 import b64encode, b64decode
import requests, os
#pubkey, privkey = rsa.newkeys(512)
class Wallet():

    def __init__(self, pubkey, privkey):
        self.db = self.update_chain()
        self.addr = self.hh(str(pubkey.n).encode('utf-8'))
        self.priv = privkey
        #self.utxo = self.search_utxo()

    def update_chain(self):
        urls= 'http://127.0.0.1:5001/chain'

        os.environ['NO_PROXY'] = 'localhost'
        resp = requests.get(urls)
        return resp.json()['chain']

    def get_funds(self):

        self.db = self.update_chain()
        my_money = self.my_coins()
        spent = []
        funds = 0
        for i in self.db:
            for k in i['tx']:
                try:
                    for j in k['UTXO']:
                        for h in my_money:
                            if k['UTXO'][j]['tx_id'] == h[0]:
                                my_money.remove(h)

                except:
                    print('no utxo')
        for m in my_money:
            funds += m[1]
        print("total funds: {f}".format(f=funds))
        return funds
    def my_coins(self):
        my_money=[]
        for k in self.db:
            for h in k['tx']:
                try:
                    for j in h['output_list']:
                        if h['output_list'][j]['addr'] == self.addr:
                            my_money.append([h['output_list'][j]['tx'],h['output_list'][j]['value']])
                            #print("mi moneda: {coin}".format(coin=h['output_list'][j]['tx']))

                except:
                    print('no output_list')
        return  my_money

    @staticmethod
    def hh(msg):
        return hashlib.sha512(msg).hexdigest()


#def make_trans(pub, priv):

#sign = b64encode(rsa.sign(mesg, privkey,"SHA-256"))

#sign_script={"pub":pubkey,
#             "sign":sign
#}

#print(sign_script)

#dsign = rsa.decrypt(sign, privkey)
#print(rsa.verify(mesg,b64decode(sign),pubkey))
