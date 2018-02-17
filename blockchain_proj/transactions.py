import rsa, hashlib, sys
import json

class Transy():

    def __init__(self, chain):
        self.tx_hist = []
        self.db = chain

    def make_fee(self, output_form):
        entry= {
            "output_list":{
            },
            "out_count":1
        }
        amt,addr,scr = output_form
        entry.update({"output_list":{
            "0": self.putify(0,amt,0,addr,scr)
            }})
        entry.update({"tx":len(self.tx_hist)+1})
        entry.update({"hash": self.hashify(entry)})
        entry["output_list"]["0"].update({"tx": entry["hash"]})
        self.tx_hist.append(entry)
        return entry

    def make_entry(self, input_form, output_form):

        if self.invalid_entry(input_form,output_form):
            return False, {}
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
                str(k): self.putify(vali[0],vali[1],vali[2],vali[3],vali[4])
                })

            k+=1

        for valo in output_form:
            entry["output_list"].update({
                str(l): self.putify(0,valo[1],valo[2],valo[3],valo[4])
                })
            l+=1

        entry.update({"tx":len(self.tx_hist)+1})
        entry.update({"hash":self.hashify(entry)})

        for x in entry["output_list"]:

            entry["output_list"][x]["tx"] = entry["hash"]
        j=1
        for utxi in input_form:
            j += 1
            entry.update({"UTXO":{
                str(j):{
                    "addr":utxi[3],
                    "tx_id": utxi[0],
                    "n": utxi[2],
                    "spent": True
                    }
            }})
        self.tx_hist.append(entry)
        return True,entry


    def invalid_entry(self,input_form,output_form):
            in_count=0
            out_count=0
            for i in input_form:
                in_count += i[1]
            for j in output_form:
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
        k=0

        for chn in self.db:

            try:
                print("si hay utxo")
                print(idtx)
                for i in self.db[k]["tx"]:
                    utx = i["UTXO"]
                    for keys in utx:
                        print(utx[keys]["tx_id"])
                        if utx[keys]["tx_id"] == idtx and utx[keys]["n"] == ntx and utx[keys]["spent"]:
                            return True

            except:
                print("no hay UTXO")

            k +=1

                #if ent["tx_id"] == idtx and ent["n"] == ntx and ent["spent"]:
                    #return True
            print("\n")
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
