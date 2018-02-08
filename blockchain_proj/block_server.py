from blockchain import *
from uuid import uuid4
from flask import Flask, jsonify, request, current_app

thatBC= Blocky()

# Instantiate our Node
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

@app.route('/mine', methods=['GET'])
def mine():


    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    thatBC.transaction("1",node_identifier,1)

    # Forge the new Block by adding it to the chain
    thatBC.prev_hash = thatBC.chain[-1]["hash"]
    block = thatBC.next_block()
    response = {
        'message': "Nuevo bloque minado",
        'index': block['index'],
        'transactions': block['tx'],
        'nonce': block['nonce'],
        'previous_hash': block['prev_hash'],
        'hash': block['hash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = thatBC.transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': 'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': thatBC.chain,
        'length': len(thatBC.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:

        thatBC.node_registry(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(thatBC.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():

    replaced = thatBC.resolv()
    if replaced:
        print("entre csm!!")
        response = {
            'message': 'Our chain was replaced',
            'new_chain': thatBC.chain
            }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': thatBC.chain
            }
    with app.app_context():
        return jsonify(response), 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=True)
