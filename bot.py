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
    bot.send_message(message.from_user.id, "🌎 Выберите язык/Choose your language", reply_markup=markup)

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
        if news.find('span') is not None:
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
duration = {'За месяц':(30, russian_url, "0"),'За неделю':(7, russian_url, "0"),'За год':(365, russian_url, "0"), 'For a month':(31, english_url, "0"),'For a week':(7, english_url, "0"),
            'For a year':(365, english_url, "0")}
categories = {"Разработки 💡":(365, russian_url, 400),"Наука 🧪":(365, russian_url, 399),"Достижения 😎":(365, russian_url, 401),"Конференции 👨‍💻👩‍💻":(365, russian_url, 1),"Возможности 🔬":(365, russian_url, 402),
              "Achievement 😎":(365, english_url, 401),"Conferences 👨‍💻👩‍💻":(365, english_url, 1),"Developments 💡":(365, english_url, 400),"Opportunities 🔬":(365, english_url, 402),"Science 🧪":(365, english_url, 399)}
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print("я тут")
    global russian_url
    global english_url
    global duration
    global categories
    def novosti(x, url, value):
        get = news(x, url, value)
        # /\global english_url
        if url == english_url:
            if get == []:
                markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn3 = types.KeyboardButton('For a week')
                btn5 = types.KeyboardButton('For a month')
                btn6 = types.KeyboardButton('For a year')
                btnback = types.KeyboardButton('Back')
                btnlng = types.KeyboardButton('🌎 Back to language selection')
                markup2.add(btnlng, btn3, btn5, btn6,btnback)
                bot.send_message(message.from_user.id, "There are no news in this period", reply_markup=markup2)
            else:
                print("here")
                for i in get:
                    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    # btn = types.KeyboardButton("To the main page")
                    # markup.add(btn)
                    messag = str(i['datt']) + "\n" + " " + "\n" + i['title']
                    markup = types.InlineKeyboardMarkup()
                    btn_my_site = types.InlineKeyboardButton(text='More', url=i['link'])
                    markup.add(btn_my_site)
                    bot.send_photo(message.from_user.id, i['photo'], messag, reply_markup=markup)
        else:
            if get == []:
                markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn3 = types.KeyboardButton('За неделю')
                btn5 = types.KeyboardButton('За месяц')
                btn6 = types.KeyboardButton('За год')
                btnback = types.KeyboardButton('Назад')
                btnlng = types.KeyboardButton('🌎 Back to language selection')
                markup2.add(btnlng, btn3, btn5, btn6, btnback)
                bot.send_message(message.from_user.id, "За это период новостей не было", reply_markup=markup2)
            else:
                for i in get:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn = types.KeyboardButton('На главную страницу')
                    markup.add(btn)
                    messag = str(i['datt']) + "\n" + " " + "\n" + i['title']
                    markup = types.InlineKeyboardMarkup()
                    btn_my_site = types.InlineKeyboardButton(text='Подробнее', url=i['link'])
                    markup.add(btn_my_site)
                    bot.send_photo(message.from_user.id, i['photo'], messag, reply_markup=markup)

    if message.text == 'Русский' or message.text == "На главную страницу":
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn10 = types.KeyboardButton('Новости факультета')
        btnlng = types.KeyboardButton('🌎 Back to language selection')
        markup2.add(btnlng, btn10)
        bot.send_message(message.from_user.id, "Что вас интересует? ", reply_markup=markup2)

    elif message.text == 'Новости факультета' or message.text == 'Назад':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn10 = types.KeyboardButton('Все новости 🗞')
        btn11 = types.KeyboardButton('Наука 🧪')
        btn12 = types.KeyboardButton('Разработки 💡')
        btn13 = types.KeyboardButton('Достижения 😎')
        btn14 = types.KeyboardButton('Конференции 👨‍💻👩‍💻')
        btn15 = types.KeyboardButton('Возможности 🔬')
        btnlng = types.KeyboardButton('🌎 Back to language selection')
        markup2.add(btnlng, btn10, btn11, btn12, btn13, btn14, btn15)
        bot.send_message(message.from_user.id, "Выберите категорию ", reply_markup=markup2)

    elif message.text == '🌎 Вернуться к выбору языка' or message.text =='🌎 Back to language selection':
        start(message)

    elif message.text == 'Все новости 🗞':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton('За год')
        btn5 = types.KeyboardButton('За неделю')
        btn6 = types.KeyboardButton('За месяц')
        btnback = types.KeyboardButton('Назад')
        btnlng = types.KeyboardButton('🌎 Back to language selection')
        markup2.add(btnlng, btn5, btn6, btn3, btnback)
        bot.send_message(message.from_user.id, "Выберите период времени ", reply_markup=markup2)
    elif message.text == 'English':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn10 = types.KeyboardButton('News of the Faculty')
        btnlng = types.KeyboardButton('🌎 Вернуться к выбору языка')
        markup2.add(btnlng, btn10)
        bot.send_message(message.from_user.id, "Сhoose the category ", reply_markup=markup2)
    elif message.text == 'News of the Faculty' or message.text == 'Back':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn10 = types.KeyboardButton('All news 🗞')
        btn11 = types.KeyboardButton('Achievement 😎')
        btn12 = types.KeyboardButton('Conferences 👨‍💻👩‍💻')
        btn13 = types.KeyboardButton('Developments 💡')
        btn14 = types.KeyboardButton('Opportunities 🔬')
        btn15 = types.KeyboardButton('Science 🧪')
        btnlng = types.KeyboardButton('🌎 Вернуться к выбору языка')
        markup2.add(btnlng, btn10, btn11, btn12, btn13, btn14, btn15)
        bot.send_message(message.from_user.id, "Сhoose the category ", reply_markup=markup2)
    elif message.text == 'All news 🗞':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton('For a month')
        btn5 = types.KeyboardButton('For a week')
        btn6 = types.KeyboardButton('For a year')
        btnback = types.KeyboardButton('Back')
        btnlng = types.KeyboardButton('🌎 Вернуться к выбору языка')
        markup2.add(btnlng, btn5, btn3, btn6,btnback)
        bot.send_message(message.from_user.id, "Choose the duration", reply_markup=markup2)
    elif message.text in duration:
        novosti(*duration[message.text])
    elif message.text in categories:
        novosti(*categories[message.text])




text_start = """
-------------------------------------------------------

                I have started, my boss!

                  Wishing all the best!

-------------------------------------------------------
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠋⠈⠻⣮⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⡿⠋⠀⠀⠀⠀⠙⣿⣿⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⡿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠿⠿⣿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⣿⣶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣠⣤⣤⣀⡀⠀⠀⣀⣴⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣄⠀⠀
⢀⣤⣾⡿⠟⠛⠛⢿⣿⣶⣾⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣷⣦⣀⣀⣤⣶⣿⡿⠿⢿⣿⡀⠀
⣿⣿⠏⠀⢰⡆⠀⠀⠉⢿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⡿⠟⠋⠁⠀⠀⢸⣿⠇⠀
⣿⡟⠀⣀⠈⣀⡀⠒⠃⠀⠙⣿⡆⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠇⠀
⣿⡇⠀⠛⢠⡋⢙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀
⣿⣧⠀⠀⠀⠓⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠋⠀⠀⢸⣧⣤⣤⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡿⠀⠀
⣿⣿⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠻⣷⣶⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠁⠀⠀
⠈⠛⠻⠿⢿⣿⣷⣶⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡏⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠻⠿⢿⣿⣷⣶⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⡄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠻⠿⢿⣿⣷⣶⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠿⠿⣿⣷⣶⣶⣤⣤⣀⡀⠀⠀⠀⢀⣴⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡿⣄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠿⠿⣿⣷⣶⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣹
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⢸⣧
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣆⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣶⣾⣿⣿⣿⣿⣤⣄⣀⡀⠀⠀⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣻⣷⣶⣾⣿⣿⡿⢯⣛⣛⡋⠁⠀⠀⠉⠙⠛⠛⠿⣿⣿⡷⣶⣿
⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣴⣦⣦⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⣾⡿⠛⠛⡉⣉⣉⡀⠀⢤⡉⢳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣀⣤⣾⡿⢋⣴⣖⡟⠛⢻⣿⣿⣽⣆⠙⢦⡙⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠖⠒⠻⠻⠶⣦⣄⠀
⠉⣿⢸⠁⣸⣥⣹⠧⡠⣾⣿⣿⣿⣿⣧⡈⢷⣼⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣾⣿⣿⣶⣦⣈⠈⠻⣤
⠀⢹⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⣫⠀⠙⣿⣿⣿⣿⣷⡄⣽
⠀⠀⠳⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣀⣿⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⠭⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠒⡊⠙⠉⠉⠉⠓⠲⠤⡀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⠏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠿⣦⣴⣿⣶⣶⠀⠠⠀⣰⣤⣿⣦⠀⠀⠀⠀⠉⠙⠛⠻⠛⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢛⠃⢀⣄⠀⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠊⠟⠋⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⣄⡀⠀⠀⢀⣀⣠⣴⡿⣿⣦⣀⠀⠀⠀⠀⢀⣴⠏⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠻⠿⠉⠉⠉⠉⠉⠑⠋⠙⠻⡢⢖⡯⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
print(text_start)
while True:
    bot.polling(none_stop=True, interval=0)