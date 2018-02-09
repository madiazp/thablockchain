import rsa, hashlib, sys
import json

class Transy():

    def __init__(self):
        self.tx_hist = []
        if len(self.tx_hist) == 0:
            self.coinbase()


    def make_trans(self, input_form, output_form):

        if self.invalid_trans(input_form,output_form):
            return False
        trans= {
            "input_list":{
            },
            "in_count":len(input_form),
            "output_list":{
            },
            "out_count":len(output_form)
        }
        for vali in input_form:
            trans["input_list"].update(self.putify(vali[0],vali[1],vali[2],vali[3],True,valo[5]))
            if any(self.tx_hist)
        for valo in output_form:
            trans["output_list"].update(self.putify(valo[0].valo[1],valo[2],valo[3],False,valo[5]))
        trans["hash"].update(self.hashify(trans))
        trans["tx"].update(len(self.tx_hist)+1)
        self.tx_hist.append(trans)
        return True

    @staticmethod
    def hashify(the_data):
        jdata=json.dumps(the_data,sort_keys=True).encode()
        return hashlib.sha256(jdata).hexdigest()

    @staticmethod
    def invalid_trans(input_form,output_form):
            in_count=0
            out_count=0
            error1="pubscrip invalido"
            for i in input_form:
                int_count += i[1]
            for j in output_form
                out_count += j[0]
            if out_count > in_count:
                print("No teni tantas moneas po compadre")
                return True
            for form in output_form:
                for inst in form[3].split(""):
                    if inst == "OP_DUP":


            return False

    @staticmethod
    def putify(tx,amt,n,addr,sp,scr):
        tx_input = {
            "tx": ptx,
            "value": amt,
            "n":n ,
            "addr": addr,
            "spent":sp
            "script": scr
        }
        return tx_input

    @staticmethod
