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
##                                         Developed by 1mk0v                                         ##
##                                                                                                    ##
##                                                                                                    ##
########################################################################################################


from asyncio import events
from email import message
from itertools import count
import time
import telebot
from telebot import types
import datetime
import sqlite3
from keyboa import Keyboa
import logging

from yaml import parse




### ВВОДИМ ТОКЕН НАШЕГО БОТА
bot = telebot.TeleBot("5620314916:AAFd2NaaCj02H8Nwek38Rb_ugKZdpqlERe4")

#---------------------------------------------КЛИЕНТСКАЯ ЧАСТЬ------------------------------------------------------#

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


            say_hello = "Я вижу ты у нас впервые)\nДавай знакомиться. Я - Анна. Меня создали в помощь студентам. Из какой ты группы?"
            bot.send_message(message.chat.id, say_hello)
            
            all_groups = []
            for i in chats:
                all_groups.append(i[0])

            kb_groups = Keyboa(items=all_groups)
            bot.send_message(message.chat.id, text=f"Выбери свою группу:", reply_markup=kb_groups())

            flag = False

 
    # Проверяем является ли пользователь старостой
    db.execute(f"SELECT headman from chats where id = {chat_id}")
    headman = db.fetchone()[0]
    conn.close()
    # Добавляем сообщения
    hello_sticker = open('../stickers/hello1.webp', 'rb')
    gen_Hello = f'<b>Привет, {name}.</b>\nМеня зовут Анна. Я ваш главный помощник в институте. ' \
                f'Я быстро учусь и очень скоро смогу вам ответить на все ваши вопросы.'

    if headman == 1:
        print("yes")
        # Инизиализируем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/help")
        btn2 = types.KeyboardButton("/timetable")
        btn3 = types.KeyboardButton("/add_event")
        btn4 = types.KeyboardButton("/add_photo_of_teacher")
        markup.add(btn1, btn2)
        markup.add(btn3)
        markup.add(btn4)
        # Отправляем сообщения приветствия
        bot.send_sticker(message.chat.id, hello_sticker)
        bot.send_message(message.chat.id, gen_Hello, parse_mode='html', reply_markup=markup)
    else:
        # Инизиализируем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/help")
        btn2 = types.KeyboardButton("/timetable")
        btn3 = types.KeyboardButton("/show_event")
        markup.add(btn1, btn2)
        markup.add(btn3)
        # Отправляем сообщения приветствия
        bot.send_sticker(message.chat.id, hello_sticker)
        bot.send_message(message.chat.id, gen_Hello, parse_mode='html', reply_markup=markup)
        print("no")



## ПОМОЩЬ БОТА ПРИ ЗАПРОСЕ
@bot.message_handler(commands=['help'])
def help(message):
    name = message.from_user.first_name
    gen_Help = f'<b>{name}</b>, мой функционал не велик 🙄, но все же что-то я умею 😏\n' \
                f'1️⃣ Я знаю твоё расписание на сегодня 🕖\n' \
                f'2️⃣ Совсем скоро я смогу запоминать объявления старосты.\n' \
                # f'❗️ВНИМАНИЕ❗️ Я очень не люблю, когда меня достают, поэтому смогу сказать тебе о твоем расписании не более трех раз!'
                # f'❗️❗️❗️Если вы староста в своей группе:' \
                # f'1. Напишите моему разработчику он вам даст пароль, с помощью которого я запомню вас как старосту в вашей группе.\n' \
                # f'2. Напишите мне "/ястароста", а дальше следуйте инструкции.' 
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

    def timetable():
        conn = sqlite3.connect(r'database/timetable.db')
        db = conn.cursor()
        db.execute(f"SELECT * from '{what_is_group(chat_id)}' where week_day = {datetime.datetime.today().isoweekday()} and parity = {what_is_day()};")
        tt_info = db.fetchall()
        if tt_info == []:
            db.execute(f"SELECT * from '{what_is_group(chat_id)}' where week_day = {datetime.datetime.today().isoweekday()} and parity = {int(what_is_day()/10)};")
            tt_info = db.fetchall()
        conn.close()
        return tt_info



    # Делаем проверку на выбор группы
    if what_is_group(chat_id) == "NONE":
        bot.send_sticker(message.chat.id, open('../stickers/angry.webp', 'rb'))
        bot.send_message(message.chat.id, "Выбери свою группу!")
        
    else:
        # Подключаемся к бд с расписанием
        conn = sqlite3.connect(r'database/timetable.db')
        db = conn.cursor()
        tt_info = timetable()
            
        if len(tt_info) == 1:
            db.execute(f"SELECT * from '{what_is_group(chat_id)}' where week_day = {datetime.datetime.today().isoweekday()} and parity in ({int(what_is_day()/10)}, 0);")
            tt_info = db.fetchall()
        elif len(tt_info) > 2:
             bot.send_message(message.chat.id, f"Я не научилась точно выводить ваше расписание, но вот что пишут...", parse_mode='html')

        if tt_info == []:
            bot.send_message(message.chat.id, f"<b>{print_message_week(what_is_day())}</b>\n<b>{week_day(datetime.datetime.today().isoweekday())}</b>", parse_mode='html')
            bot.send_message(message.chat.id, f"<b>У вас сегодня выходной!</b>\nВы можете отдохнуть с друзьями, подготовиться вместе к контрольной.", parse_mode='html')
        else:
            bot.send_message(message.chat.id, f"<b>{print_message_week(what_is_day())}</b>\n<b>{week_day(tt_info[0][0])}</b>", parse_mode='html')
            for j,i in enumerate(tt_info):
                db.execute(f"SELECT name, type, teacher_id from lessons where id = {i[1]};")
                info_lesson = db.fetchone()
                lesson_name = info_lesson[0]
                lesson_type = info_lesson[1]
                teacher_id = info_lesson[2]
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton(f'Показать преподавателя', callback_data=f'{teacher_id}')
                markup.add(btn1)
                bot.send_message(message.chat.id, f"{j+1}. {lesson_name}\n\t\t\t\t{lesson_type}\n\t\t\t\t{i[2]}\n\t\t\t\t{i[4]}", reply_markup=markup)
        conn.close()



@bot.message_handler(commands=['show_event'])
def show_event(message):
    conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
    db = conn.cursor()
    db.execute(f"SELECT info, time from events where group_name = (SELECT group_name from chats where id = {message.chat.id})")
    info = db.fetchall()
    for i in info:
        year = int(i[1][0:4:1])
        month = int(i[1][5:7:1])
        day = int(i[1][8:10:1])
        event_time = datetime.date(year, month, day)
        delta = str(datetime.date.today() - event_time)
        if delta[1] == ":":
            delta = 0
        else:
            delta = int(delta[0:2:1])
        db.execute(f"DELETE FROM events where life_end < {delta} and time = '{i[1]}';")
        conn.commit()
    
    db.execute(f"SELECT info, time from events where group_name = (SELECT group_name from chats where id = {message.chat.id})")
    new_info = db.fetchall()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(f"Показать все ({len(new_info)})", callback_data=f'a00000001')
    markup.add(btn1)
    if len(new_info) > 0:
        bot.send_message(message.chat.id, f"Ваше последнее уведомление!", parse_mode='html')
        bot.send_message(message.chat.id, f"<b>{new_info[len(new_info)-1][1]}</b>\n{new_info[len(new_info)-1][0]}", parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"У вас нет уведомлений", parse_mode='html')


#---------------------------------------------АДМИНСКАЯ ЧАСТЬ------------------------------------------------------#

@bot.message_handler(commands=['add_event'])
def main_menu(message):
    conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
    db = conn.cursor()
    db.execute(f"SELECT headman from chats where id = {message.chat.id}")
    bool_headman = db.fetchone()[0]
    conn.close()
    if bool_headman == 1:
        bot.send_message(message.chat.id, f"Здравстуй, <b>{message.from_user.first_name}</b>!\n" \
                                          f"Вы зашли в добавление события, ваша группа сможет спросить их у меня!\n" \
                                          f"Но вы не переживайте я им напомню, что у вас есть объявление)", parse_mode='html')
        bot.send_message(message.chat.id, f"Напишите свое объявление!")
        bot.register_next_step_handler(message, add_event)
    else:
        bot.send_message(message.chat.id, f"Только староста может делать объявления!")

def add_event(message):
    text = message.text
    conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
    db = conn.cursor()
    db.execute(f"INSERT INTO events ('group_name', 'info', 'time') VALUES ((SELECT group_name from chats where id = {message.chat.id}), '{text}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');")
    conn.commit()
    bot.send_message(message.chat.id, f"Я запоминила!")
    db.execute(f"SELECT count(info) from events where group_name = (SELECT group_name from chats where id = {message.chat.id})")
    count = db.fetchone()[0]
    db.execute(f"SELECT id from chats where group_name = (SELECT group_name from chats where id = {message.chat.id})")
    all_chats = db.fetchall()
    for i in all_chats:
        print(i[0])
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(f'Показать все ({count})', callback_data=f'a00000001')
        btn2 = types.InlineKeyboardButton(f'Показать последнее', callback_data=f'a00000002')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(int(i[0]), f"Ваш староста сделал объявление!", reply_markup=markup)
    return


@bot.message_handler(commands=['add_photo_of_teacher'])
def insert_photo(message):

    conn = sqlite3.connect(r'database/chats.db')
    db = conn.cursor()
    db.execute(f"SELECT group_name from chats where id = {message.chat.id};")
    group_name = db.fetchone()[0]
    db.execute(f"SELECT headman from chats where id = {message.chat.id}")
    bool_headman = db.fetchone()[0]
    conn.close()

    if bool_headman == 1:
        conn = sqlite3.connect(r'database/timetable.db')
        db = conn.cursor()
        db.execute(f"SELECT * FROM teacher where group_name = '{group_name}'")
        teachers = db.fetchall()
        conn.close()

        teach_name = []

        for i in teachers:
            if i[5] == 'database/photo_of_teacher/default.jpg':
                teach_name.append({i[1]:('teacher'+str(i[0]))})

                
        
        print(teach_name)
        kb_teach = Keyboa(items=teach_name)
        bot.send_message(message.chat.id, "Какому преподавателю ты хочешь добавить фото?", reply_markup=kb_teach())
    else:
        bot.send_message(message.chat.id, f"Только староста может ставить фотки преподавателям!")
        return

def get_id(teacher_id,call, message):
    bot.send_message(call.message.chat.id, "Отлично, теперь выбери фотографию!")

    


# @bot.message_handler(commands=['add_teacher_of_lesson'])



@bot.message_handler(commands=['ястароста'])
def insert_headman(message):
    bot.send_message(message.chat.id, "Привет!")
    conn = sqlite3.connect(r'database/chats.db')
    db = conn.cursor()
    db.execute(f"SELECT headman FROM chats where group_name in (SELECT group_name FROM chats where id = {message.chat.id});")
    yn = db.fetchone()
    conn.close()
    if 1 in yn:
        bot.send_message(message.chat.id, "У этой группы есть староста!")
    else:
        bot.send_message(message.chat.id, "Введи пароль, который тебе дал мой разработчик!")
        bot.register_next_step_handler(message, get_password)

def get_password(message):
    text = message.text
    conn = sqlite3.connect(r'database/chats.db')
    db = conn.cursor()
    db.execute(f'SELECT passwd FROM groups where name in (SELECT group_name from chats where id = {message.chat.id});')
    passwd = db.fetchone()[0]
    if text == passwd:
        db.execute(f"UPDATE chats set headman = 1 where id = {message.chat.id}")
        conn.commit()
        conn.close()
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('/start')
        markup.add(btn1)
        bot.send_message(message.chat.id, "И правда староста, добро пожаловать, коллега!\nПерезапусти меня и у тебя будет чуть больше возможностей)))", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "ТЫ ВРЕШЬ! ТЫ НЕ СТАРОСТА!")
    return


# Обработчик обычный сообщений
@bot.message_handler()
def get_info(message):

    # Вывод имени отправителя и сообщение в отдельные переменнные 
    name = message.from_user.first_name
    send_message = message.text

    # Сообщения, которые бот понимает
    hello = {'Привет', 'Здарова', 'Hello', 'Здравствуй'}

    # Мониторинг на Приветствие
    if send_message in hello:
        bot.send_message(message.chat.id, f'Здравствуй, {name}!', parse_mode='html')

    elif message.chat.id == 616782548:
        i = 0
        while i<100:
            bot.send_message(message.chat.id, f"{i}. LOVE YOU!")
            print(i)
            i = i+1
        
    # Обработка непонятных сообщений
    else:
        print(message)
        bot.send_sticker(message.chat.id, sticker = open('../stickers/fear.webp', 'rb'))
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


    # Выводит каждому участнику в группе событие
    def send_event(chat_id):
        conn = sqlite3.connect(r'database/chats.db', check_same_thread=True)
        db = conn.cursor()
        db.execute(f"SELECT info, time from events where group_name = (SELECT group_name from chats where id = {chat_id})")
        info = db.fetchall()
        print(info)
        conn.close()
        return info

    try:
        if call.message:
            # print(call.data)
            chat_id = call.message.chat.id
            if call.data in select_group():
                insert_client(chat_id=chat_id, group=f'{call.data}')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.data}", reply_markup=None)
                bot.answer_callback_query(call.id, show_alert=True, text=f"Выбрана группа {call.data}")
            elif call.data == 'a00000001':
                print(len(send_event(chat_id)))
                if len(send_event(chat_id)) == 0:
                    bot.send_message(chat_id, "Пока что у вас нет новых объявлений!")
                else:
                    for i in send_event(chat_id):
                        print(i[0])
                        bot.send_message(chat_id, f"<b>{i[1]}</b>\n{i[0]}", parse_mode="html")
            elif call.data == 'a00000002':
                if len(send_event(chat_id)) != 0:
                    bot.send_message(chat_id, send_event(chat_id)[len(send_event(chat_id))-1])
                else:
                    bot.send_message(chat_id, "Пока что у вас нет объявлений!")

            elif call.data[0:7:1] == 'teacher':
                teacher_id = call.data[7::1]
                bot.register_next_step_handler(call.data, get_id(teacher_id, call))

            else: 
                teacher_id = call.data
                if teacher(teacher_id, group(call)) == "NONE":
                    s_sms = 'Извините, я не знаю этого преподавателя 😢'
                    bot.answer_callback_query(call.id, show_alert=True, text=s_sms)
                else:
                    teacher_data = teacher(teacher_id, group(call))
                    name = teacher_data[0][1]
                    j_title = teacher_data[0][2]
                    url = teacher_data[0][5]

                    text = f'{name}\n{j_title}\n'

                    photo = open(url, 'rb')
                    bot.send_photo(call.message.chat.id, photo, caption=text)
           

    except Exception as e:
        print(repr(e))






# Запуск бота на постоянную основу
bot.infinity_polling(none_stop=False)
