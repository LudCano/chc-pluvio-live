import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
df = pd.read_csv('data_hr.dat', skiprows = [0,2,3,36972], parse_dates = ['TIMESTAMP'])

df = df[['TIMESTAMP','Precip_Tot']]

df = df[df.TIMESTAMP >= dt.datetime(2016,9,1)]
df = df[df.TIMESTAMP < dt.datetime(2024,9,1)]

anhos = df.TIMESTAMP.dt.year.unique()
df.columns = ['datetime','rain']

df.sort_values('datetime', inplace=True)

df = df.resample('5d', on = 'datetime').sum()
df = df.reset_index()

anhos = list(df.datetime.dt.year.unique())


dfss = []
dfs_toexport = []
fig, ax = plt.subplots()
for i in range(len(anhos)-1):
    anho = anhos[i]
    start = dt.datetime(year=anhos[i], month=9, day = 1)
    end = dt.datetime(year = anhos[i+1], month = 9, day = 1)
    if anho == 2015:
        end = dt.datetime(year = anhos[i], month = 11, day = 5)
        
    lim = dt.datetime(year = anhos[i+1], month = 1, day = 1)
    df_aux = df[(df.datetime >= start) & (df.datetime < end)]
    d1 = df_aux[df_aux.datetime >= lim]
    d1['dtt'] = [i.replace(year = 2024) for i in d1.datetime]
    d2 = df_aux[df_aux.datetime < lim]
    d2['dtt'] = [i.replace(year = 2023) for i in d2.datetime]
    df_aux = pd.concat([d2,d1], axis = 0)
    df_aux['rainsum'] = df_aux.rain.cumsum()
    df_aux['idx'] = df_aux.reset_index().index
    #lin, = ax.plot(df_aux.dtt, df_aux.rainsum, label = f'{min(anhos)}-2023', c = 'k', alpha = .3, lw = .7)
    lin, = ax.plot(df_aux.dtt, df_aux.rainsum, label = anho)
    dfss.append(df_aux.rainsum.to_list())
    df_exp = df_aux.copy()[['dtt','rainsum']]
    df_exp['hidroyear'] = anhos[i]
    #print(df_exp)
    dfs_toexport.append(df_exp)



df_export = pd.concat(dfs_toexport, axis = 'rows')
df_export.to_csv('chacaltaya_historial.csv', index = False)