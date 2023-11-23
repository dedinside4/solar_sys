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
    calculate_force(body,space_objects)
    while t>0:
        i=1
        dt=t/i
        oldax=body.Fx/body.m
        olday=body.Fy/body.m
        oldvx=body.Vx
        oldvy=body.Vy
        body.Vx+=body.Fx/body.m*dt
        body.Vy+=body.Fy/body.m*dt
        oldx=body.x
        oldy=body.y
        body.x+=body.Vx*dt
        body.y+=body.Vy*dt
        calculate_force(body,space_objects)
        i+=1
        while abs((body.Vx-oldvx)/body.vx)>0.07 and abs((body.Vy-oldvy)/body.vy)>0.07 and abs((body.Fy/body.m-olday)/olday)>0.07 and abs((body.Fx/body.m-oldax)/oldax)>0.07:
            dt=t/i
            body.x=oldx
            body.y=oldy
            calculate_force(body,space_objects)
            body.Vx=oldvx+body.Fx/body.m*dt
            body.Vy=oldvy+body.Fy/body.m*dt
            body.x+=body.Vx
            body.y+=body.Vy
            calculate_force(body,space_objects)
            i+=1
        t-=dt

def recalculate_space_objects_positions(space_objects, t):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    for body in space_objects:
        move_space_object(body, t, space_objects)


if __name__ == "__main__":
    print("This module is not for direct call!")
