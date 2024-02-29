import requests
import datetime
from future.moves import configparser
import db_manager

class BSCTracker:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.api_token = config.get("BSC", "token")

    def get_wallet_transactions(self, wallet_address, last_block_number):
        url = 'https://api.bscscan.com/api?module=account&action=txlist&address={}&sort=desc&startblock={}&endblock=99999999'.format(wallet_address, 0 if last_block_number == None else int(last_block_number) + 1)
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_token
        }
        results = requests.get(url, headers=headers)
        data = results.json()
        if data['status'] == '0':
            return None
        elif len(data['result']) == 0:
            return 'No transactions found for this address!'
        else:
            transactions = data['result'][0]
            block_number = data['result'][0]['blockNumber']
            timestamp = int(data['result'][0]['timeStamp'])
            tx_hash = data['result'][0]['hash']
            function_name = data['result'][0]['functionName']
            block_hash = data['result'][0]['blockHash']
            tx_from = data['result'][0]['from']
            tx_to = data['result'][0]['to']
            tx_value = int(data['result'][0]['value']) / (10**18)
            tx_gas_price = ((int(data['result'][0]['gasPrice']) * (10**-9)))
            tx_gas_limit = int(data['result'][0]['gas'])
            tx_gas_used = int(data['result'][0]['gasUsed'])
            tx_fee = ((int(data['result'][0]['gasPrice']) * (10**-9)) * int(data['result'][0]['gasUsed'])) * 10**-9
            tx_status = 'Successful' if data['result'][0]['txreceipt_status'] else 'Pending or Unsuccessful'
            
            return tx_hash, block_number, datetime.datetime.utcfromtimestamp(timestamp), block_hash, tx_from, tx_to, tx_value, tx_gas_price, tx_gas_limit, tx_gas_used, tx_fee, tx_status, function_name


# block_number, timestamp, tx_hash, block_hash, tx_from, tx_to, tx_value, tx_gas_price, tx_gas_limit, tx_gas_used, tx_fee, tx_status = BSCTracker().get_wallet_transactions(wallet_address="0x2D4C407BBe49438ED859fe965b140dcF1aaB71a9")

# print(f'Time: {datetime.datetime.utcfromtimestamp(timestamp)}')
# print(f'Block Number: {block_number}')
# print(f'Block Hash: {block_hash}')
# print(f'Transaction Hash: {tx_hash}')
# print(f'From: {tx_from}')
# print(f'To: {tx_to}')
# print(f'Value: {tx_value}')
# print(f'Transaction Fee: {tx_fee} BNB')
# print(f'Transaction Gas Price: {tx_gas_price} BNB')
# print(f'Transaction Gas Limit: {tx_gas_limit}')
# print(f'Transaction Gas Used: {tx_gas_used}')
# print(f'Transaction Status: {tx_status}')