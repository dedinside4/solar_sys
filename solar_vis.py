# coding: utf-8
# license: GPLv3

import pygame as pg

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие гaрафические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 1000
"""Ширина окна"""

window_height = 760
"""Высота окна"""

offset_x = 0

offset_y = 0

scale_factor = 1
"""Масштабирование экранных координат по отношению к физическим.

Тип: float

Мера: количество пикселей на один метр."""
standart_factor = 1

def calculate_scale_factor(max_distance,init):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
    global standart_factor
    global scale_factor
    global offset_x
    global offset_y
    lsc = scale_factor
    xm,ym=pg.mouse.get_pos()
    x=(xm-window_width/2)/lsc-offset_x
    y=(ym-window_height/2)/lsc-offset_y
    scale_factor = 0.5*min(window_height, window_width)/max_distance
    if init:
        standart_factor = scale_factor
    else:
        offset_x=(xm-window_width/2)/scale_factor-x
        offset_y=(ym-window_height/2)/scale_factor-y
    #print('Scale factor:', scale_factor)


def scale_x(x):
    """Возвращает экранную **x** координату по **x** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **x** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Параметры:

    **x** — x-координата модели.
    """

    return int((x+offset_x)*scale_factor)+window_width/2


def scale_y(y):
    """Возвращает экранную **y** координату по **y** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Параметры:

    **y** — y-координата модели.
    """
    return  int((y+offset_y)*scale_factor)+window_height/2

font_name=pg.font.match_font('times new roman')
def draw_text(screen,text,c,size=14,color=(255,255,255)):
    font=pg.font.Font(font_name,size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.center=c
    screen.blit(text_surface,text_rect)

if __name__ == "__main__":
    print("This module is not for direct call!")


class Drawer:
    def __init__(self, screen):
        self.screen = screen


    def update(self, figures, ui, shifting):
        global offset_x
        global offset_y
        self.screen.fill((0, 0, 0))
        if shifting:
            dx,dy=pg.mouse.get_rel()
            offset_x+=dx/scale_factor
            offset_y+=dy/scale_factor
        for figure in figures:
            figure.draw(self.screen)
        
        ui.blit()
        ui.update()
        pg.display.update()


class DrawableObject:
    def __init__(self, obj):
        self.obj = obj

    def draw(self, surface):
        #print(scale_x(self.obj.x),scale_y(self.obj.y))
        pg.draw.circle(surface, self.obj.color,(scale_x(self.obj.x),scale_y(self.obj.y)),max(self.obj.real_radius*scale_factor,max(1,min(self.obj.R,self.obj.R*scale_factor/standart_factor))))
        draw_text(surface,self.obj.name,(scale_x(self.obj.x),scale_y(self.obj.y)+max(14,2*self.obj.R)),color=self.obj.color)
