import rsa, hashlib, sys
import json

class Transy():

    def __init__(self, chain):
        self.tx_hist = []
        self.db = chain


    def make_entry(self, input_form, output_form):

        if self.invalid_entry(input_form,output_form):
            return False
        entry= {
            "input_list":{
            },
            "in_count":len(input_form),
            "output_list":{
            },
            "out_count":len(output_form)
        }
        k=0
        l=0
        for vali in input_form:
            entry["input_list"].update({
                str(k): self.putify(vali[0],vali[1],vali[2],vali[3],valo[4])
                })
            k+=1

        for valo in output_form:
            entry["output_list"].update({
                str(l): self.putify(0,valo[1],valo[2],valo[3],valo[4])
                })
            l+=1

        entry["tx"].update(len(self.tx_hist)+1)
        entry["hash"].update(self.hashify(entry))

        for x in entry["output_list"]:
            x["tx"] = entry["hash"]
        j=1
        for utxi in input_form:
            j += 1
            entry["UTXO"].add({
                str(j):{
                    "tx_id": utxi[0],
                    "n": utxi[2],
                    "spent": True
                    }
            })


        self.tx_hist.append(entry)
        return True

    def invalid_entry(self,input_form,output_form):
            in_count=0
            out_count=0
            for i in input_form:
                in_count += i[1]
            for j in output_form
                out_count += j[1]
            if out_count > in_count:
                print("No teni tantas moneas po compadre")
                return True
            self.fee = in_count - out_count
            for itx in input_form:
                if self.search_spent(itx[0],itx[2]):
                    print("{txi} ya fue gastado".format(txi=itx[0]))
                    return True

            return False

    def search_spent(self, idtx,ntx):
        for chn in self.db:
            for ent in chn:
                for utxo in ent["UTXO"]:
                    if utxo["tx_id"] == idtx and utxo["n"] == ntx and utxo["spent"]:
                        return True
        return False

    @staticmethod
    def hashify(the_data):
        jdata=json.dumps(the_data,sort_keys=True).encode()
        return hashlib.sha256(jdata).hexdigest()

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
