from web3 import Web3
import requests
from termcolor import cprint
import time
import json
import random

gasLimit = 124000

def zorb(privatekey):

    def mint():

        try:
            RPC = "https://eth-mainnet.g.alchemy.com/v2/m7jct_e0_RFwpmnTcHiOdV8SfWk-288Z"

            web3 = Web3(Web3.HTTPProvider(RPC))
            account = web3.eth.account.privateKeyToAccount(privatekey)
            address_wallet = account.address
            contractToken = Web3.toChecksumAddress('0x7492e30d60d96c58ed0f0dc2fe536098c620c4c0')
            ABI = '[{"inputs":[{"internalType":"address","name":"_logic","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"stateMutability":"payable","type":"receive"},{"name": "purchase","type": "function","payable":true,"inputs": [{"type": "uint256"}]}]'
            contract = web3.eth.contract(address=contractToken, abi=ABI)

            nonce = web3.eth.get_transaction_count(address_wallet)

            contract_txn = contract.functions.purchase(1).buildTransaction({
                'from': address_wallet,
                'gas': gasLimit,
                'nonce': nonce,
            })

            signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=privatekey)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

            cprint(f'\n>>> https://etherscan.io/tx/{web3.toHex(tx_hash)}', 'green')
        except Exception as error:
            cprint(f'\n>>> {error}', 'red')

    mint()
    time.sleep(random.randint(2,4))

if __name__ == "__main__":

    with open("private_keys.txt", "r") as f:
        keys_list = [row.strip() for row in f]

    for privatekey in keys_list:
        zorb(privatekey)