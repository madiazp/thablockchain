import rsa
import hashlib
from base64 import b64encode, b64decode
import requests, os, json, urllib
#pubkey, privkey = rsa.newkeys(512)

class Wallet():

    def __init__(self):
        self.server = 'http://127.0.0.1:5001'
        self.db = self.update_chain()
        self.priv, self.pub = self.get_addr()
        self.addr = self.hh(str(self.pub.n).encode('utf-8'))
        #self.utxo = self.search_utxo()

    def update_chain(self):


        os.environ['NO_PROXY'] = 'localhost'
        resp = requests.get("{serv}/chain".format(serv=self.server))
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
        return  my_money

    def my_coins(self):
        my_money=[]
        for k in self.db:
            for h in k['tx']:
                try:
                    for j in h['output_list']:
                        if h['output_list'][j]['addr'] == self.addr:
                            my_money.append([h['output_list'][j]['tx'],h['output_list'][j]['value'],h['output_list'][j]['n']])
                            #print("mi moneda: {coin}".format(coin=h['output_list'][j]['tx']))

                except:
                    print('no output_list')
        return  my_money

    def make_trans(self, amount, dest):
        money = self.get_funds()
        money = sorted(money, key=lambda m: m[1])
        cand = []
        valid = dest.encode('utf-8')
        sign = b64encode(rsa.sign(valid, self.priv,"SHA-256"))
        scr_i = {'pub_n': self.pub.n,'pub_e': self.pub.e, 'sign': sign}
        funds,h = 0,0
        input_form={}
        for i in money:
            funds += i[1]
            next_input = self.putify(i[0],i[1],i[2],dest,scr_i)
            input_form.update({str(h): next_input})
            if funds > amount:
                break

        if funds < amount :
            print("no tienes suficiente saldo")
            return 0
        change= funds - amount
        output_form = {
        "0": self.putify(0,amount,0,dest,"default"),
        "1": self.putify(0,change,0,self.addr,"default")
        }
        trans_form = {
                    "input_form": input_form,
                    "output_form": output_form
                    }
        #req = urllib.request.Request("{serv}/transactions/new".format(serv=self.server))
        head ={'Content-Type': 'application/json'}
        #return trans_form.encode('utf-8')
        response = requests.post(self.server + "/transactions/new",headers = head, json =trans_form)
        return response

    @staticmethod
    def get_addr():
        with open('key.pem', mode='rb') as privatefile:
                 keydata = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(keydata)
        with open('public.pem', mode='rb') as pubfile:
                 keydatap = pubfile.read()
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(keydatap)
        return privkey, pubkey
    @staticmethod
    def putify(tx,amt,n,addr,scr):
        tx_input = {
            "tx": tx,
            "value": amt,
            "n":n ,
            "addr": addr,
            "script": scr
        }
        return tx_input
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
