from tkinter import filedialog
import pandas
import os
from solar_input import *
from solar_compile import *
inf=filedialog.askopenfilename().split('/')[-1]
computings=filedialog.askopenfilename().split('/')[-1]
space = read_space_objects_data_from_file(inf)
space_objects=[]
for obj in space:
    space_objects.append(obj.obj)   
db=open(computings,'r')
df=pandas.read_csv(db)
db.close()
#print(df)
info=df.loc[len(df)-1]
#print(info)
for i in range(len(space_objects)):
    space_objects[i].x=info.iloc[i*2]
    space_objects[i].y=info.iloc[i*2+1]
    space_objects[i].Vx=info.iloc[2*len(space_objects)+i*2]
    space_objects[i].Vy=info.iloc[2*len(space_objects)+i*2+1]
time=0
y=int(input('лет'))
d=int(input('дней'))
h=int(input('часов'))
m=int(input('минут'))
s=int(input('секунд'))
t=s+60*(m+60*(h+24*(d+365*y)))
df1=calculate_space_objects(space_objects, t,time)
#print(df1)
#print(type(df1.columns[0]))
#print(type(df.columns[0]))
d=dict([(i,str(i)) for i in range(len(df.columns))])
df1=df1.rename(columns=d)
df0=pandas.concat([df,df1],ignore_index=True)
#print(df0)
db=open(computings+'(1)','w')
df0.to_csv(path_or_buf=db,index=False)
db.close()
