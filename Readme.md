# Python Telegram Wallet Tracker Bot
This is a Telegram bot that can track Ethereum (ETH) and Binance Smart Chain (BSC) wallets. It can accept a limited number of users and notify them of new transactions on their wallets.

# How it works
The user sends the wallet address, the name of the wallet, and the source (etherscan.io or bscscan.io) to the bot.
The bot will save the wallet details in a SQLite database.
The bot will check for new transactions of the wallets periodically (every 10 minutes by default) and will send the transaction details to the user’s private chat.
The user can manage the wallets and delete them through commands or inline keyboard buttons.

# Dependencies
This project uses the following libraries:

* python-telegram-bot v20
* future
* sqlite3
* sys
* requests
* datetime

# Installation
To run this project, you need to have Python 3.6 or higher installed on your system. You also need to create a Telegram bot token using BotFather and set it as an environment variable named TELEGRAM_TOKEN.

Then, you can clone this repository and install the dependencies using pip:

git clone https://github.com/your_username/python-telegram-wallet-tracker-bot.git
cd python-telegram-wallet-tracker-bot
pip install -r requirements.txt

# Usage
To start the bot, run the following command:

python main.py

The bot will be online and ready to receive messages from the users. You can use the following commands to interact with the bot:

/start - Start the bot and get a welcome message.
/help - Get a list of available commands and instructions.
/MyWallets - To manage and delete your wallets.

In order to Add a new wallet to your wallets list please use the following format to send me the wallet:
command wallet-address source wallet-name
For example: add 0x00005501fdsdf020sd5f0 etherscan.io my-wallet
    
In order to Delete a wallet from your wallets list please use the following message format:
command wallet-spec source
For example: delete 0x00005501fdsdf020sd5f0 etherscan.io OR delete my-wallet etherscan.io