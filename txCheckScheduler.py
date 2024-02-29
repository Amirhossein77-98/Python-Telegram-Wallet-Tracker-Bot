import sys
sys.path.insert(0, 'wallet-trackers')
import ethWalletTransactionsTracker, bscWalletTransactionsTracker
import db_manager
from telegram.constants import ParseMode

async def check_transactions(context):
        ETHtracker = ethWalletTransactionsTracker.ETHTracker()
        BSCtracker = bscWalletTransactionsTracker.BSCTracker()
        chat_ids = db_manager.db.get_users_ids()
        for chat in chat_ids:
            if chat == 'sequence':
                continue
            user_id = int(chat)
            users_wallets = db_manager.db.get_users_wallets(user_id=user_id)
            for wallet_type in users_wallets:
                for wallet in wallet_type:
                    if wallet[2] == 'etherscan.io':
                        eth_new_txs = ETHtracker.get_wallet_transactions(wallet[0], wallet[3])
                        if eth_new_txs is None:
                            continue
                        linked_hash = f'<a href="https://etherscan.io/tx/{eth_new_txs[0]}">{eth_new_txs[0]}</a>'
                        message_text = f'''🔔 New notification for {wallet[1]}
💱New ETH Transaction Hash: {linked_hash}
👝Wallet Address: {wallet[0]}
📅Date: {eth_new_txs[2]}
⚡Action: {eth_new_txs[12].split('(')[0]}
🫴From: {eth_new_txs[4]}
🫳To: {eth_new_txs[5]}
💰Value: {eth_new_txs[6]}
💸Transaction Fee: {eth_new_txs[10]} ETH
💲Transaction Gas Price: {eth_new_txs[7]} ETH
💴Transaction Gas Limit: {eth_new_txs[8]}
🪙Transaction Gas Used: {eth_new_txs[9]}
🚦Transaction Status: {eth_new_txs[11]}'''
                        await context.bot.send_message(chat_id=user_id, text=message_text, parse_mode=ParseMode.HTML)
                        db_manager.db.update_last_block_number(block_number=eth_new_txs[1], wallet_address=wallet[0], chat_id=user_id, source=wallet[2])
                    else:
                        bsc_new_txs = BSCtracker.get_wallet_transactions(wallet[0], wallet[3])
                        if bsc_new_txs is None:
                            continue
                        linked_hash = f'<a href="https://bscscan.com/tx/{bsc_new_txs[0]}">{bsc_new_txs[0]}</a>'
                        message_text = f'''🔔 New notification for {wallet[1]}
💱 New BSC Transaction Hash: {linked_hash}
👝 Wallet Address: {wallet[0]}
📅Date: {bsc_new_txs[2]}
⚡Action: {bsc_new_txs[12].split('(')[0]}
🫴From: {bsc_new_txs[4]}
🫳To: {bsc_new_txs[5]}
💰Value: {bsc_new_txs[6]}
💸Transaction Fee: {bsc_new_txs[10]} BNB
💲Transaction Gas Price: {bsc_new_txs[7]} BNB
💴Transaction Gas Limit: {bsc_new_txs[8]}
🪙Transaction Gas Used: {bsc_new_txs[9]}
🚦Transaction Status: {bsc_new_txs[11]}'''
                        await context.bot.send_message(chat_id=user_id, text=message_text, parse_mode=ParseMode.HTML)
                        db_manager.db.update_last_block_number(block_number=bsc_new_txs[1], wallet_address=wallet[0], chat_id=user_id, source=wallet[2])