# coding: utf-8
# license: GPLv3
import math
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import root_scalar
import pandas
gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_acceleration(x,y,m):
    """Вычисляет силу, действующую на тела.
    """

    Ax=[]
    Ay=[]
    for j in range(len(x)):
        r = np.sqrt((x[j] - x)**2 + (y[j] - y)**2)
        a=m*gravitational_constant/r**2
        an=np.arctan2(y-y[j],x-x[j])
        ax=(np.nan_to_num(a*np.cos(an),posinf=0,neginf=0)).sum()
        ay=(np.nan_to_num(a*np.sin(an),posinf=0,neginf=0)).sum()
        Ax.append(ax)
        Ay.append(ay)
    return np.array(Ax),np.array(Ay)
def move_space_objects(t,space_objects):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    min_dt=1000
    maxpe=0.00001
    #calculate_force(body,space_objects)
    #step(body, t)
    vx=np.array([body.Vx for body in space_objects])
    vy=np.array([body.Vy for body in space_objects])
    x=np.array([body.x for body in space_objects])
    y=np.array([body.y for body in space_objects])
    m=np.array([body.m for body in space_objects])
    while t>0:
        ax,ay=calculate_acceleration(x,y,m)
        #print(teylor_min(10**(-18),x,y,vx,vy,ax,ay,m,maxpe),teylor_min(t,x,y,vx,vy,ax,ay,m,maxpe))
        try:
            res=root_scalar(teylor_min, args=(x,y,vx,vy,ax,ay,m,maxpe), bracket=(0,t), x0=t/2, x1=t/4, maxiter=13)
            dt=min(res.root,t)
        except:
            dt=t
        #print(res)
        x,y,vx,vy=teylorpast(x,y,vx,vy,m,ax,ay, dt)
        #cont,ax1,ay1,x1,y1=teylor(dt,x,y,vx,vy,ax,ay,m,maxpe)
        #while cont:
            #dt/=2
            #dt=root_scalar(teylor, args=(x,y,vx,vy,ax,ay,m,maxpe), bracket=(0,dt), x0=dt/2, x1=dt/4, maxiter=13)
            #cont,ax1,ay1,x1,y1=teylor(dt,x,y,vx,vy,ax,ay,m,maxpe)
        #vx=vx+ax*dt
        #vy=vy+ay*dt
        #x,y,ax,ay=x1,y1,ax1,ay1
        t-=dt
    #print('moved')
    for i in range(len(space_objects)):
        space_objects[i].Vx=vx[i]
        space_objects[i].Vy=vy[i]
        space_objects[i].y=y[i]
        space_objects[i].x=x[i]

        
    #print('calculated')
    #print(body.Fx/body.m,body.Fy/body.m,body.Vx,body.Vy,body.x,body.y)
def teylorpast(x,y,vx,vy,m,ax,ay, dt):
    x=x+vx*dt+ax*dt**2/2
    y=y+vy*dt+ay*dt**2/2
    vx=vx+ax*dt
    vy=vy+ay*dt
    return x,y,vx,vy
def teylor(dt,x,y,vx,vy,ax,ay,m,e):
    px=abs(vx/(dt**2)+ax/dt)
    py=abs(vy/(dt**2)+ay/dt)
    x=x+vx*dt+(ax)*(dt**2)/2
    y=y+vy*dt+(ay)*(dt**2)/2
    ax1,ay1=calculate_acceleration(x,y,m)
    return (not (((abs((ax1-ax)/(dt*px))<=e).all() or (px==0).any()) and ((abs((ay1-ay)/(dt*py))<=e).all() or (py==0).any()))),ax1,ay1,x,y
def teylor_min(dt,x,y,vx,vy,ax,ay,m,e):
    px=np.nan_to_num(1/abs(vx/dt+ax),posinf=0,neginf=0)
    py=np.nan_to_num(1/abs(vy/dt+ay),posinf=0,neginf=0)
    x=x+vx*dt+(ax)*(dt**2)/2
    y=y+vy*dt+(ay)*(dt**2)/2
    ax1,ay1=calculate_acceleration(x,y,m)
    return max(max(abs((ax1-ax)*px)-e),max(abs((ay1-ay)*py)-e))
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
