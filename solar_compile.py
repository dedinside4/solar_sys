import math
import time as clock
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import root_scalar
import pandas
import warnings
gravitational_constant = 6.67408E-11
warnings.filterwarnings('ignore')
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
def move_space_objects_2(t,stars, planets,time):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    one_year=60*60*24*365
    one_month=60*60*24*30
    last_printed=0
    maxpe=0.0001
    t_min=100
    print(t)
    vs=np.array([np.array([body.Vx, body.Vy]) for body in stars])
    rs=np.array([np.array([body.x, body.y]) for body in stars])
    m=np.array([body.m for body in stars])
    if len(planets)>0:
        vp=np.array([np.array([body.Vx, body.Vy]) for body in planets])
        rp=np.array([np.array([body.x, body.y]) for body in planets])
    else:
        vp=np.array([[np.NaN,np.NaN]])
        rp=np.array([[np.NaN,np.NaN]])
    dfs=[]
    ar=np.array(np.concatenate((rs,rp,vs,vp)).flatten())
    s = pandas.Series(ar).dropna()
    s[len(s)]=0
    df = pandas.DataFrame(columns=[i for i in range(len(s))])
    df.loc[len(df.index)] = s
    last_time = clock.perf_counter()
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
                print(e)
                dt=t
        rs,vs=teylor_2(rs,vs,acs,dt)
        rp,vp=teylor_2(rp,vp,acp,dt)
        t-=dt
        time+=dt
        ar=np.array(np.concatenate((rs,rp,vs,vp)).flatten())
        s = pandas.Series(ar).dropna()
        s[len(s)]=dt
        df.loc[len(df.index)] = s
        if len(df)>10000:
            dfs.append(df)
            df = pandas.DataFrame(columns=[i for i in range(len(s))])
        if time//one_month>last_printed:
            last_printed+=1
            print(time//one_month, ' месяцев замоделено за ',clock.perf_counter()-last_time)
            last_time = clock.perf_counter()
    dfs.append(df)
    return dfs
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
def calculate_space_objects(space_objects, t,time):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
##    if len(space_objects)>0:
##        move_space_objects(t, space_objects)
    stars=[]
    planets=[]
    m=[]
    for obj in space_objects:
        if obj.type=='star':
            stars.append(obj)
            m.append(obj.m)
        elif obj.type=='planet':
            planets.append(obj)
    dfs=move_space_objects_2(t, stars, planets,time)
    df=pandas.concat((dfs),ignore_index=True)
    return df
