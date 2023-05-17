import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import pytz, os, ephem

planet_request = 0

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    user_name = update.message.from_user.username
    print(f'{user_name} вызвал /start')
    update.message.reply_text(f'Привет, {user_name} ! Ты вызвал команду /start')

def tell_the_time(update, context):    
    _time = datetime.now()
    tz_Moscow = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(tz_Moscow)
    update.message.reply_text(f'My time is {_time.strftime("%H:%M:%S")}')
    update.message.reply_text(f'Moscow time is {moscow_time.strftime("%H:%M:%S")}')

def stop_bot(update, context):
    user_name = update.message.from_user.username
    if user_name == "system_halted" :
        os._exit(1)
    else:   
        update.message.reply_text(user_name + ' - нет прав на выключение' )
    return

def stopping(update, context):
    user_name = update.message.from_user.username
    update.message.reply_text(user_name + ' меня выключил' )
    return stop_bot(update, context)

def astro_bot(update, context):
    global planet_request
    today = ephem.now()
    c_s = {'mars':ephem.Mars(today),  'mercury':ephem.Mercury(today), 
           'venus':ephem.Venus(today), 'jupiter':ephem.Jupiter(today), 
           'saturn':ephem.Saturn(today), 'uranus':ephem.Uranus(today), 
           'neptune' : ephem.Neptune(today)}
    user_text = update.message.text.split()
    phrase_count = len(user_text)
    user_text = user_text[phrase_count - 1].lower()
    if planet_request == 0:
        if phrase_count == 1:
            update.message.reply_text('Введите название планеты')
            planet_request = 1
            return
    constellation = c_s.get(user_text, None)
    constellation = ephem.constellation(constellation)
    planet_request = 0
    if constellation == None:
        update.message.reply_text("Нет такой планеты в солнечной системе")
    else:
        planet = user_text.capitalize()
        update.message.reply_text(f'Выбрана планета {planet}, на {today} находится в {constellation}')

def talk_to_me(update, context):
    global planet_request
    user_text= update.message.text
    user_name = update.message.from_user.username
    print(user_text)
    print(user_name)
    if planet_request == 1:
        astro_bot(update, context)
    else:
        update.message.reply_text(user_name + ' написал: ' + user_text )

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher   
    dp.add_handler(CommandHandler("start",greet_user))
    dp.add_handler(CommandHandler("time",tell_the_time))
    dp.add_handler(CommandHandler('exit', stopping))
    dp.add_handler(CommandHandler("planet", astro_bot))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стратовал")
    mybot.start_polling()
    mybot.idle

if __name__ == "__main__":
    main()