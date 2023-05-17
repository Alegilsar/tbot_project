import telebot
import requests
from bs4 import BeautifulSoup
import datetime


english_url = 'https://physics.itmo.ru/en/news'
russian_url = 'https://physics.itmo.ru/ru/news'

from telebot import types
bot = telebot.TeleBot('6181346337:AAFR9gF-FFXM66F0URtbGbnUGVHxHZonZrM')

#тело бота
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup( resize_keyboard= True)
    btn1 = types.KeyboardButton('Русский')
    btn2 = types.KeyboardButton('English')
    markup.add(btn1,btn2)
    bot.send_message(message.from_user.id, "Выберите язык/Choose your language", reply_markup=markup)

def categotia(url,value):
    url = str(url)
    params = {'category': value}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # обработка полученных данных
        return response.text
    else:
        print(f'Ошибка {response.status_code}: {response.reason}')
def news(d, url, value):
    spisok = []
    if value == "0":
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        ret = categotia(url, value)
        soup = BeautifulSoup(ret, 'html.parser')
    news_list = soup.find_all('div', {'class': 'col-md-6 views-row'})
    site_utl='https://physics.itmo.ru'
    for news in news_list:
        title = news.find('span').text
        link = site_utl + news.find('a')['href']
        datt = news.find('time')['datetime']

        if "T" in datt:

            datt=datt.replace("T",' ')
            datt = datt.replace("Z", '')

        datt = datetime.datetime.strptime(datt, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        deffer=datetime.timedelta(days= d)
        photo = site_utl +  news.find('img')['src']
        slovo = {}
        if datt > (now - deffer):
            slovo['title'] = title
            slovo['link'] = link
            slovo['photo'] = photo
            slovo['datt'] = datt
            spisok.append(slovo)

    return spisok



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print("я тут")
    global russian_url
    global english_url
    def novosti(x, url, value):
        get = news(x, url, value)
        # /\global english_url
        if url == english_url:
            if get == []:
                markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn3 = types.KeyboardButton('For day')
                btn5 = types.KeyboardButton('For week')
                btn6 = types.KeyboardButton('For month')
                btnlng = types.KeyboardButton('Вернуться к выбору языка')
                markup2.add(btnlng, btn3, btn5, btn6)
                bot.send_message(message.from_user.id, "There are no news in this period", reply_markup=markup2)
            else:
                for i in get:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn = types.KeyboardButton("Main")
                    markup.add(btn)
                    messag = str(i['datt']) + "\n" + " " + "\n" + i['title'] + "\n" + " " + "\n" + "Подробнее " + i[
                        'link']
                    bot.send_photo(message.from_user.id, i['photo'], messag)
        else:
            if get == []:
                markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn3 = types.KeyboardButton('За сутки')
                btn5 = types.KeyboardButton('Неделя')
                btn6 = types.KeyboardButton('За месяц')
                btnlng = types.KeyboardButton('Back to language choosing')
                markup2.add(btnlng, btn3, btn5, btn6)
                bot.send_message(message.from_user.id, "За это период новостей не было", reply_markup=markup2)
            else:
                for i in get:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn = types.KeyboardButton('Главная страница')
                    markup.add(btn)
                    messag = str(i['datt']) + "\n" + " " + "\n" + i['title'] + "\n" + " " + "\n" + "Подробнее " + i['link']
                    bot.send_photo(message.from_user.id, i['photo'], messag)



    if message.text == 'Русский':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn10 = types.KeyboardButton('Все новости факультета')
        btn11 = types.KeyboardButton('Наука')
        btn12 = types.KeyboardButton('Разработки')
        btn13 = types.KeyboardButton('Разработки')
        btnlng = types.KeyboardButton('Back to language choosing')
        markup2.add(btnlng, btn10, btn11, btn12)
        bot.send_message(message.from_user.id, "Выберите категорию ", reply_markup=markup2)

    elif message.text == 'Вернуться к выбору языка' or message.text =='Back to language choosing':
        start(message)

    elif message.text == 'Все новости факультета':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton('За сутки')
        btn5 = types.KeyboardButton('Неделя')
        btn6 = types.KeyboardButton('За месяц')
        btnlng = types.KeyboardButton('На главную страницу')
        markup2.add(btnlng, btn3, btn5, btn6)
        bot.send_message(message.from_user.id, "Выберите период времени ", reply_markup=markup2)
    elif message.text == 'За месяц':
        novosti(365, russian_url, "0")
    elif message.text == 'Неделя':

        novosti(7, russian_url, "0")
    elif message.text == 'За сутки':
        novosti(1, russian_url, "0")
    elif message.text == 'English':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn10 = types.KeyboardButton('Any news')
        btn11 = types.KeyboardButton('Achievement')
        btn12 = types.KeyboardButton('Conferences')
        btn13 = types.KeyboardButton('Developments')
        btn14 = types.KeyboardButton('Opportunities')
        btn15 = types.KeyboardButton('Science')
        btnlng = types.KeyboardButton('Back to language choosing')
        markup2.add(btnlng, btn10, btn11, btn12,btn13,btn14,btn15)
        bot.send_message(message.from_user.id, "Выберите категорию ", reply_markup=markup2)
    elif message.text == 'Any news':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton('For mont')
        btn5 = types.KeyboardButton('For week')
        btn6 = types.KeyboardButton('For day')
        btnlng = types.KeyboardButton('Back to the main')
        markup2.add(btnlng, btn3, btn5, btn6)
        bot.send_message(message.from_user.id, "Выберите период времени ", reply_markup=markup2)

    elif message.text == 'For month':
        novosti(31, english_url, "0")
    elif message.text == 'For week':
        novosti(7, english_url, "0")
    elif message.text == 'For day':
        novosti(1, english_url, "0")
    elif message.text == 'Наука':
        novosti(365,russian_url,399)


text_start = """
-------------------------------------------------------

                I have started, my boss!

                  Wishing all the best!

-------------------------------------------------------
"""
print(text_start)

bot.polling(none_stop=True, interval=0)