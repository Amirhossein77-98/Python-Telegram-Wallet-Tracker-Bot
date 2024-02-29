import sqlite3

class DBManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def create_table(self, chat_id):
        self.conn.execute(f"""CREATE TABLE IF NOT EXISTS user_{str(chat_id)}
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          source TEXT,
                          chat_id INTEGER,
                          eth_wallet TEXT UNIQUE,
                          bsc_wallet TEXT UNIQUE,
                          wallet_name TEXT,
                          last_block TEXT)""")
    
    def save_wallet(self, user_id, wallet_address, wallet_name, source):
        if source == 'etherscan.io':
            self.conn.execute(f"INSERT INTO user_{str(user_id)} (chat_id, eth_wallet, wallet_name, source) VALUES (?, ?, ?, ?)", (user_id, wallet_address, wallet_name, source))
        elif source == 'bscscan.com':
            self.conn.execute(f"INSERT INTO user_{str(user_id)} (chat_id, bsc_wallet, wallet_name, source) VALUES (?, ?, ?, ?)", (user_id, wallet_address, wallet_name, source))
        self.conn.commit()
    
    def update_last_block_number(self, chat_id, block_number, wallet_address, source):
        if source == 'bscscan.com':
            self.conn.execute(f"UPDATE user_{str(chat_id)} SET last_block = ? WHERE bsc_wallet = ?", (block_number, str(wallet_address)))
        elif source == 'etherscan.io':
            self.conn.execute(f"UPDATE user_{str(chat_id)} SET last_block = ? WHERE eth_wallet = ?", (block_number, str(wallet_address)))
        self.conn.commit()
    

    def delete_wallet(self, chat_id, source, wallet_address='None', wallet_name='None'):
        if source == 'etherscan.io':
            if wallet_name == 'None':
                self.conn.execute(f"DELETE FROM user_{str(chat_id)} WHERE eth_wallet = ?", ([str(wallet_address)]))
            elif wallet_address == 'None':
                self.conn.execute(f"DELETE FROM user_{str(chat_id)} WHERE wallet_name = ? AND source = ?", (wallet_name, source))
        elif source == 'bscscan.com':
            if wallet_name == 'None':
                self.conn.execute(f"DELETE FROM user_{str(chat_id)} WHERE bsc_wallet = ?", ([str(wallet_address)]))
            elif wallet_address == 'None':
                self.conn.execute(f"DELETE FROM user_{str(chat_id)} WHERE wallet_name = ? AND source = ?", (wallet_name, source))
        self.conn.commit()
    
    def get_users_wallets(self, user_id):
        eth_wallets = self.conn.execute(f"SELECT eth_wallet, wallet_name, source, last_block FROM user_{str(user_id)} WHERE eth_wallet IS NOT NULL").fetchall()
        bsc_wallets = self.conn.execute(f"SELECT bsc_wallet, wallet_name, source, last_block FROM user_{str(user_id)} WHERE bsc_wallet IS NOT NULL").fetchall()
        return [eth_wallets] + [bsc_wallets]

    def get_users_ids(self):
        tables = self.conn.execute("""SELECT name FROM sqlite_master WHERE type='table'""").fetchall()
        cleared_tables = []
        for table in tables:
            if table[0].split('_')[1] not in cleared_tables:
                cleared_tables.append(table[0].split('_')[1])
        return cleared_tables
        
db = DBManager('database.db')