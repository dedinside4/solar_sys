# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet
from solar_vis import DrawableObject

def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return [DrawableObject(obj) for obj in objects]


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.

    Входная строка должна иметь слеюущий формат:

    <type> <name> <R> <color> <real_radius> <m> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.

    Пример строки:

    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.

    **star** — объект звезды.
    """
    a=line.split()
    star.name=a[1]
    star.R=float(a[2])
    star.color=a[3]
    star.real_radius=float(a[4])
    star.m=float(a[5])
    star.x=float(a[6])
    star.y=float(a[7])
    star.Vx=float(a[8])
    star.Vy=float(a[9])
  # FIXME: допишите парсер

def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Входная строка должна иметь слеюущий формат:

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.

    Пример строки:

    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.

    **planet** — объект планеты.
    """
    a=line.split()
    planet.name=a[1]
    planet.R=float(a[2])
    planet.color=a[3]
    planet.real_radius=float(a[4])
    planet.m=float(a[5])
    planet.x=float(a[6])
    planet.y=float(a[7])
    planet.Vx=float(a[8])
    planet.Vy=float(a[9])
 # FIXME: допишите парсер

def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.

    Строки должны иметь следующий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла

    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            print(out_file, "%s %d %s %f" % ('1', 2, '3', 4.5))
            s=obj.type.capitalize()+' '+str(obj.R)+' '+obj.color+' '+str(obj.m)+' '+str(obj.x)+' '+str(obj.y)+' '+str(obj.Vx)+' '+str(obj.Vy)+'/n'
            out_file.write(s)
        out_file.close()


if __name__ == "__main__":
    print("This module is not for direct call!")
