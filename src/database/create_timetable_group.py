#!/usr/bin/env python3

import sys, warnings
import sqlite3

warnings.simplefilter('always')


def main(argv=sys.argv):

    # Создаем массив дней недели 
    day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


    # Введенные значения
    print(f'Вы ввели {argv[1]}')

    conn = sqlite3.connect(r'timetable.db')
    db = conn.cursor()

    # Создаем таблицу
    db.execute(f"""CREATE TABLE IF NOT EXISTS '{argv[1]}' ( week_day INTEGER, honest_week TEXT, odd_week TEXT, type_honest TEXT, type_odd TEXT, classroom_honest TEXT, classroom_odd TEXT, start_time TEXT);""")
    conn.commit()
    print(f"CREATE TABLE IF NOT EXISTS '{argv[1]}' ( week_day INTEGER, honest_week TEXT, odd_week TEXT, type_honest TEXT, type_odd TEXT, classroom_honest TEXT, classroom_odd TEXT, start_time TEXT);")

    # Наполняем таблицу
    # for i in range(7):
    #     db.execute(f"""INSERT INTO '{argv[1]}' ('week_day', 'honest_week', 'odd_week', 'start_time') VALUES ({i+1}, '{day_of_week[i]}_honest_{argv[1]}', '{day_of_week[i]}_odd_{argv[1]}', '18:50:00');""")
    #     conn.commit()
    #     db.execute(f"""INSERT INTO '{argv[1]}' ('week_day', 'honest_week', 'odd_week', 'start_time') VALUES ({i+1}, '{day_of_week[i]}_honest_{argv[1]}', '{day_of_week[i]}_odd_{argv[1]}', '20:30:00');""")
    #     conn.commit()
    #     print(f"INSERT INTO '{argv[1]}' ('week_day', 'honest_week', 'odd_week', 'start_time') VALUES ({i+1}, '{day_of_week[i]}_honest_{argv[1]}', '{day_of_week[i]}_odd_{argv[1]}', 'num', '18:50:00');")
    #     print(f"INSERT INTO '{argv[1]}' ('week_day', 'honest_week', 'odd_week', 'start_time') VALUES ({i+1}, '{day_of_week[i]}_honest_{argv[1]}', '{day_of_week[i]}_odd_{argv[1]}', 'num', '20:30:00');")
        


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <input_name_of_group>\n".format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())