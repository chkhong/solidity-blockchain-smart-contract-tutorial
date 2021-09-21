from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open('./SimpleStorage.sol', 'r') as file:
  simple_storage_file = file.read()

# Compile Our Solidity

compiled_sol = compile_standard(
  {
    'language': 'Solidity',
    'sources': {'SimpleStorage.sol': {'content': simple_storage_file}},
    'settings': {
      'outputSelection': {
        '*': {
          '*': ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
        }
      }
    }
  },
  solc_version="0.6.0"
)

with open('compiled_code.json', 'w') as file:
  json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# for connecting to kovan
w3 = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/8e1f69fbb54044df8f29bba49d7deab3'))
chain_id = 42
my_address = '0x064D65c7a5773BA707Fea2aB435892AA39916a3D'
private_key = os.getenv('PRIVATE_KEY')
print(private_key)

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transcation
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
  {'chainId': chain_id, 'from': my_address, 'nonce': nonce}
)
# 2. Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# 3. Send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#  Working with the contract, you always need
#  Contract Address
#  Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#  Call -> Simulate making the call and getting a return value
#  Transact -> Actually make a state change
print(simple_storage.functions.retrieve().call())
store_transaction = simple_storage.functions.store(15).buildTransaction(
  {'chainId': chain_id, 'from': my_address, 'nonce': nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrieve().call())