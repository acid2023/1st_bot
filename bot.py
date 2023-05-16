import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import pytz, os, ephem

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    user_name = update.message.from_user.username
    print(f'{user_name} вызвал /start')
    update.message.reply_text(f'Привет, {user_name} ! Ты вызвал команду /start')

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
    today = ephem.now()
    p_s = ['mars' , 'earth', 'mercury', 'venus', 'jupiter', 'saturn', 'uranus', 'neptune']
    mars = ephem.Mars(today)
    venus = ephem.Venus(today)
    jupiter = ephem.Jupiter(today)
    mercury = ephem.Mercury(today)
    saturn = ephem.Saturn(today)
    uranus = ephem.Uranus(today)
    neptune = ephem.Neptune(today)
    c_s = {'Mars': mars, 'Venus': venus, 'Mercury': mercury, 'Jupiter': jupiter,'Saturn':saturn,'Uranus':uranus, 'Neptune': neptune}
    print (c_s)
    print(today)
    user_text = update.message.text.split()
    phrase_count = len(user_text)
    if phrase_count == 1:
        update.message.reply_text('Введите название планеты')
        print ('no planet')
        return
    user_text = user_text[phrase_count - 1].lower()
    print(user_text)
    if user_text not in p_s:
        update.message.reply_text("Нет такой планеты в солнечной системе")
    else:
        planet = user_text.capitalize()
        print(planet)
        constelation = ephem.constellation(c_s[planet])
        print(constelation)
        update.message.reply_text(f'Выбрана планета {planet}, на {today} находится в {constelation}')

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