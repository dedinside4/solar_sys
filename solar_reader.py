import pandas
import os 
dfs=[]
order=0
df=None
last_index=0
cur_time=0
real_time=0
def init(filename):
    global dfs
    global df
    global order
    db=open(filename,'r')
    df1=pandas.read_csv(db)
    num=10000
    for i in range(0,len(df1)//num+1):
        dfs.append(df1[i*num:(i+1)*num])
    df=dfs[order]
    time_column=str(len(df.columns)-1)
    print(df[time_column][last_index])
def get_objects_position(space_objects,time):
    global dfs
    global df
    global order
    global last_index
    global cur_time
    global real_time
    time_column=str(len(df.columns)-1)
    while cur_time<real_time+time:
        try:
            cur_time+=df[time_column].loc[last_index]
            last_index+=1
        except:
            order+=1
            df=dfs[order]
    real_time=real_time+time
    info=df.loc[last_index-1]
    for i in range(len(space_objects)):
        space_objects[i].x=info.iloc[i*2]
        space_objects[i].y=info.iloc[i*2+1]
        

