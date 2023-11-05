import math
from PIL import Image, ImageDraw
from PyQt5 import QtGui

from MainClasses import *
from WriteAndReadFilesFunctions import planet_classes


def create_angle(first, second):
    planets = planet_classes()  # список планет
    parent = None
    if first == second:  # заменение строчек классами
        raise SamePlanet('укажите разные планеты')
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
    if first == second:
        raise SamePlanet('Укажите разные планеты')
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
        raise DifferentParent('укажите планеты с одинаковым "родителем"')

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
