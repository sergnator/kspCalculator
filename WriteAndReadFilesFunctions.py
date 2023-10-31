import os
import datetime
import sqlite3
from MainClasses import Planet
from Constans import DATABASE


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


def add_to_db_new_planet(planet: Planet):
    con = sqlite3.connect(DATABASE + 'planets.db')
    cur = con.cursor()
    cur.execute(
        f"insert into planets.db (name, g, atnosphere, secondSpaceSpeed, color, parent, alt VALUES ({planet.name}, {planet.g}, {planet.atmosphere}, {planet.secondspacespeed}, {planet.color}, {planet.parent}, {planet.alt})")
    con.commit()
    con.close()
