#Importing the Libraries
import datetime
import hashlib
import json
from flask import Flask,jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block( prev_hash = '0')

    def create_block(self, prev_hash):
        block = {'block_id' : len(self.chain)+1,
                  'prev_hash' : prev_hash,
                  'nonce' : 0,
                  'timestamp' : str(datetime.datetime.now()),
                  'message' : 'This is a Transaction',
                  'hash' : ''
                  }
        self.chain.append(block)
        return block
        
    def prev_block(self):
        return self.chain[-1]

    def proof_of_work(self , block):
        proof = '1'*64
        while proof[:4]!="0000":
            block['nonce']+=1
            encoded_block = json.dumps(block , sort_keys = True).encode()
            proof = hashlib.sha256(encoded_block).hexdigest()
        block['hash'] = proof
        return proof
    
    
    
    def add_message(self , block):
        message = ' This is a Transaction'
        block['message'] = message
        return message

    def is_chain_valid(self,chain):
        block_index = 1
        prev_block = self.chain[0]
        block = self.chain[block_index]
        while(block_index < len(self.chain)):
            if block['prev_hash']==prev_block['hash']:
                return True
            else:
                return False
            block_index += 1
            prev_block = block
#Creating  a web app
app = Flask(__name__)

#Creating a blockchain
blockchain = Blockchain()

#Mining a new block
@app.route('/mine_block' , methods = ['GET'])
def mine_block():
    prev_block = blockchain.prev_block()
    prev_hash = prev_block['hash']
    block = blockchain.create_block(prev_hash)
    proof = blockchain.proof_of_work(block)
    print("Congratulations,you have mined a block!")
    response = {
                 'index' : block['block_id'],
                 'timestamp' : block['timestamp'],
                 'message' : block['message'],
                 'prev_hash' : block['prev_hash'],
                 'hash' : block['hash']
                 }
    return jsonify(response) , 200

#Getting the full blockchain
@app.route('/get_chain' , methods = ['GET'])
def get_chain():
    response = {
               'blockchain' : blockchain.chain,
               'length' : len(blockchain.chain)
                }
    return jsonify(response) , 200

#Running the app
app.run(host = '0.0.0.0' , port = 5000)
