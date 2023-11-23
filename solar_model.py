# coding: utf-8
# license: GPLv3
import math
import numpy as np
from scipy.optimize import minimize
import pandas
gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(x,y,m):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    Fx=[]
    Fy=[]
    for j in range(len(x)):
        r = np.sqrt((x[j] - x)**2 + (y[j] - y)**2)
        f=m*m[j]*gravitational_constant/r**2
        an=np.arctan2(y-y[j],x-x[j])
        #print(f,an,f*np.cos(an),np.nan_to_num(f*np.cos(an)))
        fx=(np.nan_to_num(f*np.cos(an),posinf=0,neginf=0)).sum()
        fy=(np.nan_to_num(f*np.sin(an),posinf=0,neginf=0)).sum()
        #print(f*np.cos(an),f*np.sin(an),fy,fx)
        Fx.append(fx)
        Fy.append(fy)
    return np.array(Fx),np.array(Fy)
def move_space_objects(t,space_objects):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    e_speed=0.01
    max_speed_std=20
    max_a_std=0.00000001
    #calculate_force(body,space_objects)
    #step(body, t)
    vx=np.array([body.Vx for body in space_objects])
    vy=np.array([body.Vy for body in space_objects])
    x=np.array([body.x for body in space_objects])
    y=np.array([body.y for body in space_objects])
    m=np.array([body.m for body in space_objects])
    fx,fy=calculate_force(x,y,m)
    while t>0:
        ax=fx/m
        ay=fy/m
        #print(ax,ay)
        minv1=min(min(abs(max_speed_std/ax)),min(abs(max_speed_std/ay)))
        minv2=min(min(vx*e_speed/ax),min(vy*e_speed/ay))
        #mina=minimize(stda,0, args=(x,y,vx,vy,fx,fy,m,max_a_std), bounds=[(0,t)]).x
        #print(minv,mina)
        #print(minimize(stda,0, args=(x,y,vx,vy,fx,fy,m,max_a_std), bounds=[(0,t)]).fun)
        dt=min(max(minv1,minv2),t)#min(minv,mina)
##        oldx=x
##        oldy=y
##        oldvx=vx
##        oldvy=vy
        x,y,vx,vy=teylor(x,y,vx,vy,m,fx,fy,dt)
##        oldfx=fx
##        oldfy=fy
        fx,fy=calculate_force(x,y,m)
##        stdax=abs(fx-oldfx)/m
##        stday=abs(fy-oldfy)/m
##        stdvx=abs(vx-oldvx)
##        stdvy=abs(vy-oldvy)
##        while max(stdax)>max_a_std and max(stday)>max_a_std and max(stdvx)>max_speed_std and max(stdvy)>max_speed_std:
##            dt/=(i+1)
##            x=oldx
##            y=oldy
##            vx=oldvx
##            vy=oldvy
##            fx=oldfx
##            fy=oldfy
##            x,y,vx,vy=teylor(x,y,vx,vy,m,fx,fy,dt)
##            fx,fy=calculate_force(x,y,m)
##            stdax=abs(fx-oldfx)/m
##            stday=abs(fy-oldfy)/m
##            stdvx=abs(vx-oldvx)
##            stdvy=abs(vy-oldvy)
        t-=dt
    for i in range(len(space_objects)):
        space_objects[i].Vx=vx[i]
        space_objects[i].Vy=vy[i]
        space_objects[i].y=y[i]
        space_objects[i].x=x[i]

        
    #print('calculated')
    #print(body.Fx/body.m,body.Fy/body.m,body.Vx,body.Vy,body.x,body.y)
def teylor(x,y,vx,vy,m,fx,fy, dt):
    x=x+vx*dt+(fy/m)*dt**2/2
    y=y+vy*dt+(fy/m)*dt**2/2
    vx=vx+fx/m*dt
    vy=vy+fy/m*dt
    return x,y,vx,vy
def stda(dt,x,y,vx,vy,fx,fy,m,a):
    x=x+vx*dt+(fx/m)*dt**2/2
    y=y+vy*dt+(fy/m)*dt**2/2
    fx1,fy1=calculate_force(x,y,m)
    return max(max(abs((fx1-fx)/m)-a),max(abs((fy1-fy)/m)-a))
def recalculate_space_objects_positions(space_objects, t):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    if len(space_objects)>0:
        move_space_objects( t, space_objects)


if __name__ == "__main__":
    print("This module is not for direct call!")
