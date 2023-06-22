import sqlite3
from datetime import datetime


def add_new_spam(user_id, first_name, text):
    connection = sqlite3.Connection('statistics.db')
    date_data = datetime.now().strftime('%d.%m.%Y %H:%M')
    print('ХУЙ')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO data VALUES({user_id}, '{first_name}', '{text}', '{date_data}', 1)")
    connection.commit()
    connection.close()

def get_statistics():
    string = 'Список переписок с новыми людьми:\n'
    connection = sqlite3.Connection('statistics.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id, first_name, date, banned FROM data")
    data = cursor.fetchall()
    for i in data:
        string += f"\n[{i[1]}](https://web.telegram.org/z/#{i[0]}) {i[2]} "
        if i[3]:
            string += f"⛔"
            string += f' [Разблокировать](https://t.me/userbot434431_bot/start=unblock_{i[0]})'
    return string