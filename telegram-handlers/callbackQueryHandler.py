from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db_manager

async def button_pressed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = update.effective_chat.id
    message_id = query.message.message_id
    
    if query['data'] == "etherscan_wallets":
        eth_wallets = db_manager.db.get_users_wallets(user_id)[0]
        wallets_button = []
        for wallet in eth_wallets:
            wallets_button.append([InlineKeyboardButton(wallet[1], callback_data=f"eth_wallet_{wallet[0]}")])
        
        wallets_button.append([InlineKeyboardButton("< Back", callback_data=f"source_selection")])
        await context.bot.edit_message_text(chat_id=user_id, text='Here are your ETH wallets with respect:\nSelect a wallet if you want to delete it.', 
                                                    message_id=message_id, reply_markup=InlineKeyboardMarkup(wallets_button))


    elif query['data'] == "bscscan_wallets":
        bsc_wallets = db_manager.db.get_users_wallets(user_id)[1]
        wallets_button = []
        for wallet in bsc_wallets:
            wallets_button.append([InlineKeyboardButton(wallet[1], callback_data=f"bsc_wallet_{wallet[0]}")])
        
        wallets_button.append([InlineKeyboardButton("< Back", callback_data=f"source_selection")])
        await context.bot.edit_message_text(chat_id=user_id, text='Here are your BSC wallets with respect:\nSelect a wallet if you want to delete it.', 
                                                    message_id=message_id, reply_markup=InlineKeyboardMarkup(wallets_button))

    elif query['data'].startswith('eth_wallet_'):
        wallet = query['data'].split('_')[-1]
        yes_button = [InlineKeyboardButton("Yes DELETE!", callback_data=f"yes_delete_eth_{wallet}")]
        no_button = [InlineKeyboardButton("NO!!!", callback_data="no_delete_eth")]
        back_button = [InlineKeyboardButton("< Back", callback_data=f"etherscan_wallets")]
        keyboard = [yes_button, no_button, back_button]
        await context.bot.edit_message_text(chat_id=user_id, text="Are you sure you want to delete this wallet?", message_id=message_id, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query['data'].startswith('bsc_wallet_'):
        wallet = query['data'].split('_')[-1]
        yes_button = [InlineKeyboardButton("Yes DELETE!", callback_data=f"yes_delete_bsc_{wallet}")]
        no_button = [InlineKeyboardButton("NO!!!", callback_data="no_delete_bsc")]
        back_button = [InlineKeyboardButton("< Back", callback_data=f"bscscan_wallets")]
        keyboard = [yes_button, no_button, back_button]
        await context.bot.edit_message_text(chat_id=user_id, text="Are you sure you want to delete this wallet?", message_id=message_id, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query['data'].startswith('yes_delete_'):
        wallet = str(query['data'].split('_')[-1])
        if query['data'].split('_')[-2] == 'eth':
            back_button = [[InlineKeyboardButton("< Back", callback_data=f"etherscan_wallets")]]
            db_manager.db.delete_wallet(chat_id=user_id, wallet_address=wallet, source='etherscan.io')
        elif query['data'].split('_')[-2] == 'bsc':
            back_button = [[InlineKeyboardButton("< Back", callback_data=f"bscscan_wallets")]]
            db_manager.db.delete_wallet(chat_id=user_id, wallet_address=wallet, source='bscscan.com')
        await context.bot.edit_message_text(chat_id=user_id, text="Wallet deleted successfully!", message_id=message_id, reply_markup=InlineKeyboardMarkup(back_button))
    
    elif query['data'].startswith('no_delete_'):
        if query['data'].split('_')[-1] == 'eth':
            back_button = [[InlineKeyboardButton("< Back", callback_data=f"etherscan_wallets")]]
        elif query['data'].split('_')[-1] == 'bsc':
            back_button = [[InlineKeyboardButton("< Back", callback_data=f"bscscan_wallets")]]

        await context.bot.edit_message_text(chat_id=user_id, text="Ok, I keep the wallet in mind!", message_id=message_id, reply_markup=InlineKeyboardMarkup(back_button))

    elif query['data'] == 'source_selection':
        bsc_button = [InlineKeyboardButton("BSCscan.com", callback_data="bscscan_wallets")]
        eth_button = [InlineKeyboardButton("Etherscan.io", callback_data="etherscan_wallets")]
        keyboard = [eth_button, bsc_button]
        await context.bot.edit_message_text(chat_id=user_id, message_id=message_id, text='Which wallets would you like to manage?', reply_markup=InlineKeyboardMarkup(keyboard))