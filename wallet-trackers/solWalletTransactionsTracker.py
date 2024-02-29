import requests
from future.moves import configparser

class SOLTracker:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.api_token = config.get("SOL", "token")

    def get_wallet_transactions(self, wallet_address):
        url = 'https://pro-api.solscan.io/v1.0/account/transactions?account={}&limit=10'.format(wallet_address)
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.api_token
        }
        results = requests.get(url, headers=headers)
        data = results.json()
        print(data)
        transactions = data['result']
        return transactions
    

print(SOLTracker().get_wallet_transactions(wallet_address='AELKuZXRnxSHCFQ52aR87xYVqRbrB471GsgH66hDtghM'))