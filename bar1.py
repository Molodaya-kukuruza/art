#import schedule
import time
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler
import logging
import sqlite3
import datetime
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


tg_token = '947027312:AAFVxwkYgVRT2fkd5Ux7ExD9hxlu7-eCMj8'


def start(update, context):
    current_user = update.effective_user
    # (User_id0 int, First_name1 text, Last_name2 text, num3 int, coffee4 text, ttime5 text, size6 text, addit7 text, comment8, price9 )""")
    conn_barmens = sqlite3.connect("Bar.db")
    cursor_barmens = conn_barmens.cursor()
    cursor_barmens.execute("""CREATE TABLE  IF NOT EXISTS barmens
                  (User_id int, First_name text, Last_name text)""")
    cursor_barmens.execute("""SELECT * from barmens WHERE User_id = ?""", (current_user.id, ))
    data = cursor_barmens.fetchall()
    if len(data) == 0:
        cursor_barmens.execute("""INSERT INTO barmens
                VALUES (?, ?, ?)""", 
                  (current_user.id, current_user.first_name, current_user.last_name))
    conn_barmens.commit()
    conn_barmens.close()
    while (True):
        conn_barmens = sqlite3.connect("Bar.db")
        cursor_barmens = conn_barmens.cursor()
        cursor_barmens.execute("""SELECT User_id from barmens""")
        data = cursor_barmens.fetchall()
        bar = []
        for barmens in data:
            bar.append (barmens[0])
        conn = sqlite3.connect("List.db")
        cursor = conn.cursor()
        cursor.execute('SELECT num FROM list GROUP BY num HAVING count(*) > 1')
        seq_num = []
        for elem in cursor.fetchall():
            seq_num.append(elem[0])
        for sn in seq_num:
            cursor.execute('SELECT * from list WHERE num = (?) and ttime = (?)', (sn, 'now', ))
            group = cursor.fetchall()
            if (group):
                client = group[0][1] + ' '+ group[0][2] + ' ' + str(group[0][0]) + '\n'
                when = 'Будет уже сейчас\n'
                num = str(sn)
                result = ''
                for row in group:
                    order = row [4]
                    if (row[6] != '-'):
                        order += ' (' + row[6] + ')   '
                    else:
                        order += '   '
                    dops = ''
                    if (row[7] == '-'):
                        dops += ' + ' + '(' + row[8] + ')'
                    elif (row[7] in ['На альтернативном молоке', 'Сироп', 'Топпинг']):
                        dops += ' + ' + row[7] + ' (' + row[8] + ')'
                    elif (row[7]):
                        dops += ' + ' + row[7]
                    else:    
                        dops += ''
                    result += '•' + order + dops + '\n'
                result += '\n'
                for barmens in bar:
                    try:
                        context.bot.send_message(chat_id=barmens, 
                            text='Заказ от: ' + client +
                                'Заказ: \n'  + result +
                                    'Номер заказа: ' + num + 
                                        '\n\n' + when)
                    except:
                        print(barmens, 'is not available')
                cursor.execute('DELETE FROM list WHERE ttime = (?) and num = (?)', ('now', sn, ))

        cursor.execute('SELECT * FROM list WHERE ttime = (?)', ('now',))
        table = cursor.fetchall()
        for row in table:
            client = row[1] + ' '+ row[2] + ' ' + str(row[0]) + '\n'
            when = 'Будет уже сейчас\n'
            num = str(row[3])
            order = row [4]
            if (row[6] != '-'):
                order += ' (' + row[6] + ')   '
            else:
                order += '   '
            dops = ''
            if (row[7] == '-'):
                dops += ' + ' + '(' + row[8] + ')'
            elif (row[7] in ['На альтернативном молоке', 'Сироп', 'Топпинг']):
                dops += ' + ' + row[7] + ' (' + row[8] + ')'
            elif (row[7]):
                dops += ' + ' + row[7]
            else:    
                dops += ''

            for barmens in bar:
                try:
                    context.bot.send_message(chat_id=barmens, 
                        text='Заказ от: ' + client +
                            'Заказ: \n' + '•' + order + dops + '\n'
                                '\nНомер заказа: ' + num + 
                                    '\n\n' + when)
                except:
                    print(barmens, 'is not available')
        cursor.execute('DELETE FROM list WHERE ttime = (?)', ('now',))
        seq_num.clear()


        current_time = datetime.datetime.now()
        time10 = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=10, hours=0, weeks=0)
        todel = []
        cursor.execute('SELECT num FROM list GROUP BY num HAVING count(*) > 1')
        for elem in cursor.fetchall():
            seq_num.append(elem[0])
        for sn in seq_num:
            cursor.execute('SELECT * FROM list WHERE ttime != (?) and num = (?)', ('now', sn, ))
            group = cursor.fetchall()
            if (group):
                client = group[0][1] + ' '+ group[0][2] + ' ' + str(group[0][0]) + '\n'
                when = 'Будет в ' + group[0][5] + '\n'
                num = str(sn)
                result = ''
                time_split = group[0][5].split(':')
                order_time = current_time.replace(minute = int(time_split[1]), hour = int(time_split[0]))
                if (order_time - time10 <= current_time):
                    todel.append(group[0][5])
                    for row in group:
                        order = row [4]
                        if (row[6] != '-'):
                            order += ' (' + row[6] + ')   '
                        else:
                            order += '   '
                        dops = ''
                        if (row[7] == '-'):
                            dops += ' + ' + '(' + row[8] + ')'
                        elif (row[7] in ['На альтернативном молоке', 'Сироп', 'Топпинг']):
                            dops += ' + ' + row[7] + ' (' + row[8] + ')'
                        elif (row[7]):
                            dops += ' + ' + row[7]
                        else:    
                            dops += ''
                        result += '•' + order + dops + '\n'
                    for barmens in bar:
                        try:
                            context.bot.send_message(chat_id=barmens, 
                                text='Заказ от: ' + client +
                                'Заказ:\n' + result + '\n'
                                    '\nНомер заказа: ' + num + 
                                        '\n\n' + when)
                        except:
                            print(barmens, 'is not available')
        for sn in seq_num:    
            for t in todel:
                cursor.execute('DELETE FROM list WHERE ttime = (?) and num = (?)', (t, sn, ))
        todel.clear()
        seq_num.clear()



        for row in cursor.execute('SELECT * FROM list WHERE ttime != (?)', ('now', )):
            time_split = row[5].split(':')
            order_time = current_time.replace(minute = int(time_split[1]), hour = int(time_split[0]))
            if (order_time - time10 <= current_time):
                todel.append(row[5])
                client = row[1] + ' '+ row[2] + ' ' + str(row[0]) + '\n'
                when = 'Будет в ' + row[5] + '\n'
                num = str(row[3])
                order = row [4]
                if (row[6] != '-'):
                    order += ' (' + row[6] + ')   '
                else:
                    order += '   '
                dops = ''
                if (row[7] == '-'):
                    dops += ' + ' + ' (' + row[8] + ')'
                elif (row[7] in ['На альтернативном молоке', 'Сироп', 'Топпинг']):
                    dops += ' + ' + row[7] + ' (' + row[8] + ')'
                elif (row[7]):
                    dops += ' + ' + row[7]
                else:
                    dops += ''

                for barmens in bar:
                    try:
                        context.bot.send_message(chat_id=barmens,
                            text='Заказ от: ' + client +
                                'Заказ: \n' + '•' + order + dops + '\n'
                                    '\nНомер заказа: ' + num + 
                                        '\n\n' + when)
                    except:
                        print(barmens, 'is not available')

        for t in todel:
            cursor.execute('DELETE FROM list WHERE ttime = (?)', (t,))
        todel.clear()
        seq_num.clear()
        conn.commit()
        conn.close() 
        bar.clear()
        conn_barmens.commit()
        conn_barmens.close()

        if (current_time.hour >=22 ):
            conn = sqlite3.connect("DayReport.db")
            curs = conn.cursor()
            curs.execute('SELECT * FROM report')
            dat =curs.fetchall()
            if len(dat) != 0:
                filename = str(current_time.day)+ '_' + str(current_time.month) + '.txt'
                f = open(filename, 'w')
                for row in dat:
                    for i in range(len(row)):
                        f.write(str(row[i]) + '   ')
                    f.write('\n')
                #f.write (dat)
                f.close()
                g = open(filename, 'rb')
                context.bot.send_document(chat_id=current_user.id, document = g)
                g.close()
                os.remove(filename)
            cursor = conn.cursor()
            data = cursor.execute('DELETE FROM report').rowcount    
            conn.commit()
            conn.close() 

        time.sleep(10)
        '''не работать ночью, вроде логично
        if (current_time.hour == 23):
            time.sleep(25 000)'''
    return

def main():
    update = Updater(token=tg_token, use_context=True)
    dp = update.dispatcher

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)
      
    update.start_polling()
    update.idle()
    #update.stop()

if __name__ == '__main__':
    main()