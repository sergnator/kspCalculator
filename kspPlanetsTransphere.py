import sqlite3
import math
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtGui

from Constans import *
from MainClasses import *
from WriteAndReadFilesFunctions import planet_classes
from random import randint


def get_part_info(name):
    con = sqlite3.connect(DATABASE + 'objects.db')
    cur = con.cursor()
    data = cur.execute("""select * from objects where name = ?""", (name,)).fetchall()

    con.close()
    return RocketEngine(*data[0])


def delta_v(first, second):
    if second == first:
        return 0
    if second == 'Kerbin':
        first, second = second, first

    con = sqlite3.connect(DATABASE + 'MapDeltaV.db')
    cur = con.cursor()
    data = cur.execute("""select DeltaV from main where End = ?""", second).fetchall()
    return data[0][0]


def create_angle(first, second):
    planets = planet_classes()
    parent = 0
    for el in planets:
        if el.name == first:
            first = el
        elif el.name == second:
            second = el
    for el in planets:
        if el.id == first.parent:
            parent = el

    t_h = math.pi * math.sqrt(math.pow(first.alt + second.alt, 3) / (8 * parent.second_space_speed))
    angle = (180 - math.sqrt(parent.second_space_speed / second.alt) * (t_h / second.alt) * (180 / math.pi)) % 360
    return str(angle)


def draw_angle(first, second, width=1000, height=1000, color=(255, 255, 255), color_text=(0, 0, 0)):
    angle = float(create_angle(first, second))
    im = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(im)
    x = 0
    y = 0

    # определение какакя планета выше, какая ниже
    planets = planet_classes()
    for el in planets:
        if el.name == first:
            first = el
        elif el.name == second:
            second = el
    flag = second.alt < first.alt
    if first.parent != second.parent:
        raise DifferentParent

    # рисует second

    draw.ellipse(((int(0.2 * width), int(0.2 * height)), (int(0.8 * width), int(0.8 * height))),
                 fill=color, outline=color_text)
    if flag:
        draw.ellipse(((int(0.77 * width), int(0.47 * height)), (int(0.83 * width), int(0.53 * height))),
                     fill=first.color)
        draw.text((int(0.77 * width), int(0.53 * height)), first.name, fill=color_text, font_size=20)
    else:
        R = (int(0.2 * height) - int(0.8 * height)) / 2
        x0 = int(0.5 * width)
        y0 = int(0.5 * height)
        x = int(x0 + R * -math.cos(math.radians(angle)))
        y = int(y0 + R * math.sin(math.radians(angle)))

        draw.ellipse([x - 30, y - 30, x + 30, y + 30], fill=second.color)
        draw.text((x - 30, y + 30), second.name, fill=color_text, font_size=20)

    # рисует first

    draw.ellipse(((int(0.3 * width), int(0.3 * height)), (int(0.7 * width), int(0.7 * height))),
                 fill=color, outline=color_text)
    if flag:
        R = (int(0.3 * height) - int(0.7 * height)) / 2
        x0 = int(0.5 * width)
        y0 = int(0.5 * height)
        x = int(x0 + R * -math.cos(math.radians(angle)))
        y = int(y0 + R * math.sin(math.radians(angle)))
        draw.ellipse([x - 30, y - 30, x + 30, y + 30], fill=second.color)
        draw.text((x - 30, y + 30), second.name, fill=color_text, font_size=20)
    else:
        draw.ellipse(((int(0.67 * width), int(0.47 * height)), (int(0.73 * width), int(0.53 * height))),
                     fill=first.color)
        draw.text((int(0.67 * width), int(0.53 * height)), first.name, fill=color_text, font_size=20)

    # рисует кербол
    draw.ellipse(((int(0.45 * width), int(0.45 * height)), (int(0.55 * width), int(0.55 * height))), (238, 210, 2))

    draw.text((int(0.475 * width), int(0.55 * height)), 'kerbol', fill=color_text, font_size=20)

    # линии
    if not flag:
        draw.line(((int(0.5 * width), int(0.5 * height)), (int(0.7 * width), int(0.5 * height))), fill='red', width=2)
    else:
        draw.line(((int(0.5 * width), int(0.5 * height)), (int(0.8 * width), int(0.5 * height))), fill='red', width=2)
    draw.line(((int(0.5 * width), int(0.5 * height)), (x, y)), fill='red', width=2)

    data = im.tobytes("raw", "RGB")
    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(qim)


def draw_map(width=1000, height=1000, color=(255, 255, 255), color_text=(0, 0, 0)):
    # создание системы
    font = ImageFont.truetype(TTF + '21028.ttf', size=16)
    planets = planet_classes()[1:]
    planets1 = []
    for planet in planets:
        if planet.parent == 0:
            planets1.append(planet)
    planets = planets1[:]
    planets = sorted(planets, key=lambda x: x.alt)
    i = 0.3 / len(planets)
    b = 0.9
    im = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(im)
    # x-левый : (0.1, 0.4), y :(0.1, 0.4)
    # x-правый: (0.6, 0.9)
    # draw.ellipse([(1 - b) * width, (1 - b) * height, b * width, b * height], fill=(255, 255, 255), outline=(0, 0, 0))
    randomlist = []
    # b -= i
    # draw.ellipse([(1 - b) * width, (1 - b) * height, b * width, b * height], fill=(255, 255, 255), outline=(0, 0, 0))
    for j in range(len(planets), 0, -1):
        # орбита
        draw.ellipse([(1 - b) * width, (1 - b) * height, b * width, b * height], fill=color,
                     outline=color_text)
        # планета
        angle = randint(0, 360)
        while True:
            if angle in randomlist:
                angle = randint(0, 360)
            else:
                break
        randomlist.append(angle)
        for one in range(angle - 5, angle):
            randomlist.append(one)
        for two in range(angle, angle + 5):
            randomlist.append(two)

        R = (int((1 - b) * height) - int(b * height)) / 2
        x0 = int(0.5 * width)
        y0 = int(0.5 * height)
        x = int(x0 + R * -math.cos(math.radians(angle)))
        y = int(y0 + R * math.sin(math.radians(angle)))
        draw.ellipse([x - 20, y - 20, x + 20, y + 20], fill=planets[j - 1].color)

        # текст
        draw.text((x - 15, y + 20), text=planets[j - 1].name, fill=color_text, font=font)
        b -= i

    # кербол
    draw.ellipse([0.45 * width, 0.45 * height, 0.55 * width, 0.55 * height], 'yellow')
    draw.text((0.486 * width, 0.55 * height), 'Kerbol', fill=color_text, font=font)

    data = im.tobytes("raw", "RGB")
    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(qim)

