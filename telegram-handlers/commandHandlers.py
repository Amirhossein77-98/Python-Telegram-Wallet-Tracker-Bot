from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db_manager
from access_checker import check_user_access

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if check_user_access(update.effective_chat.id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a bot, please talk to me!")
        db_manager.db.create_table(chat_id=update.effective_chat.id)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you don't have access.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = '''Hi, I'm a wallet tracker bot and I can track Ethereum and BNBSmartChain wallets from etherscan.io and bscscan.com.
    
In order to Add a new wallet to your wallets list please use the following format to send me the wallet:
command wallet-address source wallet-name
For example: add 0x00005501fdsdf020sd5f0 etherscan.io my-wallet
    
In order to Delete a wallet from your wallets list please use the following message format:
command wallet-spec source
For example: delete 0x00005501fdsdf020sd5f0 etherscan.io OR delete my-wallet etherscan.io'''
    if check_user_access(update.effective_chat.id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you don't have access.")

async def mywallets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    if check_user_access(user_id):
        bsc_button = [InlineKeyboardButton("BSCscan.com", callback_data="bscscan_wallets")]
        eth_button = [InlineKeyboardButton("Etherscan.io", callback_data="etherscan_wallets")]
        keyboard = [eth_button, bsc_button]
        await context.bot.send_message(chat_id=user_id, text='Which wallets would you like to manage?', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you don't have access.")