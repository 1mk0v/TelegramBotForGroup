#!/bin/env python3
# vim:tabstop=4:shiftwidth=4:expandtab:ai:

from ast import arg
from re import S
import sys, warnings, string
from tokenize import group
from dataclasses import replace
from bs4 import BeautifulSoup 
import sqlite3

def main(argv=sys.argv):

    print(f'Вы ввели {argv[1]}')

    response = open(f'groups/{argv[1]}.html', 'r')
    soup = BeautifulSoup(response, 'lxml')
    lesson = soup.find_all('td')

    def sort(line):
        pip = True
        while pip:
            if chr(32)*2 in line:
                line = line.replace(chr(32)*2, chr(32))
            else:
                pip = False            
        return line

    conn = sqlite3.connect(r"chats.db")
    db = conn.cursor()
    db.execute("SELECT * FROM groups;")
    groups = db.fetchall()

    flag = False
    for i in groups:
        print(i[0])
        if i[0] == argv[1]:
            flag = True
            break
    
    if flag == False:
        print("NONE")
        db.execute(f"INSERT INTO groups (name) VALUES ('{argv[1]}');")
        conn.commit()
        print(f"INSERT INTO groups (name) VALUES ('{argv[1]}');")
    else:
        print("ALREADY INSERTED")
    conn.close()

    
    teacher = []
    classroom = []
    parity = []
    l_type = []
    lesson_name = []
    time = []
    week_day = 0
    
    for i, j  in enumerate(lesson):
        if (i+1)%6 == 0:
            line = j.text
            if line != "Еженедельно" and line != "Преподаватель":
                teacher.append(sort((line).upper()))
            elif line == "Преподаватель":
                week_day = week_day + 1
                    
        elif i == 10 or (i-10)%6 == 0:
            line = j.text
            if line != "Аудитория" and line != "День самостоятельной работы":
                classroom.append(sort((line).upper()))

        elif i == 9 or (i-9)%6 == 0:
            line = j.text
            if line != "Периодичность занятий" and line != "Суббота":
                if "ЗНАМ." in sort((line).upper()):
                    parity.append("20")
                elif "ЧИСЛ." in sort((line).upper()):
                    parity.append("10")
                elif "ЗНАМЕНАТЕЛЬ" in sort((line).upper()):
                    parity.append("2")
                elif "ЧИСЛИТЕЛЬ" in sort((line).upper()):
                    parity.append("1")
                elif "ЕЖЕНЕДЕЛЬНО" in sort((line).upper()):
                    parity.append("0")
                elif line == "":
                    parity.append("NONE")
                else:
                    parity.append(sort((line).upper()))
                    

        elif i == 8 or (i-8)%6 == 0:
            line = j.text
            if line != "Вид занятий" and line != "Знаменатель":
                if line in "Практические занятия /семинар/":
                    l_type.append("ПРАКТИЧЕСКИЕ ЗАНЯТИЯ")
                else:
                    l_type.append(sort((line).upper()))

        elif i == 7 or (i-7)%6 == 0:
            line = j.text
            if line != "Наименование дисциплины" and line != "День самостоятельной работы":
                lesson_name.append((sort((line).upper()), week_day))

        elif i%6 == 0:
            line = j.text
            if line != "Время занятий" and line != "Среда":
                time.append(sort(line))

        


    # print(len(teacher))
    # print(len(сlassroom))
    # print(len(parity))
    # print(len(l_type))
    # print(len(lesson_name))
    # print(len(time))

    # # ВЫВОД ТАБЛИЦЫ
    # for i in range(len(teacher)):
    #     print(time[i], lesson_name[i], l_type[i], parity[i], classroom[i], teacher[i])

    # for i in range(len(teacher)):
    #     print(parity[i])

    # Сортировка по четности и нечетности недели

    # for i in range(len(parity)):
    #     if "ЗНАМ." in parity[i]:
    #         print(time[i], lesson_name[i], l_type[i], "20", classroom[i], teacher[i])
    #     elif "ЧИСЛ." in parity[i]:
    #         print(time[i], lesson_name[i], l_type[i], "10", classroom[i], teacher[i])
    #     elif "ЗНАМЕНАТЕЛЬ" in parity[i]:
    #         print(time[i], lesson_name[i], l_type[i], "2", classroom[i], teacher[i])
    #     elif "ЧИСЛИТЕЛЬ" in parity[i]:
    #         print(time[i], lesson_name[i], l_type[i], "1", classroom[i], teacher[i])
    #     elif "ЕЖЕНЕДЕЛЬНО" in parity[i]:
    #         print(time[i], lesson_name[i], l_type[i], "0", classroom[i], teacher[i])
    #     elif parity[i] == "":
    #         print("NONE")
    #     else: 
    #         print(parity[i])


    conn = sqlite3.connect(r'timetable.db')
    db = conn.cursor()



    # СОЗДАНИЕ/ДОБАВЛЕНИЕ УЧИТЕЛЕЙ В БАЗУ ДАННЫХ
    teacher_table = []
    for i in range(len(teacher)):
        if (teacher[i], argv[1]) not in teacher_table and teacher[i] != "":
            teacher_table.append((teacher[i], argv[1]))

    try:
        db.execute(f"CREATE TABLE teacher (id INTEGER, name TEXT, j_title TEXT TEXT NOT NULL DEFAULT ('NONE'), department_name TEXT NOT NULL DEFAULT ('NONE'), group_name TEXT, url_photo TEXT NOT NULL DEFAULT ('database/photo_of_teacher/default.jpg'), PRIMARY KEY(id));")
        conn.commit()
        print(f"CREATE TABLE teacher (id INTEGER, name TEXT, j_title TEXT TEXT NOT NULL DEFAULT ('NONE'), department_name TEXT NOT NULL DEFAULT ('NONE'), group_name TEXT, url_photo TEXT NOT NULL DEFAULT ('database/photo_of_teacher/default.jpg'), PRIMARY KEY(id));")
    except:
        db.execute(f"SELECT name, group_name from teacher;")
        db_teach_table = db.fetchall() 
        for i in teacher_table:
            flag = False
            for j in db_teach_table:
                if i == j:
                    flag = True
                    break
            if flag == False: 
                db.execute(f"INSERT INTO teacher ('name', 'group_name') VALUES ('{i[0]}', '{i[1]}');")
                conn.commit()
                print(f"INSERT INTO teacher ('name', 'group_name') VALUES ('{i[0]}', '{i[1]}');")
            else:
                print("ALREADY INSERTED TO TEACHER")
        print("SUCCESS INSERTING TO TEACHERS")

        db.execute(f"SELECT id, name from teacher;")
        db_teach_table = db.fetchall()


    # СОЗДАНИЕ/ДОБАВЛЕНИЕ ДИСЦИПЛИН В БАЗУ ДАННЫХ
    try:
        lesson_table = []
        for i in range(len(lesson_name)):
            for j in db_teach_table:
                flag = False
                if teacher[i] == j[1]:
                    flag = True
                    teacher_id = str(j[0])
                    break
            if flag == True:
                if (lesson_name[i][0], l_type[i], teacher_id) not in lesson_table:
                    lesson_table.append((lesson_name[i][0], l_type[i], teacher_id))
            else:
                if (lesson_name[i][0], l_type[i], "NONE") not in lesson_table:
                    lesson_table.append((lesson_name[i][0], l_type[i], "NONE"))
    except:
        print("NO INFO IN TEACHER TABLE")


    try: 
        db.execute(f"CREATE TABLE lessons (id INTEGER, name TEXT, type TEXT, teacher_id TEXT NOT NULL DEFAULT ('NONE'), PRIMARY KEY(id));")
        conn.commit()
        print(f"CREATE TABLE lessons (id INTEGER, name TEXT, type TEXT, teacher_id TEXT NOT NULL DEFAULT ('NONE'), PRIMARY KEY(id));")
    except:
        db.execute(f"SELECT name, type, teacher_id from lessons;")
        db_lesson_table = db.fetchall()
        for i in lesson_table:
            flag = False
            for j in db_lesson_table:
                if i == j:
                    flag = True
                    break
            if flag == False:
                db.execute(f"INSERT INTO lessons ('name', 'type', 'teacher_id') VALUES ('{i[0]}', '{i[1]}', '{i[2]}');")
                conn.commit()
                print(f"INSERT INTO lessons ('name', 'type', 'teacher_id') VALUES ('{i[0]}', '{i[1]}', '{i[2]}');")
            else:
                print("ALREADY INSERTED TO LESSONS")
        print("SUCCESS INSERTING TO LESSONS")



    try: 
        db.execute(f"CREATE TABLE '{argv[1]}' (week_day INTEGER, lesson_id TEXT, classroom TEXT, parity TEXT, time TEXT);")
        conn.commit()
        print(f"CREATE TABLE '{argv[1]}' (week_day INTEGER, lesson_id TEXT, classroom TEXT, parity TEXT, time TEXT);")
    except:
        print(f"ALREADY CREATE {argv[1]} TABLE")
        for i in range(len(lesson_name)):
            db.execute(f"SELECT id from lessons where name = '{lesson_name[i][0]}' and type = '{l_type[i]}';")
            lesson_id = db.fetchone()
            db.execute(f"INSERT INTO '{argv[1]}' ('week_day', 'lesson_id', 'classroom', 'parity', 'time') VALUES ('{lesson_name[i][1]}', '{lesson_id[0]}', '{classroom[i]}', '{parity[i]}', '{time[i]}');")
            conn.commit()
            print(f"INSERT INTO '{argv[1]}' ('week_day', 'lesson_id', 'classroom', 'parity', 'time') VALUES ('{lesson_name[i][1]}', '{lesson_id[0]}', '{classroom[i]}', '{parity[i]}', '{time[i]}');")
            

    # СДЕЛАТЬ ПРОВЕРКУ НА НАЛИЧИЕ ТОЧНО ТАКОГО ЖЕ РАСПИСАНИЯ

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <input_html_of_group>\n".format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())