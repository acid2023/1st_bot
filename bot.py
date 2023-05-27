import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import pytz
import os
import ephem
import calc
import csv

planet_request = 0


logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    user_name = update.message.from_user.username
    update.message.reply_text(f'Привет, {user_name} ! Ты вызвал команду /start')


def tell_the_time(update, context):
    _time = datetime.now()
    tz_Moscow = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(tz_Moscow)
    update.message.reply_text(f'My time is {_time.strftime("%H:%M:%S")}')
    update.message.reply_text(f'Moscow time is {moscow_time.strftime("%H:%M:%S")}')


def stop_bot(update, context):
    user_name = update.message.from_user.username
    if user_name == "system_halted":
        os._exit(1)
    else:
        update.message.reply_text(user_name + ' - нет прав на выключение')
    return


def stopping(update, context):
    user_name = update.message.from_user.username
    update.message.reply_text(user_name + ' меня выключил')
    return stop_bot(update, context)


def astro_bot(update, context):
    global planet_request
    today = ephem.now()
    c_s = {'mars': ephem.Mars(today),  'mercury': ephem.Mercury(today),
           'venus': ephem.Venus(today), 'jupiter': ephem.Jupiter(today),
           'saturn': ephem.Saturn(today), 'uranus': ephem.Uranus(today),
           'neptune': ephem.Neptune(today)}
    input = context.args
    if len(input) == 0:
        update.message.reply_text('Введите название планеты')
        planet_request = 1
        return
    elif len(input) > 1:
        update.message.reply_text('Введите только одну планету')
        return
    user_text = input.lower()
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
    if constellation is None:
        update.message.reply_text("Нет такой планеты в солнечной системе")
    else:
        planet = user_text.capitalize()
        update.message.reply_text(f'Выбрана планета {planet}, на {today} находится в {constellation}')


def talk_to_me(update, context):
    global planet_request
    user_text = update.message.text
    user_name = update.message.from_user.username
    if planet_request == 1:
        astro_bot(update, context)
    else:
        update.message.reply_text(user_name + ' написал: ' + user_text)


def word_count(update, context):
    words_list = []
    words_list.clear()
    characters = '""!@#$%^&*()-+?_=,<>/""1234567890'
    words_list = context.args
    words_count = len(words_list)
    if words_count == 0:
        update.message.reply_text('необходимо ввести как минимум одно слово')
    words_count = 0
    special_char = 0
    print(words_list)
    for word in words_list:
        if any(c in characters for c in word):
            special_char += 1
        else:
            words_count += 1
    if words_count == 0:
        update.message.reply_text('слова не могут содержать цифры и спецсимволы')
        update.message.reply_text('необходимо ввести как минимум одно слово')
        return
    elif words_count == 1:
        number = 'слово'
    elif words_count <= 4:
        number = 'слова'
    elif words_count <= 20:
        number = 'слов'
    else:
        number = 'слово'
    update.message.reply_text(f'{words_count} {number}')


def calculator(update, context):
    update.message.reply_text('calculator')
    input = context.args
    if len(input) == 0:
        update.message.reply_text('необходимо ввести аргументы')
        return
    input_string = ''.join(input)
    arguement_check = calc.calc_arguement_check(input_string)
    if arguement_check != 'ok':
        update.message.reply_text(arguement_check)
        return
    answer = calc.calcus(input_string)
    update.message.reply_text(answer)


def get_cities_list_from_csv():
    results = []
    with open('city.csv', encoding='cp1251') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            results.append(row[0].split(';')[3][1:-1]) #из файла получались кривые строки вида "'text'" - то есть в строку входили кавычки
        return results

list_cities = get_cities_list_from_csv()
cities_dict = {}
cities_dict['reference'] = list_cities.copy()


def play_cities(update, context):
    global cities_dict
    user_name = update.message.from_user.username
    input = context.args
    user_text = input[0]
    if len(user_text) == 0:
        update.message.reply_text('введите город')
        return
    if cities_dict.get(user_name, 'none') == 'none':
        cities_dict[user_name] = cities_dict['reference'].copy()
    if user_text not in cities_dict['reference']:
        update.message.reply_text('нет такого города')
        return
    elif user_text not in cities_dict[user_name]:
        update.message.reply_text('такой город уже был')
        return
    next_city_start_letter = "#"
    for count, city in enumerate(cities_dict[user_name]):
        if city == user_text:
            next_city_start_letter = city[-1]
            del cities_dict[user_name][count]
            break
    answer = 'не нашел город'
    for count, city in enumerate(cities_dict[user_name]):
        if city[0].lower() == next_city_start_letter:
            answer = f'{city}. Твой ход.'
            update.message.reply_text(answer)
            del cities_dict[user_name][count]
            return
    update.message.reply_text(answer)
        


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("time", tell_the_time))
    dp.add_handler(CommandHandler('exit', stopping))
    dp.add_handler(CommandHandler("planet", astro_bot))
    dp.add_handler(CommandHandler("calc", calculator))
    dp.add_handler(CommandHandler("city", play_cities))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стратовал")
    mybot.start_polling()
    mybot.idle


if __name__ == "__main__":
    main()
