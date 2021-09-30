from brownie import SimpleStorage, accounts, config

def read_contract():
  simple_storage = SimpleStorage[-1] # get the latest deployed contract
  # ABI found in build/contracts
  # Address found in build/deployments
  print(simple_storage.retrieve())

def main():
  read_contract()