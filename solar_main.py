1# coding: utf-8
# license: GPLv3

import pygame as pg
from solar_vis import *
from solar_model import *
from solar_input import *
from solar_objects import *
import solar_compile
import solar_reader
import thorpy
import time
import numpy as np
from tkinter import filedialog
import os
import pandas
timer = None
reading=False
alive = True
years_compile, days_compile, hours_compile, minutes_compile, seconds_compile=0,0,0,0,0
perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 1.0
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""
max_distance = 0
shifting=False
def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global model_time
    global displayed_time
    recalculate_space_objects_positions([dr.obj for dr in space_objects], delta)
    model_time += delta
def read(time):
    solar_reader.get_objects_position([dr.obj for dr in space_objects],time)

def get_time_passed(time):
    measures=[60,60,24,365]
    units=['sec','min','hours','days','years']
    i=0
    measured_time=[]
    while i<4 and time//measures[i]>0:
        measured_time.append(time%measures[i])
        time//=measures[i]
        i+=1
    if time>0:
        measured_time.append(time)
    s='passed'
    for i in range(len(measured_time)):
        s=(str(measured_time[i]) if len(str(measured_time[i]))==2 or i>2 else '0'+str(measured_time[i]))+' '+units[i]+' '+s
    return s
    
        

def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True

def pause_execution():
    global perform_execution
    perform_execution = False

def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global alive
    alive = False

def open_file():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global browser
    global model_time
    global max_distance
    global reading
    try:
        reading=False
        model_time = 0.0
        in_filename = filedialog.askopenfilename()   
        space_objects = read_space_objects_data_from_file(in_filename)
        max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects])
        calculate_scale_factor(max_distance, True)
    except Exception as e:
        print(e)
def compile_file():
    global space_objects
    global browser
    global model_time
    global max_distance
    global years_compile
    global days_compile
    global hours_compile
    global minutes_compile
    global seconds_compile
    #try:
    modeling_time = int(seconds_compile.get_value()) + int(minutes_compile.get_value())*60 + int(hours_compile.get_value())*60*60 + int(days_compile.get_value())*60*60*24 + int(years_compile.get_value())*60*60*24*365
    in_filename = filedialog.askopenfilename().split('/')[-1]  
    space_objects = read_space_objects_data_from_file(in_filename)
    name=in_filename[:in_filename.index('.')]
    df=solar_compile.calculate_space_objects([dr.obj for dr in space_objects],modeling_time,0)
    files=[]
    for filename in os.listdir():
        files.append(filename)
    print(files)
    file=name+'_movement.csv'
    print(file)
    if files.count(file)==0:
        db=open(file,'w')
        df.to_csv(path_or_buf=db,index=False)
        db.close()
    else:
        i=1
        while files.count(file+f'({i})')>0:
            i+=1
        db=open(file+f'({i})','w')
        df.to_csv(path_or_buf=db,index=False)
        db.close()
    print('Compiled!')
    #except Exception as e:
        #print(e)
def read_file():
    global space_objects
    global browser
    global model_time
    global max_distance
    global reading
    try:
        reading=True
        modeling_time = 0
        in_filename = filedialog.askopenfilename().split('/')[-1]
        move_filename = filedialog.askopenfilename().split('/')[-1]
        space_objects = read_space_objects_data_from_file(in_filename)
        max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects])
        calculate_scale_factor(max_distance, True)
        solar_reader.init(move_filename)
    except Exception as e:
        print(e)
def handle_events(events, menu):
    global alive
    global max_distance
    global shifting
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive = False
        elif event.type == pg.MOUSEWHEEL:
            if event.y==-1:
                max_distance*=1.1
            elif event.y==1:
                max_distance/=1.1 
            calculate_scale_factor(max_distance, False)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and (event.pos[0]>258 or event.pos[1]>175):
            shifting=True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            shifting=False
def slider_to_real(val):
    return np.exp(val)

def slider_reaction(event):
    global time_scale
    time_scale = slider_to_real(event.el.get_value())

def init_ui(screen):
    global browser
    help(thorpy.Inserter)
    slider = thorpy.SliderX(100, (0, 16), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    timer = thorpy.OneLineText("Seconds passed")

    button_load = thorpy.make_button(text="Load a file", func=open_file)

    button_compile = thorpy.make_button(text="Compile a model", func=compile_file)

    button_read = thorpy.make_button(text="Read a file", func=read_file)
    
    compile_message1 = thorpy.OneLineText("Compile for:")
    years_input = thorpy.Inserter(name='years',value="0")
    days_input = thorpy.Inserter(name='days',value="0")
    hours_input = thorpy.Inserter(name='hours',value="0")
    minutes_input = thorpy.Inserter(name='min',value="0")
    seconds_input = thorpy.Inserter(name="sec",value="0")
    box = thorpy.Box(elements=[
        slider,
        button_pause, 
        button_stop, 
        button_play, 
        button_load,
        button_read,
        button_compile,
        compile_message1,
        years_input,
        days_input,
        hours_input,
        minutes_input,
        seconds_input,
        timer])
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id":thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)
    
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0,0))
    box.blit()
    box.update()
    return menu, box, timer,years_input,days_input,hours_input,minutes_input,seconds_input

def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global perform_execution
    global timer
    global shifting
    global years_compile
    global days_compile
    global hours_compile
    global minutes_compile
    global seconds_compile
    global reading
    global model_time
    
    print('Modelling started!')
    physical_time = 0

    pg.init()
    width = 1000
    height = 760
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer,years_compile, days_compile, hours_compile, minutes_compile, seconds_compile = init_ui(screen)
    perform_execution = False

    while alive:
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution:
            if not reading:
                execution((cur_time - last_time) * time_scale)
            else:
                model_time+=(cur_time - last_time) * time_scale
                read((cur_time - last_time) * time_scale)
            text = get_time_passed(int(model_time))
            timer.set_text(text)
            timer.set_location((0.01,0.43), func='set_topleft', state=0)
        last_time = cur_time
        drawer.update(space_objects, box, shifting)

    print('Modelling finished!')
    pg.quit()
if __name__ == "__main__":
    main()
