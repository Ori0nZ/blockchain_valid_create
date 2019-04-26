#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:48:16 2019

@author: infosec
"""
# install Flask= 0.22.2
# install postman
#import library
import datetime
import hashlib
import json
from flask import Flask,jsonify
# class Blockchain
class Blockchain:
    def __init__(self):
        self.chain=[]
        #create block 
        self.create_block(proof = 1 , previous_hash= '0')
    def create_block(self, proof, previous_hash):
        block = {
                'index': len(self.chain), 
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash
                }
        self.chain.append(block)
        return block
    def get_prevlock(self):
        return self.chain[-1]
    # check value to make new block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_block = False
        while check_block is False:
            hash_str = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            #need 8 digest 0 to valid
            if(hash_str[:5]=='00000'):
                check_block = True
            else:
                new_proof +=1
        return new_proof
    def hash(self, block):
        encode_block = json.dumps(block , sort_keys = True ).encode()
        return hashlib.sha256(encode_block).hexdigest()
    def is_valid_block(self, chain):
        previous_block = chain[0]
        index_block = 1
        while index_block < len(chain):
            block = chain[index_block]
            #check the privious hash is valid = hash(block)
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            #check the proof is valid
            hash_str = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if(hash_str[:4]!='0000'):
                return False
            previous_block = block
            index_block += 1
        return True
    
#Part 2: Mining the block chain
#Flask sreate app name
app = Flask(__name__)
blockchain = Blockchain()
@app.route("/", methods=['GET'])
#mine new block 
#jonify make a json ouput sources
#200 OK http response

def mine_block():
    prevblock = blockchain.get_prevlock()
    proof = blockchain.proof_of_work(prevblock['proof'])#need proof_block
    previous_hash = blockchain.hash(prevblock)
    block = blockchain.create_block(proof, previous_hash)
    response = { 'messange': "Congatitation! Success",
                'index': block['index'], 
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
            }
    return jsonify(response),200

#getting the full blockchain
@app.route("/chain", methods=['GET'])
def get_chain():
    response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)}
    return jsonify(response), 200
# Running the app
@app.route("/check", methods=['GET'])
def check_chain():
        result =  blockchain.is_valid_block(blockchain.chain)
        if result:
            response = {'messenge': "All right. the blockchain is valid"}
        else:
            response = {'messenge': "Not Success"}
        return jsonify(response), 200
#Run appp postman http://127.0.0.1:5000/chain
app.run(host='0.0.0.0', port=5000)















































    
        
        
       