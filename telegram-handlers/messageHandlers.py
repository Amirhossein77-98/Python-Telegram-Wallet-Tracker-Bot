from telegram import Update
from telegram.ext import CallbackContext
import db_manager
from access_checker import check_user_access


async def message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if check_user_access(user_id):
        message = update.message.text
        try:
            if message.lower().startswith('add'):
                command, wallet_address, source, wallet_name = message.split()
                if source == 'etherscan.io' or source == 'bscscan.com':
                    try:
                        db_manager.db.save_wallet(user_id=user_id, wallet_address=wallet_address, wallet_name=wallet_name, source=source)
                        await context.bot.send_message(chat_id=user_id, text='Wallet saved successfully')
                    except Exception as e:
                        e = str(e)
                        await context.bot.send_message(chat_id=user_id, text=f"An error occured: {'This wallet already exists!' if e.startswith('UNIQUE') else e}")
                else:
                    await context.bot.send_message(chat_id=user_id, text='Supported sources are only: etherscan.io and bscscan.com')

            elif message.lower().startswith('delete'):
                command, wallet_spec, source = message.split()
                if source == 'etherscan.io' or source == 'bscscan.com':
                    if wallet_spec.startswith('0x'):
                        try:
                            db_manager.db.delete_wallet(chat_id=user_id, source=source, wallet_address=wallet_spec)
                            await context.bot.send_message(chat_id=user_id, text=f'Wallet deleted successfully')

                        except Exception as e:
                            e = str(e)
                            await context.bot.send_message(chat_id=user_id, text=f"Something went wrong! please try again.\nFor more help please use /help\n {e}")
                    else:
                        try:
                            db_manager.db.delete_wallet(chat_id=user_id, source=source, wallet_name=wallet_spec)
                            await context.bot.send_message(chat_id=user_id, text=f'Wallet deleted successfully')
                        except Exception as e:
                            e = str(e)
                            await context.bot.send_message(chat_id=user_id, text=f"Something went wrong! please try again.\nFor more help please use /help\n {e}")
                else:
                    await context.bot.send_message(chat_id=user_id, text='Supported sources are only: etherscan.io and bscscan.com')
            else:
                await context.bot.send_message(chat_id=user_id, text='Your message should either start with "delete" or "add""')
        except:
            await context.bot.send_message(chat_id=user_id, text='''If you want to add a wallet, your message should be in this format:
    command walltet_address source wallet_name
    If you want to delete a wallet, your message should be in this format:
    command wallet_spec source
                                        
    For more information use /help''')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you don't have access.")