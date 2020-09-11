from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import KeyboardButton
import datetime
import time
import random
import time
import requests 
from bs4 import BeautifulSoup 

#import sqlite3
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

tg_token = '1147665814:AAGvNAF1VRq0_5D-WMr0lb_xhJ3mr6Ervr8'

ARTPIZDA, GUEST, WAIT= range (3)
stickers_hi = ["CAACAgIAAxkBAAIBMV9ajyo--yj5YxKCVDOkWKlS1kWIAAImAQACJMLGNoLQFfyDhhAiGwQ", "CAACAgEAAxkBAAIBOV9akmQqocqllOHaneCA7o4EDHUBAAKEAQAC2guxHluGqtjJthcRGwQ",
"CAACAgEAAxkBAAIBOl9akmXul49wF3x8bJecAe-ELmcKAAKFAQAC2guxHqdVnqa0KuIQGwQ", "CAACAgEAAxkBAAIBO19akmV2sifaD4RNkTBt9orCl-3oAAKGAQAC2guxHuILe2NTDD6lGwQ",
 "AACAgEAAxkBAAIBPF9akmYDAAHUlgGuww9goHXCtvin8QAChwEAAtoLsR4p3Rai1J4kXhsE", "CAACAgEAAxkBAAIBPV9akmaLhrQObGF0ZHAN7i6a9hdWAAKIAQAC2guxHhddgvVvaFQ0GwQ",
  "CAACAgEAAxkBAAIBPl9akmgerw_N6HESxWUsL31Csjv3AAKJAQAC2guxHotTshMtrV94GwQ", "CAACAgEAAxkBAAIBP19akmnY6miC_-JW5F2XQu6QyRl_AAKKAQAC2guxHvb5JoaDUTj6GwQ",
   "CAACAgEAAxkBAAIBQF9akmmT4QbIsJCD-OfJoUJfsKU4AAKLAQAC2guxHndHvV3xMd2yGwQ", "CAACAgEAAxkBAAIBQV9akmpESiljj1q4T4cMZZ2xsEOyAAKMAQAC2guxHnKJS4xX7_YTGwQ",
    "CAACAgEAAxkBAAIBQl9akmokpn51MvHOJbkDJPhCXr8DAAKNAQAC2guxHnkFFtdWSOTtGwQ"]
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



def start(update, context):
    current_user = update.effective_user
    if current_user.username == "Aw69some" or current_user.username == "requesterror":
        filename = 'Up.jpg'
        g = open(filename, 'rb')
        context.bot.send_photo(chat_id=current_user.id, photo = g, caption = 'Этот чувак поздавляет тебя с ДНЁМ РОЖДЕНИЯ!!!')
        time.sleep(1)
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="Короч я буду присылать тебе иногда ахуенные советы, гороскопы, мудрые мысли или картинки членов... ладно без последнего", reply_markup=ReplyKeyboardRemove(True))
        context.bot.send_message(chat_id=current_user.id, 
        text="Тебе нравится?", reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']]))
        return ARTPIZDA
    else:
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="ХА! Хотел обмануть меня? Ты нихуя не Артём. -10 баллов Гриффиндору!!!", reply_markup=ReplyKeyboardRemove(True))
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="Лааадно, тебе тоже можно кой-что сделать, пиши мне чо хочешь, присылай картинки, они будут сразу отправляться Артёму \n Анонимно!! Кто пришлет сиськи, тому +5 баллов", reply_markup=ReplyKeyboardRemove(True))
        return GUEST

def artpizda(update, context):
    current_user = update.effective_user
    if (update.message.text == 'Да'):
        context.bot.send_message(chat_id=update.message.chat_id, 
            text="Пизда!!!!)", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardRemove(True))
    elif (update.message.text == 'Нет'):
        context.bot.send_message(chat_id=current_user.id, 
            text="Ну и ладно, мне похуй", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardRemove(True))
    context.bot.send_message(chat_id=current_user.id, 
            text="Только важный вопрос \nЕсли придёт Майли Сайрус и скажет: Или ты покупаешь хорька или всё?", reply_markup=ReplyKeyboardMarkup([['Всё']]))
    return WAIT


def wait(update, context):
    current_user = update.effective_user
    context.bot.send_message(chat_id=update.message.chat_id, 
            text="Ну теперь точно все выяснили, теперь просто жди чего-нибудь", reply_to_message_id=update.message.message_id, reply_markup=ReplyKeyboardRemove(True))
    while (True):
        current_time = datetime.datetime.now()
        print (current_time.hour)
        if current_time.hour == 23:
            url='https://horo.mail.ru/prediction/virgo/today/'
            resp=requests.get(url) 
            horoscope = ''
            if resp.status_code==200:  
                soup=BeautifulSoup(resp.text,'html.parser')     
          
                l=soup.find("div",{"class":"article__item article__item_alignment_left article__item_html"}) 
               
                for note in l:
                    horoscope = horoscope + '\n' + (str(note)[3:-4])
            else: 
                print("Error") 
                continue
            hello = ["ВрЕмЯ гОросКОПОв", "ГАРАСКОПЧИКИ", "чо там по звездам седня?", "Меркурий то сегодня че покажет", "звезды не врут....."]
            #context.bot.send_sticker(chat_id=update.message.chat_id, sticker = random.choice(stickers_hi))
            context.bot.send_message(chat_id=current_user.id, 
                text=random.choice(hello), reply_markup=ReplyKeyboardRemove(True))

            context.bot.send_sticker(chat_id=update.message.chat_id, sticker = random.choice(stickers_hi))
            context.bot.send_message(chat_id=current_user.id, 
                text=horoscope, reply_markup=ReplyKeyboardRemove(True))
        time.sleep(60*32)

def guest(update, context):
    current_user = update.effective_user
    Mes = update.message
    context.bot.send_message(chat_id=current_user.id, 
            text="Окей, я понял, будет доставлено!", reply_markup=ReplyKeyboardRemove(True))
    '''print (Mes.photo)
    #y_photo = update.message.photo
    #y_document = update.message.document
    #y_voice = update.message.voice
    #y_sticker = update.message.sticker 
    #y_text = update.message.text
    for ph in Mes.photo:
        #y_photo = ph.get_file
        print (Mes.forward_from)
        try:
            context.bot.send_photo(chat_id=708316082, photo = ph, caption = 'Этот чувак поздавляет тебя с ДНЁМ РОЖДЕНИЯ!!!')
            #context.bot.send_message(chat_id= 708316082, 
            #    text=y_text,  photo = y_photo,  reply_markup=ReplyKeyboardRemove(True))
            #document = y_document, voice = y_voice, sticker = y_sticker,
        except:
            print ("!") '''
    context.bot.send_message(chat_id= 708316082, 
               text=y_text,  reply_markup=ReplyKeyboardRemove(True))
    return GUEST

def cancel(update, context):

    return ConversationHandler.END

def unknown(update, context):
    if update.message.text == '/start':
        context.bot.send_message(chat_id=update.effective_user.id, text="Я блять уже стартовал, не тыкай сто раз", 
            reply_markup=ReplyKeyboardRemove(True))
    else:
        context.bot.send_message(chat_id=update.effective_user.id, text="Хуй знает, че ты хочешь", 
            reply_markup=ReplyKeyboardRemove(True))

def main():

    update = Updater(token=tg_token, use_context=True)
    dp = update.dispatcher

    '''CommandList = [CommandHandler('refill', refill), CommandHandler('help', help), CommandHandler('balance', balance), 
        CommandHandler('key', key)]'''

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ARTPIZDA: [MessageHandler(Filters.text, artpizda)],

            GUEST: [MessageHandler(Filters.text, guest)],

            WAIT: [MessageHandler(Filters.text, wait)] 

            #+ CommandList, ENTERKEY: [MessageHandler(Filters.text, enterkey)] + CommandList,

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)


    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    update.start_polling()
    #update.idle()
    update.stop()

if __name__ == '__main__':
    main()