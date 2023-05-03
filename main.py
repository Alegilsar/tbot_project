import telebot
import requests
from bs4 import BeautifulSoup
import datetime


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



def news(d):
    url = 'https://physics.itmo.ru/ru/news'
    spisok = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_list = soup.find_all('div', {'class': 'col-md-6 views-row'})
    print(news_list)
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
    if message.text  == 'Русский':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3= types.KeyboardButton('За сутки')
        btn5 = types.KeyboardButton('Неделя')
        btn6 = types.KeyboardButton('За месяц')
        btn4 = types.KeyboardButton('Всё время ')
        btnlng =types.KeyboardButton('Вернутся к выбору языка/back to language choosing')
        markup2.add(btnlng,btn3,btn5,btn6,btn4)
        bot.send_message(message.from_user.id, "Выберите период времени ", reply_markup=markup2)

    elif message.text == 'За месяц':
        get = news(31)
        if get == []:
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton('За сутки')
            btn5 = types.KeyboardButton('Неделя')
            btn6 = types.KeyboardButton('За месяц')
            btn4 = types.KeyboardButton('Всё время ')
            btnlng = types.KeyboardButton('Вернутся к выбору языка/back to language choosing')
            markup2.add(btnlng, btn3, btn5, btn6, btn4)
            bot.send_message(message.from_user.id, "За это период новостей не было", reply_markup=markup2)
        else:
            for i in get:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = types.KeyboardButton('Главная страница')
                markup.add(btn)
                messag =  str(i['datt']) + "\n" + " " + "\n" + i['title'] + "\n" + " " + "\n" + "Подробнее " + i['link']
                bot.send_photo(message.from_user.id, i['photo'], messag)
    elif message.text == 'Неделя':
        nov= news(7)
        if nov == []:
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton('За сутки')
            btn5 = types.KeyboardButton('Неделя')
            btn6 = types.KeyboardButton('За месяц')
            btn4 = types.KeyboardButton('Всё время ')
            btnlng = types.KeyboardButton('Вернутся к выбору языка/back to language choosing')
            markup2.add(btnlng, btn3, btn5, btn6, btn4)
            bot.send_message(message.from_user.id, "За это период новостей не было", reply_markup=markup2)
        else:
            for i in nov:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = types.KeyboardButton('Главная страница')
                markup.add(btn)
                messag =  str(i['datt']) + "\n" + " " + "\n" + i['title'] + "\n" + " " + "\n" + "Подробнее " + i['link']
                bot.send_photo(message.from_user.id, i['photo'], messag)


    # отправляем новость в Telegram bot
    # params = {
    #     'chat_id': 'https://t.me/FacultyofNews_bot',
    #     'text': f'<b>{title}</b><a href="{link}">Подробнее</a>',
    #     'parse_mode': 'HTML'
    # }
    # response = requests.post('https://api.telegram.org/botY6181346337:AAFR9gF-FFXM66F0URtbGbnUGVHxHZonZrM/sendMessage', data=params)



bot.polling(none_stop=True, interval=0)
