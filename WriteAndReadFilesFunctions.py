import os
import datetime
import sqlite3
from MainClasses import Planet
from Constans import DATABASE

# запись исключений
def write_exception(message):
    now = datetime.datetime.now()
    path = f"crusheslogs\\{now.strftime('%c').replace(':', '.').replace(' ', '_')}.txt"

    if 'crusheslogs' in os.listdir():
        with open(path, 'w', encoding='utf-8') as f:
            f.write(message)
    else:
        os.mkdir('crusheslogs')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(message)

# функция, которая возращает список экземпляров классов
def planet_classes():
    con = sqlite3.connect(DATABASE + 'planets.db')
    cur = con.cursor()
    data = cur.execute("""select * from planets""").fetchall()
    result = []

    for el in data:
        result.append(Planet(*el))
    con.close()
    return result


def __convert(obj):
    if isinstance(obj, bool):
        if obj:
            return str(1)
        return str(0)

    return f"'{obj}'"

# добавления планет в базу данных
def add_obj_in_database(path, data, data_name):
    con = sqlite3.connect(path)
    cur = con.cursor()
    database = path.split('\\')[-1].split('.')[0]
    req = f"insert into {database}\n"
    req += f"({', '.join(data_name)})\n"
    data = map(__convert, data)
    req += f"values ({', '.join(data)})"
    cur.execute(req)
    con.commit()
    con.close()


