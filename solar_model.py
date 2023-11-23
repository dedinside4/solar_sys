# coding: utf-8
# license: GPLv3
import math
gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    fx=0
    fy=0
    for obj in space_objects:
        if body == obj:
            continue
        r = math.sqrt((body.x - obj.x)**2 + (body.y - obj.y)**2)
##        if r<=obj.r+body.r and obj.type!='star':
##            space_objects.remove(obj)
##            p1y=body.Vy*body.m
##            p2y=obj.Vy*obj.m
##            p1x=body.Vx*body.m
##            p2x=obj.Vx*obj.m
##            body.m+=obj.m
##            body.Vy=(p1y+p2y)/bod
        f=obj.m*body.m*gravitational_constant/r**2
        an=math.atan2(obj.y-body.y,obj.x-body.x)
        fx+=f*math.cos(an)
        fy+=f*math.sin(an)
    body.Fx=fx
    body.Fy=fy

def move_space_object(body, t,space_objects):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    x,y = body.x,body.y  # FIXME: Вывести формулы для ускорения, скоростей и координат
    Fx,Fy=body.Fx,body.Fy
    ax = body.Fx/body.m
    ay = body.Fy/body.m
    i=1
    dt1=t/i
    oldvx=body.Vx
    oldvy=body.Vy
    oldax=ax
    olday=ay
    body.Vx+=ax*dt1
    body.Vy+=ay*dt1
    body.x+=body.Vx
    body.y+=body.Vy
    i+=1
    while abs((body.Vx-oldvx)/body.vx)>0.07 and abs((body.Vy-oldvy)/body.vy)>0.07 and abs((body.Vy-oldvy)/body.vy)>0.07 and abs((body.Vy-oldvy)/body.vy)>0.07:
        dt=t/i
        body.Vx=oldvx+ax*dt
        body.Vy=oldvy+ay*dt
        i+=1
        body.x+=body.Vx
        body.y+=body.Vy
        oldax=body.Fx/body.m
        olday=body.Fy/body.m
        calculate_force(body,space_objects)

def recalculate_space_objects_positions(space_objects, t):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    for body in space_objects:
        fx,fycalculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, t, space_objects)


if __name__ == "__main__":
    print("This module is not for direct call!")
