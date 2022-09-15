#!/bin/env python3



########################################################################################################
##                                                                                                    ##
##                                                                                                    ##
##                            .S_SSSs     .S_sSSs     .S_sSSs     .S_SSSs                             ##
##                           .SS~SSSSS   .SS~YS%%b   .SS~YS%%b   .SS~SSSSS                            ##
##                           S%S   SSSS  S%S   `S%b  S%S   `S%b  S%S   SSSS                           ##
##                           S%S    S%S  S%S    S%S  S%S    S%S  S%S    S%S                           ##
##                           S%S SSSS%S  S%S    S&S  S%S    S&S  S%S SSSS%S                           ##
##                           S&S  SSS%S  S&S    S&S  S&S    S&S  S&S  SSS%S                           ##
##                           S&S    S&S  S&S    S&S  S&S    S&S  S&S    S&S                           ##
##                           S&S    S&S  S&S    S&S  S&S    S&S  S&S    S&S                           ##
##                           S*S    S&S  S*S    S*S  S*S    S*S  S*S    S&S                           ##
##                           S*S    S*S  S*S    S*S  S*S    S*S  S*S    S*S                           ##
##                           S*S    S*S  S*S    S*S  S*S    S*S  S*S    S*S                           ##
##                           SSS    S*S  S*S    SSS  S*S    SSS  SSS    S*S                           ##
##                                  SP   SP          SP                 SP                            ##
##                                  Y    Y           Y                  Y                             ##
##                                                                                                    ##
##                                                                                                    ##
##                                                                                                    ##
##                                                                                                    ##
##                                                                                                    ##
########################################################################################################




from cgi import print_form
from cgitb import html, text
import time
from tokenize import group
from typing import Text
from pickle import TRUE
import telebot
from telebot import types
import datetime
import sqlite3
from keyboa import Keyboa
from datetime import timedelta
# from lessons import lesson1_evening, lesson2_evening



### ВВОДИМ ТОКЕН НАШЕГО БОТА
bot = telebot.TeleBot("5620314916:AAFd2NaaCj02H8Nwek38Rb_ugKZdpqlERe4")


## НАПОМИНАЛКИ (Не работает, пока что)


# Считаем разницу во времени
# difference_of_time = lesson1_evening - timedelta(hours=datetime.datetime.now().hour, minutes=datetime.datetime.now().minute)


# Создаем функции для отправки оповещений всем пользователям, что запустили бота
# ...


## ПРИВЕТСТВИЕ ПРИ ПОДКЛЮЧЕНИИ
@bot.message_handler(commands=['start'])
def start(message):

    # Получаем id чата 
    chat_id = int(message.chat.id)

    # Инициализируем имя отправителя
    name = message.from_user.first_name

    # Подключаемся к базе данных
    conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
    db = conn.cursor()
    db.execute("SELECT * from chats;")
    chat = db.fetchall()

    # Проверяем chat.id в нашей базе данных
    flag = True
    print(name)    
    while flag == True:
        for id in chat:
            if int(id[0]) == int(chat_id):
                print(f'{id[0]} = {chat_id}')
                flag = False
                break
            else:
                print(f'{id[0]} != {chat_id}')
                print('FALSE')


        # Бот не нашел chat_id у себя, значит его нужно добавить 
        if flag == True:
            db.execute(f"INSERT INTO chats ('id') VALUES ('{chat_id}');")
            conn.commit()
            print(f"INSERT INTO chats ('id') VALUES ('{chat_id}');")
            db.execute("SELECT name from groups;")
            chats = db.fetchall()
            conn.close()


            say_hello = "Я вижу ты у нас впервые)\nДавай знакомиться. Я - Анна. Меня создали в помощь студентам. Из какой ты группы?"
            bot.send_message(message.chat.id, say_hello)
            
            all_groups = []
            for i in chats:
                all_groups.append(i[0])

            kb_groups = Keyboa(items=all_groups)
            bot.send_message(message.chat.id, text=f"Выбери свою группу:", reply_markup=kb_groups())

            flag = False

    time.sleep(4)

    # Добавляем сообщения
    sticker = open('../stickers/hello1.webp', 'rb')
    gen_Hello = f'<b>Привет, {name}.</b>\nМеня зовут Анна. Я ваш главный помощник в институте. ' \
                f'Я быстро учусь и очень скоро смогу вам ответить на все ваши вопросы.'

    # Инизиализируем кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/help")
    btn2 = types.KeyboardButton("/timetable")
    markup.add(btn1, btn2)

    # Отправляем сообщения приветствия
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, gen_Hello, parse_mode='html', reply_markup=markup)  # (кому. что. параметры)    schedule.run_pending()




## ПОМОЩЬ БОТА ПРИ ЗАПРОСЕ
@bot.message_handler(commands=['help'])
def help(message):
    name = message.from_user.first_name
    gen_Help = f'<b>{name}</b>, мой функционал не велик 🙄, но все же что-то я умею 😏\n' \
                f'1. Я буду напоминать тебе о сегодняшних занятиях и отсылать новости 😉\n' \
                f'2. Я знаю твоё расписание на сегодня 🕖' 
    bot.send_message(message.chat.id, gen_Help, parse_mode='html')




## ВЫВОД РАСПИСАНИЯ ПРИ ЗАПРОСЕ
@bot.message_handler(commands=['timetable'])
def timetable(message):

    chat_id = message.chat.id

    # Определение группы
    def what_is_group(id):
        conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
        db = conn.cursor()
        db.execute(f"SELECT group_name from chats where id = {id};")
        group = db.fetchone()
        conn.close()
        return group[0]



    # Определение четности и нечетности недели
    def what_is_day():
        if int(datetime.datetime.now().strftime('%W')) % 2 == 0:
            return 20
        else:
            return 10

    # День недели
    def week_day(tt_info):
        if tt_info == 1:
            week_day = 'ПОНЕДЕЛЬНИК'
        elif tt_info == 2:
            week_day = 'ВТОРНИК'
        elif tt_info == 3:
            week_day = 'СРЕДА'
        elif tt_info == 4:
            week_day = 'ЧЕТВЕРГ'
        elif tt_info == 5:
            week_day = 'ПЯТНИЦА'
        elif tt_info == 6:
            week_day = 'СУББОТА'
        elif tt_info == 7:
            week_day = 'ВОСКРЕСЕНЬЕ'
        return week_day

    # Вывод четной или нечетной недели для пользователя 
    def print_message_week(week):
        if week == 20:
            return 'ЗНАМЕНАТЕЛЬ'
        else:
            return 'ЧИСЛИТЕЛЬ'


    # Проверка на количество пройденных четных недель
    # def check_honest():
    #     count = 0
    #     datetime.timedelta()
    #     return datetime.datetime.now().isoweekday()


    # Делаем проверку на выбор группы
    if what_is_group(chat_id) == "NONE":
        bot.send_message(message.chat.id, "Выбери свою группу!😡")
    else:
        # Подключаемся к бд с расписанием
        conn = sqlite3.connect(r'database/timetable.db')
        db = conn.cursor()
        teacher_id= []
        db.execute(f"SELECT * from '{what_is_group(chat_id)}' where week_day = {datetime.datetime.today().isoweekday()} and parity = {what_is_day()};")
        tt_info = db.fetchall()
        if tt_info == []:
            db.execute(f"SELECT * from '{what_is_group(chat_id)}' where week_day = {datetime.datetime.today().isoweekday()} and parity = {int(what_is_day()/10)};")
            tt_info = db.fetchall()
        if tt_info == []:
            bot.send_message(message.chat.id, f"<b>{print_message_week(what_is_day())}</b>\n<b>{week_day(datetime.datetime.today().isoweekday())}</b>", parse_mode='html')
            bot.send_message(message.chat.id, f"<b>У вас сегодня выходной!</b>\nВы можете отдохнуть с друзьями, подготовиться вместе к контрольной.", parse_mode='html')
            exit()
        elif len(tt_info) == 1:
            db.execute(f"SELECT * from '{what_is_group(chat_id)}' where week_day = {datetime.datetime.today().isoweekday()} and parity in ({int(what_is_day()/10)}, 0);")
            tt_info = db.fetchall()
        elif len(tt_info) > 2:
             bot.send_message(message.chat.id, f"Я не научилась точно выводить ваше расписание, но вот что пишут в расписании", parse_mode='html')
                 
        bot.send_message(message.chat.id, f"<b>{print_message_week(what_is_day())}</b>\n<b>{week_day(tt_info[0][0])}</b>", parse_mode='html')
        for j,i in enumerate(tt_info):
            # db.execute(f"SELECT name FROM parity_settings where id = {i[3]}")
            # parity = db.fetchone()[0]
            db.execute(f"SELECT name, type, teacher_id from lessons where id = {i[1]};")
            info_lesson = db.fetchone()
            lesson_name = info_lesson[0]
            lesson_type = info_lesson[1]
            teacher_id = info_lesson[2]
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(f'Показать преподавателя', callback_data=f'{teacher_id}')
            markup.add(btn1)
            bot.send_message(message.chat.id, f"{j+1}. {lesson_name}\n\t\t\t\t{lesson_type}\n\t\t\t\t{i[2]}\n\t\t\t\t{i[4]}", reply_markup=markup)



# Обработчик обычный сообщений
@bot.message_handler()
def get_info(message):

    def what_is_day():
        if int(datetime.datetime.now().strftime('%W')) % 2 == 0:
            return 'honest_week'
        else:
            return 'odd_week'

    # Вывод имени отправителя и сообщение в отдельные переменнные 
    name = message.from_user.first_name
    send_message = message.text

    # Сообщения, которые бот понимает
    hello = {'Привет', 'Здарова', 'Hello', 'Здравствуй'}
    how_are_you = {'Как ты?', 'как ты?', 'Как ты', 'как ты', 'Как дела?', 'как дела?', 'как дела', 'Как дела'}

    # Мониторинг на Приветствие
    if send_message in hello:
        bot.send_message(message.chat.id, f'Здравствуй, {name}!', parse_mode='html')
    
    elif send_message in how_are_you:
        bot.send_message(message.chat.id, f'Хорошо, а вы как?', parse_mode='html')


    # Расписание на всю неделю (Марк Цысь обещал сделать...)
    elif send_message in 'Покажи расписание на всю неделю':

        # Смотрим расписание в базе данных 
        conn = sqlite3.connect(r'database/timetable.db')
        db = conn.cursor()
        db.execute(f"SELECT week_day, {what_is_day()}, start_time from '2vbASU';")
        all = db.fetchall()
        print(all)
        conn.close()


        # Распарсиваем данные на недели, пары, и время
        week = []
        lesson = []
        time = []
        for timetable in all:
            week.append(timetable[0])
            lesson.append(timetable[1])
            time.append(timetable[2])
        for i in range(14):
            bot.send_message(message.chat.id, f'{week[i]}\n{lesson[i]} {time[i]}', parse_mode='html')

    # Обработка непонятных сообщений
    else:
        bot.send_message(message.chat.id, f'Извините, {name} я вас не понимаю 😥', parse_mode='html')
    
        
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):

    def select_group():
        conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
        db = conn.cursor()
        db.execute("SELECT * from groups;")
        all_info = db.fetchall()
        conn.close()
        chats = []
        for i in all_info:
            chats.append(i[0])
        return chats
    
    #ИНФОРМАЦИЯ о группе
    def group(call):
        chat_id = call.message.chat.id
        conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
        db = conn.cursor()
        db.execute(f"SELECT group_name from chats where id = '{chat_id}';")
        group = db.fetchone()[0]
        conn.close()
        return group


    # ИНФОРМАЦИЯ о преподавателя
    def teacher(id, group):
        conn = sqlite3.connect(r'database/timetable.db', check_same_thread=True)
        db = conn.cursor()
        db.execute(f"SELECT * FROM teacher where id = '{id}' and group_name = '{group}';")
        lesson = db.fetchall()
        if lesson == []:
            db.close()
            return "NONE"
        else: 
            return lesson


    # Добавляет нового пользователя
    def insert_client(chat_id, group):
        conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
        db = conn.cursor()
        db.execute(f"UPDATE chats SET group_name = '{group}' where id = '{chat_id}';")
        conn.commit()
        conn.close()
        print(f"UPDATE chats SET group_name = '{group}' where id = '{chat_id}';")


    try:
        if call.message:
            print(select_group())
            if call.data in select_group():
                chat_id = call.message.chat.id
                insert_client(chat_id=chat_id, group=f'{call.data}')
            else: 
                teacher_id = call.data
                if teacher(teacher_id, group(call)) == "NONE":
                    s_sms = 'Извините, я не знаю этого преподавателя 😢'
                    bot.send_message(call.message.chat.id, s_sms)
                else:
                    teacher_data = teacher(teacher_id, group(call))
                    name = teacher_data[0][1]
                    j_title = teacher_data[0][2]
                    url = teacher_data[0][5]

                    text = f'{name}\n{j_title}\n'

                    photo = open(url, 'rb')
                    bot.send_photo(call.message.chat.id, photo, caption=text)

            # Меняем запрос на более удобный
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Работаю над запросом...", reply_markup=None)
           

    except Exception as e:
        print(repr(e))





# Запуск бота на постоянную основу
bot.polling(none_stop=True)
