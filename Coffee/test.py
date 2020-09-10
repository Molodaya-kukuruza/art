from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import KeyboardButton
import datetime
import time
import random

import sqlite3
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

tg_token = '842308578:AAHu6MUSeIsfFOhOVJ6R9QsYxcN1so7qLM4'

FRIEND, ENTERKEY, HEY, CHOOSE, COFF, TENSE, DOPS, ORDER, COMMENT, PRINTRESULT, PAY, REFILL2 = range (12)
stickers_hi = ["CAADAgADAQADMrRrHqcoMF-oDYwwFgQ", "CAADAgADDQADMrRrHjMWVp8jKWqmFgQ", "CAADAgADEQADMrRrHl1MXbQzqgABHhYE", 
    "CAADAgADBAADW9VNI6KdnboBVRslFgQ", "CAADAgADCAADW9VNIxA9x-MQ2veWFgQ", "CAADAgADEQADzOBAFP6dLgHHb39LFgQ", "CAADAgADPAADpnQoA8Uj-TgfLDWcFgQ",
        "CAADAgADGgADH0xEDPfiqJWTEUp6FgQ"]
stickers_by = ["CAADAgADBgADW9VNI4B6BZiQ9giGFgQ", "CAADAgADBAADW9VNI6KdnboBVRslFgQ", "CAADAgADOwADpnQoA04d9dQIOkjQFgQ"]
'''class Order():
    def __init__(self, user_id = 0, user_name = '', user_surname = '', order_num = 0, ttime = 'now', coffee = '', ssize = '', add = '', 
    com = '', sect_cost = '', cost = 0, cost_extra = 0, cost_fin = 0):
        self.user_id = user_id
        self.user_name = user_name
        self.user_surname = user_surname
        self.order_num = order_num
        self.ttime = ttime
        self.coffee = coffee
        self.ssize = ssize
        self.add = add
        self.com = com
        self.sect_cost = sect_cost
        self.cost = cost
        self.cost_extra = cost_extra
        self.cost_fin = cost_fin'''

number = []
number.append(1)

Categories = [['Кофе'], ['Раф'], ['Напитки'], ['Фреши', 'Другое']]
butDops =[['На альтернативном молоке'], ['Сироп'], ['Топпинг', 'Сгущенное молоко', 'Маршмеллоу'], ['Еще эспрессо'], ['Что-то свое, сейчас напишу'], ['Ничего не надо']]
Greeting = ['Привет', 'привет', 'Здравствуй', 'здравствуй', 'Здравствуйте', 'Здравствуйте', 'Хай', 'хай', 'Халлоу', 'халлоу', 'Халоу', 'халоу', 
    'Хэллоу', 'хэллоу', 'Хэлоу', 'хэлоу', 'Прифки', 'прифки', 'Привки', 'привки', 'Чекаво', 'чекаво', 'Дратути', 'дратути', 'Хало', 'хало',
        'Здаров', 'здаров', 'Даров', 'даров', 'Здарова', 'здарова', 'Дарова', 'дарова', 'Куку', 'куку', 'Куку епта', 'куку епта', 
            'Доброе утро', 'доброе утро', 'Добрый день', 'добрый день', 'Добрый вечер', 'добрый вечер', 'Здарофки', 'здарофки', 'Дарофки',
                 'дарофки', 'Хей', 'хей', 'Прив', 'прив']


def start(update, context):
    current_user = update.effective_user
    conn = sqlite3.connect("Clients.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE  IF NOT EXISTS users
                  (User_id int, First_name text, Last_name text, Balance int, Friends int, Orders int, Inv_key text)""")
    cursor.execute("""SELECT * from users WHERE User_id = ?""", (current_user.id, ))
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute("""INSERT INTO users
                VALUES (?, ?, ?, ?,?, ?, ?)""", 
                  (current_user.id, current_user.first_name, current_user.last_name, 0, 0, 0, None))
        context.bot.send_message(chat_id=current_user.id, 
        text="Важный момент, ты узнал про бота от друга и у тебя есть его ключ?", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
        conn.commit()
        conn.close()
        return FRIEND
    else:
        context.bot.send_message(chat_id=current_user.id, 
            text="Снова привет, ты у нас уже был, всё знаешь) Здоровайся, когда захочешь заказать", reply_to_message_id=update.message.message_id,
            reply_markup=ReplyKeyboardRemove(True))
        return HEY

def friend(update, context):
    current_user = update.effective_user
    if (update.message.text == 'Да'):
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="Вводи его ключ:)", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardRemove(True))
        return ENTERKEY
    elif (update.message.text == 'Нет'):
        context.bot.send_message(chat_id=current_user.id, 
            text="Ну что ж, начнем)\n" + 
                "\nЯ знаю следующие команды:\n/refill - Пополнить балланс \n/balance  - Узнать оставшийся балланс \n" + 
                "/help - Напомнить как со мной общаться \n/key - Напомнить ключ для приглашения друзей" +
                "\n\nТвой ключ - KEY" + str(current_user.id) + "\nЗа каждого друга, присоединившегося к нам по твоему приглашению - " +
                'КОФЕ БЕСПЛАТНО!', reply_markup=ReplyKeyboardRemove(True))
        time.sleep(1)
        filename = 'ImMenu.jpg'
        g = open(filename, 'rb')
        context.bot.send_photo(chat_id=current_user.id, photo = g, caption = 'Теперь меню всегда доступно во вложениях)')
        time.sleep(1)
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="Каждый раз, как захочешь заказать, просто здоровайся со мной)", reply_markup=ReplyKeyboardRemove(True))
        g.close()
        return HEY
    else:
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="Не понял, все таки есть ключ?", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
        return FRIEND


def enterkey(update, context):
    current_user = update.effective_user
    if (update.message.text[:3] != "KEY"):
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="Что-то не так с ключом, попробуем еще раз?", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
        return FRIEND
    try:
        cur_key = int(update.message.text[3:])
        if (cur_key == current_user.id):
            context.bot.send_message(chat_id=update.message.chat_id, 
            text="Свой ключ вводить нечестно! Вернемся и введем ключ друга?", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
            return FRIEND
        conn = sqlite3.connect("Clients.db")
        cursor = conn.execute("SELECT * from users WHERE User_id = ?", (cur_key,))
        data=cursor.fetchall()
        if len(data)!=0:
            inc = 1
            cursor.execute("""UPDATE users SET Friends = Friends + ? WHERE User_id = ?""", (inc, cur_key,))
            cursor.execute("""UPDATE users SET Inv_key = ? WHERE User_id = ?""", ('KEY' + str(cur_key), current_user.id,))
        else:
            conn.commit()
            conn.close()
            context.bot.send_message(chat_id=update.message.chat_id, 
            text="Что-то не так с ключом, попробуем еще раз?", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
        return FRIEND
    except:
        conn.commit()
        conn.close()
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="Что-то не так с ключом, попробуем еще раз?", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
        return FRIEND
    conn.commit()
    conn.close()
    context.bot.send_message(chat_id=current_user.id, 
        text="Ну что ж, начнем)\n" + 
            "\nЯ знаю следующие команды:\n/refill - Пополнить балланс \n/balance  - Узнать оставшийся балланс \n" + 
            "/help - Напомнить как со мной общаться \n/key - Напомнить ключ для приглашения друзей" +
            "\n\nТвой ключ - KEY" + str(current_user.id) + "\nЗа каждого друга, присоединившегося к нам по твоему приглашению - " +
            '**КОФЕ БЕСПЛАТНО**!', reply_markup=ReplyKeyboardRemove(True))
    time.sleep(1)
    filename = 'ImMenu.jpg'
    g = open(filename, 'rb')
    context.bot.send_photo(chat_id=current_user.id, photo = g, caption = 'Теперь меню всегда доступно во вложениях)')
    time.sleep(1)
    context.bot.send_message(chat_id=update.message.chat_id, 
        text="Теперь каждый раз, как захочешь заказать, просто здоровайся со мной)", reply_markup=ReplyKeyboardRemove(True))
    return HEY

def help(update, context):
    KeyboardButton(text = '/')
    context.bot.send_message(chat_id=update.message.chat_id, text="Всё, что тебе нужно знать - это как начать разговор, а это легко - просто 'привет'" +
        "\n\nКакие команды я знаю?\n/refill - Пополнить балланс \n/balance  - Узнать оставшийся балланс \n" + 
        "/help - Напомнить как со мной общаться \n/key - Напомнить ключ для приглашения друзей\n" +
        "/start - Если на 'Привет' я молчу, нужно перезапустить меня", reply_to_message_id=update.message.message_id,
         reply_markup=ReplyKeyboardRemove(True))
    return HEY


def refill(update, context):
    KeyboardButton(text = '/')
    current_user = update.effective_user
    context.bot.send_message(chat_id=current_user.id, text="Приступаем к пополнению баланса) Сколько внесем?", reply_to_message_id=update.message.message_id,
        reply_markup=ReplyKeyboardMarkup([['300', '400', '500'], ['600', '700', '800'], ['900', '1000', '1500']]))
    return REFILL2

def refill2(update, context):
    KeyboardButton(text = '/')
    current_user = update.effective_user
    try:
        summ = int(update.message.text)
    except:
        context.bot.send_message(chat_id=current_user.id, text="Что-то не так с суммой, попробуй сначала", 
            reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardRemove(True))
        return HEY
    conn = sqlite3.connect("Clients.db")
    cursor = conn.execute("SELECT Balance from users WHERE User_id = ?", (current_user.id,))
    data=cursor.fetchall()
    if len(data)==1:
        try:
            #оплата на sum
            #payment_func(sum)
            cursor.execute("""UPDATE users SET Balance = Balance + ? WHERE User_id = ?""", (summ, current_user.id,))
            context.bot.send_message(chat_id=current_user.id, text="Всё супер, пополнили на " + summ + "₽", 
                reply_markup=ReplyKeyboardRemove(True))
            conn.commit()
            conn.close()
            return HEY
        except:
            context.bot.send_message(chat_id=current_user.id, text="Технические неполадочки,  /refill для повтора",
                reply_markup=ReplyKeyboardRemove(True))
            conn.commit()
            conn.close()
            return HEY
    else:
        context.bot.send_message(chat_id=current_user.id, text="Технические неполадочки", reply_markup=ReplyKeyboardRemove(True))
        conn.commit()
        conn.close()
        return HEY       
    return HEY

def balance(update, context):
    KeyboardButton(text = '/')
    current_user = update.effective_user
    conn = sqlite3.connect("Clients.db")
    cursor = conn.cursor()
    cursor = conn.execute("SELECT Balance from users WHERE User_id = ?", (current_user.id,))
    data=cursor.fetchall()
    if len(data)==0:
         context.bot.send_message(chat_id=current_user.id, text="Ваш балланс пока что пуст(\n/refill - пополнение балланса",
         reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardRemove(True))
    elif len(data)==1:
        #data[0][0] = str(int(data[0][0]) + int(update.message.text))
        context.bot.send_message(chat_id=current_user.id, text="Ваш балланс: " + str(data[0][0]) + " р.", 
            reply_to_message_id=update.message.message_id,)
    else:
        #Ошибка в бд  
        context.bot.send_message(chat_id=current_user.id, text="Технические неполадочки, сообщите в кофейню, все исправим",
        reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardRemove(True))   
        return HEY   
    conn.commit()
    conn.close()
    return HEY    

def key(update, context):
    KeyboardButton(text = '/')
    current_user = update.effective_user
    context.bot.send_message(chat_id=current_user.id, text="Ваш персональный ключ для приглашения друзей: KEY" + str(current_user.id),
    reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardRemove(True))
    return HEY



######################################################################################
def hey(update, context):
    KeyboardButton(text = '/')
    current_user = update.effective_user
    context.user_data.clear()
    context.user_data['amount'] = '0'
    context.user_data['user_id'] = current_user.id
    context.user_data['user_name'] = current_user.first_name
    context.user_data['user_surname'] = current_user.last_name
    if (update.message.text in Greeting):
        context.bot.send_sticker(chat_id=update.message.chat_id, sticker = random.choice(stickers_hi))
        context.bot.send_message(chat_id=current_user.id, text='Привет! Уже бежишь или еще больше десяти минут?', 
            reply_markup=ReplyKeyboardMarkup([['Бегу'], ['Медленно бегу']]))
        return CHOOSE
    else:
        context.bot.send_message(chat_id=current_user.id, 
            text='Пока ты не поздороваешься, я не буду ничего делать!', reply_markup=ReplyKeyboardRemove(True))
        return HEY

def choose(update, context):
    current_user = update.effective_user
    if (update.message.text == 'Бегу'):
        current_time = datetime.datetime.now()
        minute = current_time.minute
        hrs = current_time.hour
        '''if (hrs >= 21):
            context.bot.send_message(chat_id=current_user.id, 
            text= 'К сожалению, кофейня уже закрыта:(\nВозвращайся с утра!', reply_markup=ReplyKeyboardRemove(True))
            return HEY
        if (hrs <= 5 or hrs ==6 and minute <50):
            context.bot.send_message(chat_id=current_user.id, 
            text= 'К сожалению, кофейня еще закрыта:(\nВозвращайся с утра!', reply_markup=ReplyKeyboardRemove(True))
            return HEY'''
        context.user_data['ttime'] = 'now'
        context.bot.send_message(chat_id=current_user.id, 
            text='Для начала, что из этого?', reply_markup=ReplyKeyboardMarkup(Categories))
        return COFF
    elif (update.message.text == 'Медленно бегу'):
        current_time = datetime.datetime.now()
        minute = current_time.minute
        hrs = current_time.hour
        if (hrs >= 21 or hrs <=5):
            context.bot.send_message(chat_id=current_user.id, 
            text= 'К сожалению, кофейня уже закрыта:(\nВозвращайся с утра!', reply_markup=ReplyKeyboardRemove(True))
            return HEY
        if (hrs == 6):
            hrs = 7
            mints = 0
        if (minute < 15):
            mints= 15
        elif (minute >= 15 and minute < 30):
            mints = 30
        elif (minute >= 30 and minute < 45):
            mints  = 45
        elif (minute >= 45):
            mints = 0
            hrs+=1
        print_time = current_time.replace(minute = mints, hour = hrs)
        quarter_time = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=15, hours=0, weeks=0)
        buttons1 = []
        buttons2 = []
        for i in range (4):
            for j in range (4):
                if (print_time.minute < 10):
                    min_to_print = '0'+ str(print_time.minute)
                else:
                    min_to_print = str(print_time.minute)
                buttons1.append(str(print_time.hour) + ':' + min_to_print)
                print_time = print_time + quarter_time
                if (print_time.hour == 21):
                    break
            buttons2.append(buttons1[:])
            buttons1.clear()
            if (print_time.hour == 21):
                break
        context.user_data['butTime'] = buttons2
        context.bot.send_message(chat_id=current_user.id, 
            text='Во сколько будешь?:)', 
            reply_markup=ReplyKeyboardMarkup(buttons2))
        return TENSE
    else:
        context.bot.send_message(chat_id=current_user.id, 
            text="Давай начнём сначала, дело не в тебе, дело во мне. Поздаровайся со мной еще раз(", reply_markup=ReplyKeyboardRemove(True))
        return HEY


def tense(update, context):
    current_user = update.effective_user
    context.user_data['ttime'] = update.message.text
    ind = 0
    for i in range (len(context.user_data['butTime'])): 
        IN = context.user_data['ttime'] in context.user_data['butTime'][i]
        if (IN):
            ind = 1
    if not (ind):
        context.bot.send_message(chat_id=current_user.id, 
            text="Давай начнём сначала, что-то не так. Снова скажи 'привет'", reply_markup=ReplyKeyboardRemove(True))
        return HEY
    '''context.bot.send_message(chat_id=current_user.id, 
            text=menu)
    context.bot.send_message(chat_id=current_user.id, 
            text='Выбирай)', reply_markup=ReplyKeyboardMarkup(menuList))'''
    context.bot.send_message(chat_id=current_user.id, 
        text='Для начала, что из этого?', reply_markup=ReplyKeyboardMarkup(Categories))
    return COFF


def coff(update, context):
    current_user = update.effective_user
    IN = False
    for c_name in Categories:
        if (update.message.text in c_name):
            IN = True
    if (IN):
        conn = sqlite3.connect("Menu.db")
        cursor = conn.cursor()
        context.user_data['sect_cost' + context.user_data['amount']] = update.message.text
        if (update.message.text == 'Кофе'):
            cursor.execute("""SELECT * from Coffee""")
            Sizes = ['S', 'M', 'L']
        elif (update.message.text == 'Раф'):
            cursor.execute("""SELECT * from Raff""")
            Sizes = ['M', 'L']
        elif (update.message.text == 'Напитки'):
            cursor.execute("""SELECT * from Drinks""")
            Sizes = ['M', 'L']
        elif (update.message.text == 'Фреши'):
            cursor.execute("""SELECT * from Freshs""")
            Sizes = ['S', 'L']
        elif (update.message.text == 'Другое'):
            cursor.execute("""SELECT * from Other""")
            Sizes = ['S', 'L']

        data = cursor.fetchall()
        but = []
        for row in data:
            qua = 0
            siz = ''
            for i in range (len(row) -1):
                if (row[1+i]):
                    qua = qua +1
            if (qua) == 1:
                but.append([row[0]])
            else:
                ep = []
                for i in range (len(row) -1):
                    if (row[1+i]):
                        #siz = siz + Sizes[i] + ' '
                        if context.user_data['sect_cost' + context.user_data['amount']] == 'Напитки':
                            ep.append(row[0] + '(' + Sizes[i] + ')')
                        else:
                            ep.append(row[0] + '.\n' + Sizes[i])
                but.append(ep[:])
                ep.clear()

        context.user_data['butMenu'] = but[:]
        context.bot.send_message(chat_id=current_user.id, 
                text='Ага, дальше)', reply_markup=ReplyKeyboardMarkup(but))
        conn.commit()
        conn.close()
        return DOPS
    else:
        context.bot.send_sticker(chat_id = context.user_data['user_id'], sticker ="CAADAgADRAADpnQoA51VAzSQtaXEFgQ")
        context.bot.send_message(chat_id=current_user.id, 
            text="Не понял, давай еще раз начнем с 'привет'", reply_markup=ReplyKeyboardRemove(True))
        return HEY

def dops(update, context):
    current_user = update.effective_user
    IN = False
    for butMenu_name in context.user_data['butMenu']:
        if (update.message.text in butMenu_name):
            IN = True
    if (IN):
        context.bot.send_message(chat_id=current_user.id, 
             text='Сироп, топпинг, еще эспрессо? ', 
             reply_markup=ReplyKeyboardMarkup(butDops))
        if 'S' in update.message.text:
           context.user_data['ssize' + context.user_data['amount']] = 'S'
           context.user_data['coffee' + context.user_data['amount']] = update.message.text[:-3]
        elif 'M' in update.message.text:
           context.user_data['ssize' + context.user_data['amount']] = 'M'
           context.user_data['coffee' + context.user_data['amount']] = update.message.text[:-3]
        elif 'L' in update.message.text:
           context.user_data['ssize' + context.user_data['amount']] = 'L'
           context.user_data['coffee' + context.user_data['amount']] = update.message.text[:-3]
        else:
           context.user_data['ssize' + context.user_data['amount']] = '-'
           context.user_data['coffee' + context.user_data['amount']] = update.message.text

        conn = sqlite3.connect("Menu.db")
        cursor = conn.cursor()
        if (context.user_data['sect_cost'+ context.user_data['amount']]== 'Кофе'):
            cursor.execute("""SELECT * from Coffee WHERE name = (?)""", 
                (context.user_data['coffee'+ context.user_data['amount']],))
            dictSizes = {'S': 1, 'M': 2 , 'L': 3}
        elif (context.user_data['sect_cost'+ context.user_data['amount']] == 'Раф'):
            cursor.execute("""SELECT * from Raff WHERE name = (?)""", 
                (context.user_data['coffee'+ context.user_data['amount']],))
            dictSizes = {'M': 1 , 'L': 2}
        elif (context.user_data['sect_cost'+ context.user_data['amount']] == 'Напитки'):
            cursor.execute("""SELECT * from Drinks WHERE name = (?)""", 
                (context.user_data['coffee'+ context.user_data['amount']],))
            dictSizes = {'M': 1 , 'L': 2}
        elif (context.user_data['sect_cost'+ context.user_data['amount']] == 'Фреши'):
            cursor.execute("""SELECT * from Freshs WHERE name = (?)""", 
                (context.user_data['coffee'+ context.user_data['amount']],))
            dictSizes = {'S': 1, 'L': 2}
        elif (context.user_data['sect_cost'+ context.user_data['amount']] == 'Другое'):
            cursor.execute("""SELECT * from Other WHERE name = (?)""", 
                (context.user_data['coffee'+ context.user_data['amount']],))
            dictSizes = {'S': 1, 'L': 2}
        data = cursor.fetchall()
        for row in data:
            if context.user_data['ssize' + context.user_data['amount']] == '-':
                for i in range (1, len(row)):
                    if row[i]:
                       context.user_data['cost' + context.user_data['amount']] = row[i]
            else:
                context.user_data['cost' + context.user_data['amount']] = \
                    row[dictSizes[context.user_data['ssize'+ context.user_data['amount']]]]
        return ORDER
    else:
        context.bot.send_sticker(chat_id = context.user_data['user_id'], sticker ="CAADAgADRAADpnQoA51VAzSQtaXEFgQ")
        context.bot.send_message(chat_id=current_user.id, 
            text="Не понял, давай еще раз начнем с приветствия", reply_markup=ReplyKeyboardRemove(True))
        return HEY


def order(update, context):
    context.user_data['cost_extra' + context.user_data['amount']] = 0
    current_user = update.effective_user
    IN = False
    for butDops_name in butDops:
        if (update.message.text in butDops_name):
            IN = True
    if (IN):
        context.user_data['add' + context.user_data['amount']] = update.message.text
        if (update.message.text == 'Сироп'):
            context.user_data['cost_extra' + context.user_data['amount']] = 30
            conn = sqlite3.connect("Menu.db")
            cursor = conn.cursor()
            cursor.execute("""SELECT * from syrups""")
            data = cursor.fetchall()
            butSyr = []
            for row in data:
                butSyr.append([row[0]])
            context.bot.send_message(chat_id=current_user.id, 
                 text='Какой?', reply_markup=ReplyKeyboardMarkup(butSyr))
            conn.commit()
            conn.close()
            butSyr.clear()

        elif (update.message.text == 'Что-то свое, сейчас напишу'):
            context.user_data['add' + context.user_data['amount']] = '-'
            context.user_data['cost_extra' + context.user_data['amount']] = 0
            context.bot.send_message(chat_id=current_user.id, 
                 text='Ждем комментариев)', reply_markup=ReplyKeyboardRemove(True))

        elif (update.message.text == 'Топпинг'):
            context.user_data['cost_extra' + context.user_data['amount']] = 30
            context.bot.send_message(chat_id=current_user.id, 
                 text='Какой?', reply_markup=ReplyKeyboardRemove(True))

        elif (update.message.text == 'Ничего не надо'):
            context.user_data['cost_extra' + context.user_data['amount']] = 0
            context.user_data['add' + context.user_data['amount']] = ''
            context.user_data['com' + context.user_data['amount']] = ''
            context.user_data['cost_fin' + context.user_data['amount']] = \
                context.user_data['cost_extra' + context.user_data['amount']] + \
                    context.user_data['cost' + context.user_data['amount']]
            context.bot.send_message(chat_id=current_user.id, 
                    text="Это весь заказ или возьмешь еще напитки?", 
                        reply_markup=ReplyKeyboardMarkup([['Это весь заказ'], ['Еще']]))

            return PRINTRESULT

        elif (update.message.text == 'На альтернативном молоке'):
            context.user_data['cost_extra' + context.user_data['amount']] = 70
            context.bot.send_message(chat_id=current_user.id, 
                 text='На каком?', reply_markup=ReplyKeyboardMarkup([['Овсяное'], ['Кокосовое']]))

        else:
            context.user_data['cost_extra' + context.user_data['amount']] = 30
            context.user_data['com' + context.user_data['amount']] = ''
            context.user_data['cost_fin' + context.user_data['amount']] = \
                context.user_data['cost_extra' + context.user_data['amount']] + \
                    context.user_data['cost' + context.user_data['amount']]
            context.bot.send_message(chat_id=current_user.id, 
                    text="Это весь заказ или возьмешь еще напитки?", 
                        reply_markup=ReplyKeyboardMarkup([['Это весь заказ'], ['Еще']]))

            return PRINTRESULT

        return COMMENT
    else:
        context.bot.send_sticker(chat_id = context.user_data['user_id'], sticker ="CAADAgADRAADpnQoA51VAzSQtaXEFgQ")
        context.bot.send_message(chat_id=current_user.id, 
            text="Не понял, давай еще раз начнем с приветствия'", reply_markup=ReplyKeyboardRemove(True))
        return HEY

def comment(update, context):
    current_user = update.effective_user
    context.user_data['com' + context.user_data['amount']] = update.message.text
    if (context.user_data['com'+ context.user_data['amount']] == '.' or 
            context.user_data['add' + context.user_data['amount']] in 
                ['Сгущенное молоко', 'Маршмеллоу', 'Еще эспрессо', 'Ничего не надо']):
        context.user_data['com' + context.user_data['amount']] = ''
    context.user_data['cost_fin' + context.user_data['amount']] = \
        context.user_data['cost_extra' + context.user_data['amount']] +context.user_data['cost' + context.user_data['amount']]

    context.bot.send_message(chat_id=current_user.id, 
            text="Это весь заказ или возьмешь еще напитки?", reply_markup=ReplyKeyboardMarkup([['Это весь заказ'], ['Еще']]))

    return PRINTRESULT

def printresult(update, context):
    current_user = update.effective_user
    if (update.message.text == 'Это весь заказ'):
        finprint = 'Заказ:\n'
        printcost = 'Стоимость: \n'
        printfincost = 0
        finprint = ''
        for counter in range (int(context.user_data['amount'])+1):
            if context.user_data['ssize' + str(counter)] != '-':
                final = context.user_data['coffee' + str(counter)] + '  (' +context.user_data['ssize' + str(counter)] + ')'
            else:
                final =context.user_data['coffee' + str(counter)]
            if context.user_data['add' + str(counter)] == 'Сироп' or context.user_data['add' + str(counter)] == 'Топпинг':
                final = final + ' + ' +context.user_data['add' + str(counter)] + ' ' +context.user_data['com' + str(counter)]
            elif context.user_data['add' + str(counter)] == '-': 
                if context.user_data['com' + str(counter)] != '.':
                    final = final + ' + ' + ' (' +context.user_data['com' + str(counter)] + ')'
            elif context.user_data['add' + str(counter)]:
                final = final + ' + ' + context.user_data['add' + str(counter)]
            finprint += final + '\n'  
            printcost += str(context.user_data['cost' + str(counter)]) + '₽ + ' + \
                str(context.user_data['cost_extra' + str(counter)]) + '₽ \n'
            printfincost += int(context.user_data['cost_fin' + str(counter)])

        context.bot.send_message(chat_id=current_user.id, text= finprint + printcost + ' = ' + str(printfincost) + '₽' +
                '\nВсе верно?', reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
        return PAY
        
    elif (update.message.text == 'Еще'):
        context.user_data['amount'] = str(int(context.user_data['amount']) + 1)
        context.bot.send_message(chat_id=current_user.id, 
        text='Хорошо, выбираем второй напиток)\nДля начала, что из этого?', reply_markup=ReplyKeyboardMarkup(Categories))
        return COFF

    else:
        context.bot.send_sticker(chat_id = context.user_data['user_id'], sticker ="CAADAgADRAADpnQoA51VAzSQtaXEFgQ")
        context.bot.send_message(chat_id=current_user.id, 
             text="Тогда начнем сначала, снова скажи 'Привет'", reply_markup=ReplyKeyboardRemove(True))
        return HEY



def pay(update, context):
    current_user = update.effective_user

    if (update.message.text == 'Да' or update.message.text == 'да'):
        #try:
            #Пилим оплату на take_pay рублей
        take_pay = 0
        for counter in range (int(context.user_data['amount']) +1):
            take_pay += int(context.user_data['cost_fin' + str(counter)])
        print ('take_pay', take_pay)
        #payment_func(take_pay)'''
        end(context)
        return HEY
        #except:
            #context.bot.send_message(chat_id=current_user.id, 
            #    text='Не прошла, давай попробуем оплалить еще раз?', reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
            #return PAY
    else:
        context.bot.send_sticker(chat_id = context.user_data['user_id'], sticker ="CAADAgADRAADpnQoA51VAzSQtaXEFgQ")
        context.bot.send_message(chat_id=current_user.id, 
             text="Тогда начнем сначала, снова поздаровайся со мной)", reply_markup=ReplyKeyboardRemove(True))
        return HEY


def end(context):
    global number
    context.user_data['order_num'] = number[-1]

    context.bot.send_message(chat_id= context.user_data['user_id'],  
        text='Твой номер: ' + str(context.user_data['order_num']) + '\nЖдём тебя :)', reply_markup=ReplyKeyboardRemove(True))

    context.bot.send_sticker(chat_id = context.user_data['user_id'], sticker = random.choice(stickers_by))

    for counter in range (int(context.user_data['amount'])+1):        
        print ('Order: ',context.user_data['coffee' + str(counter)])
        print ('Size: ',context.user_data['ssize' + str(counter)] )
        print('Add: ',context.user_data['add' + str(counter)])
        print('Comment: ',context.user_data['com' + str(counter)])
        print ('Price: ',context.user_data['cost_fin' + str(counter)])

        conn2 = sqlite3.connect("List.db")
        cursor2 = conn2.cursor()
        cursor2.execute("""CREATE TABLE  IF NOT EXISTS list
                (User_id int, First_name text, Last_name text, 
                num int, coffee text, 
                ttime text, size text, 
                addit text, comment text, price int)""")
        cursor2.execute("""INSERT INTO list
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (context.user_data['user_id'], context.user_data['user_name'], context.user_data['user_surname'],
                    context.user_data['order_num'],context.user_data['coffee' + str(counter)], 
                    context.user_data['ttime'], context.user_data['ssize' + str(counter)],
                    context.user_data['add' + str(counter)],
                    context.user_data['com' + str(counter)], 
                    context.user_data['cost_fin' + str(counter)]))
        conn2.commit()
        conn2.close()        

        conn3 = sqlite3.connect("DayReport.db")
        cursor3 = conn3.cursor()
        cursor3.execute("""CREATE TABLE  IF NOT EXISTS report 
                (User_id int, First_name text, Last_name text, 
                num int, coffee text, 
                ttime text, size text, 
                addit text, comment text, price int)""")
        cursor3.execute("""INSERT INTO report
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (context.user_data['user_id'], context.user_data['user_name'], context.user_data['user_surname'],
                    context.user_data['order_num'],context.user_data['coffee' + str(counter)], 
                    context.user_data['ttime'], context.user_data['ssize' + str(counter)],
                    context.user_data['add' + str(counter)],
                    context.user_data['com' + str(counter)], 
                    context.user_data['cost_fin' + str(counter)]))
        conn3.commit()
        conn3.close()        

        conn = sqlite3.connect("Clients.db")
        cursor = conn.cursor()
        inc = 1
        cursor.execute("""UPDATE users SET Orders = Orders + ? WHERE User_id = ?""", (inc, context.user_data['user_id'],))

    cursor = conn.execute("SELECT Orders from users WHERE User_id = ?", (context.user_data['user_id'],))
    data=cursor.fetchall()
    if data == 1:
        cursor = conn.execute("SELECT Inv_key from users WHERE User_id = ?", (context.user_data['user_id'],))
        curkey=cursor.fetchall()
        if (curkey):
            context.bot.send_message(chat_id=int(curkey[3:]), 
                text='Ура, бесплатный кофе!\nПокажите сообщение баристе и получите подарок за приглашенного друга', 
                    reply_markup=ReplyKeyboardRemove(True))
    conn.commit()
    conn.close() 
    number.append(number[-1]+1)
    return HEY
    '''else:
        context.bot.send_message(chat_id=current_user.id, 
        text='Тогда начнем сначала, снова скажи "Привет"', reply_markup=ReplyKeyboardRemove(True))
        coffee = 'Nothing'
        ttime = 'now'
        ssize = '-'
        add = '-'
        comment = ''
        cost = 0
        cost_extra = 0
        butMenu.clear()
        return HEY'''




def cancel(update, context):

    return ConversationHandler.END

def unknown(update, context):
    if update.message.text == '/start':
        context.bot.send_message(chat_id=update.effective_user.id, text="С возвращением) привет?", 
            reply_markup=ReplyKeyboardRemove(True))
    else:
        context.bot.send_message(chat_id=update.effective_user.id, text="Таааак, такой команды я не знаю", 
            reply_markup=ReplyKeyboardRemove(True))

def main():

    update = Updater(token=tg_token, use_context=True)
    dp = update.dispatcher

    CommandList = [CommandHandler('refill', refill), CommandHandler('help', help), CommandHandler('balance', balance), 
        CommandHandler('key', key)]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            FRIEND: [MessageHandler(Filters.text, friend)] + CommandList,

            ENTERKEY: [MessageHandler(Filters.text, enterkey)] + CommandList,

            HEY: [MessageHandler(Filters.text, hey)] + CommandList,

            CHOOSE: [MessageHandler(Filters.text, choose)] + CommandList,

            COFF: [MessageHandler(Filters.text, coff)] + CommandList,

            TENSE: [MessageHandler(Filters.text, tense)] + CommandList,

            DOPS: [MessageHandler(Filters.text, dops)] + CommandList,

            ORDER: [MessageHandler(Filters.text, order)] + CommandList,

            COMMENT: [MessageHandler(Filters.text, comment)] + CommandList,

            PRINTRESULT: [MessageHandler(Filters.text, printresult)] + CommandList,

            PAY: [MessageHandler(Filters.text, pay)] + CommandList,

            #END: CommandList,

            REFILL2: [MessageHandler(Filters.text, refill2)] + CommandList
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)


    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    update.start_polling()
    update.idle()
    #update.stop()

if __name__ == '__main__':
    main()