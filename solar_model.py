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
def calculate_acceleration_2(rs,m,rt):
    """Вычисляет силу, действующую на тела.
    """
    r=rs-rt
    l=np.linalg.norm(r,axis=1)
    k=m*gravitational_constant/l**3
    a=r*k[:, np.newaxis]
    a=(np.nan_to_num(a,posinf=0,neginf=0)).sum(axis=0)
    #print(a, ' - ускорение')
    #print(rs,rt, ' - координаты всех тел и ускоряемого')
    return a
def move_space_objects(t,space_objects):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    maxpe=0.00001
    vx=np.array([body.Vx for body in space_objects])
    vy=np.array([body.Vy for body in space_objects])
    x=np.array([body.x for body in space_objects])
    y=np.array([body.y for body in space_objects])
    m=np.array([body.m for body in space_objects])
    while t>0:
        ax,ay=calculate_acceleration(x,y,m)
        try:
            res=root_scalar(teylor_min, args=(x,y,vx,vy,ax,ay,m,maxpe), bracket=(10**(-7),t), x0=t/2, x1=t/4)#, maxiter=13)
            dt=res.root
        except Exception as e:
            #print(e)
            dt=t
        x,y,vx,vy=teylor(x,y,vx,vy,m,ax,ay,dt)
        t-=dt
    for i in range(len(space_objects)):
        space_objects[i].Vx=vx[i]
        space_objects[i].Vy=vy[i]
        space_objects[i].y=y[i]
        space_objects[i].x=x[i]
def teylor(x,y,vx,vy,m,ax,ay,dt):
    x=x+vx*dt+ax*dt**2/2
    y=y+vy*dt+ay*dt**2/2
    vx=vx+ax*dt
    vy=vy+ay*dt
    return x,y,vx,vy
def teylor_min(dt,x,y,vx,vy,ax,ay,m,e):
    px=vx/dt+ax/2
    py=vy/dt+ay/2
    l=px**2+py**2
    x=x+vx*dt+(ax)*(dt**2)/2
    y=y+vy*dt+(ay)*(dt**2)/2
    ax1,ay1=calculate_acceleration(x,y,m)
    da=(ax1-ax)**2+(ay1-ay)**2
    #print(dt, ' - время')
    #print(da, ' - изменение ускорения')
    #print(l, ' - какая то фигня')
    return max(da/l)-e**2
def move_space_objects_2(t,stars, planets):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    maxpe=0.0006
    vs=np.array([np.array([body.Vx, body.Vy]) for body in stars])
    rs=np.array([np.array([body.x, body.y]) for body in stars])
    m=np.array([body.m for body in stars])
    if len(planets)>0:
        vp=np.array([np.array([body.Vx, body.Vy]) for body in planets])
        rp=np.array([np.array([body.x, body.y]) for body in planets])
    else:
        vp=np.array([[np.NaN,np.NaN]])
        rp=np.array([[np.NaN,np.NaN]])
    dt=t
    while t>0:
        acs=np.array([])
        for i in range(len(m)):
            a=calculate_acceleration_2(rs,m,rs[i])
            acs=np.append(acs,a)
        acs=np.reshape(acs, (len(m),2), order='C')
        acp=np.array([])
        for i in range(len(rp)):
            a=calculate_acceleration_2(rs,m,rp[i])
            acp=np.append(acp,a)
        acp=np.reshape(acp, (len(rp),2), order='C')
        try:
            res=root_scalar(teylor_min_2, args=(rs,rp,vs,vp,acs,acp,m,maxpe),method='brenth',bracket=[dt,t],rtol=0.0001) #bracket=(10**(-7),dt))#, maxiter=1)
            dt=res.root
        except Exception as e:
            try:
                res=root_scalar(teylor_min_2, args=(rs,rp,vs,vp,acs,acp,m,maxpe),method='brenth',bracket=[0,dt],rtol=0.0001)#, maxiter=1)
                dt=res.root
            except Exception as e:
                #print(e)
                dt=t
        #print(acs)
        rs,vs=teylor_2(rs,vs,acs,dt)
        rp,vp=teylor_2(rp,vp,acp,dt)
        t-=dt
    for i in range(len(stars)):
        stars[i].Vx,stars[i].Vy=vs[i]
        stars[i].x,stars[i].y=rs[i]
    for i in range(len(planets)):
        planets[i].Vx,planets[i].Vy=vp[i]
        planets[i].x,planets[i].y=rp[i]
def teylor_2(r,v,ac,dt):
    r=r+v*dt+ac*(dt**2)/2
    v=v+ac*dt
    return r,v
def teylor_min_2(dt,rs,rp,vs,vp,acs,acp,m,e):
    rs=rs+vs*dt+acs*(dt**2)/2
    acs1=np.array([])
    for i in range(len(m)):
        a=calculate_acceleration_2(rs,m,rs[i])
        acs1=np.append(acs1,a)
    acs1=np.reshape(acs1, (len(m),2), order='C')
    rp=rp+vp*dt+acp*(dt**2)/2
    acp1=np.array([])
    for i in range(len(rp)):
        a=calculate_acceleration_2(rs,m,rp[i])
        acp1=np.append(acp1,a)
    acp1=np.reshape(acp1, (len(rp),2), order='C')
    das=np.linalg.norm(acs1-acs,axis=1)
    dap=np.linalg.norm(acp1-acp,axis=1)
    acs=np.linalg.norm(acs,axis=1)
    acp=np.linalg.norm(acp,axis=1)
    return max(max(np.nan_to_num(das/acs,posinf=0,neginf=0)),max(np.nan_to_num(dap/acp,posinf=0,neginf=0)))-e
def recalculate_space_objects_positions(space_objects, t):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
##    if len(space_objects)>0:
##        move_space_objects(t, space_objects)

    
    if len(space_objects)>0:
        stars=[]
        planets=[]
        for obj in space_objects:
            if obj.type=='star':
                stars.append(obj)
            elif obj.type=='planet':
                planets.append(obj)
        move_space_objects_2(t, stars, planets)   

if __name__ == "__main__":
    print("This module is not for direct call!")
