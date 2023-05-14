import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import pytz

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    user_text= update.message.text
    user_name = update.message.from_user.username
    print(user_text)
    print(user_name)
    update.message.reply_text(user_name + ' написал: ' + user_text )

def tell_the_time(update, context):    
    _time = datetime.now()
    tz_Moscow = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(tz_Moscow)
    update.message.reply_text(f'My time is {_time.strftime("%H:%M:%S")}')
    update.message.reply_text(f'Moscow time is {moscow_time.strftime("%H:%M:%S")}')

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start",greet_user))
    dp.add_handler(CommandHandler("time",tell_the_time))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стратовал")
    mybot.start_polling()
    mybot.idle

if __name__ == "__main__":
    main()