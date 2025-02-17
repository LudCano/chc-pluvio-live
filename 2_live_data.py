import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

df = pd.read_csv('data_hr.dat', skiprows = [0,2,3,36972], parse_dates = ['TIMESTAMP'])

df = df[['TIMESTAMP','Precip_Tot']]
df = df[df.TIMESTAMP >= dt.datetime(2024,9,1)]
df.columns = ['datetime','rain']



# dia en que el pluviometro fue destapado
lst_dat = df.datetime.to_list()[-1]
lim = lst_dat + dt.timedelta(days = -1)
lim = lim.replace(hour = 0, minute= 0, second=0)
#########################################
##### figura
#########################################
fig, axs = plt.subplots(3,1,figsize = (8,12))
fig.subplots_adjust(hspace = 0.2, top = 0.98, bottom = 0.05)

#########################################
##### horario
#########################################
df_ = df[df.datetime >= lim]
ax1 = axs[0]
ax1.bar(df_.datetime, df_.rain, width=pd.Timedelta(hours=1), align='edge', edgecolor = 'black')
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%d%b'))
ax1.xaxis.set_major_locator(mdates.HourLocator(np.arange(2,24,2)))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
ax1.tick_params(axis='x', which='minor', pad=18)
ax1.set_xlim(lim + dt.timedelta(hours=-1), lim+dt.timedelta(hours = 47, minutes = 30))
ax1.grid(which='both', lw = 0.2, alpha = .5)
#ax1.set_title('Precipitación últimos dos días Cota Cota', fontsize = 18)
#ax1.set_xlabel('Hora Local', fontsize = 10)
ax1.set_ylabel('Precipitación [mm/hora]', fontsize = 10)



#########################################
##### 10 dias
#########################################
df_ = df[df.datetime > (dt.datetime.now() + dt.timedelta(days = -9)).replace(hour = 0, minute = 0)]
df_ = df_.resample('1d', on = 'datetime').sum()
df_ = df_.reset_index()
ax2 = axs[1]
ax2.bar(df_.datetime, df_.rain, width = pd.Timedelta(days = 1), align = 'edge', edgecolor = 'black')
ax2.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%b'))
ax2.grid(which='both', lw = 0.2, alpha = .7)
#ax2.set_title('Precipitación últimos 10 días Cota Cota', fontsize = 18)
#ax2.set_xlabel('Fecha', fontsize = 10)
ax2.set_ylabel('Precipitación acumulada diaria [mm]', fontsize = 10)


#########################################
##### acumulado
#########################################
hist = pd.read_csv('chacaltaya_historial.csv', parse_dates = ['dtt'])


anhos = hist.hidroyear.unique()
dfss = []


ax3 = axs[2]

for year in anhos:
    df_ = hist[hist.hidroyear == year]
    lin, = ax3.plot(df_.dtt, df_.rainsum, label = f'{min(anhos)}-2023', c = 'k', alpha = .3, lw = .7)
    dfss.append(df_.rainsum.to_list()[:73])
    
rains = np.array(dfss)
rain_cummean = np.mean(rains, axis = 0)

df_now = [i + dt.timedelta(days = -365) for i in df.datetime.to_list()]
lin2, = ax3.plot(df_.dtt, rain_cummean, label = 'Promedio', c = 'k', lw = 1.5, ls = '--')
lin3, = ax3.plot(df_now, df.rain.cumsum(), label = '2024', c = 'r', lw = 1.5)
ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax3.set_xlabel('Año Hidrológico', fontsize = 10)
ax3.set_ylabel('Precipitación acumulada [mm]', fontsize = 10)
#ax3.set_title('Precipitación acumulada Cota Cota', fontsize = 15)
ax3.legend(handles = [lin, lin2, lin3])

nownow = (dt.datetime.now() + dt.timedelta(hours = -4)).strftime('%d%b %H:%M')
nowtxt = 'Última ejecución ' + nownow
last_date = df.datetime.to_list()[-1]
last_date = 'Último dato ' + dt.datetime.strftime(last_date, '%d%b %H:%M')
last_rain = df.rain.cumsum().to_list()[-1]
txt = f'Precipitación acumulada\n {round(last_rain,1)}mm'
ax3.annotate(txt, (0.96,0.01), xycoords='axes fraction', ha = 'right', fontsize = 12)
ax3.annotate(last_date, (0.96,0.01), xycoords='figure fraction', ha = 'right', fontsize = 6)
ax3.annotate(nowtxt, (0.96,0.002), xycoords='figure fraction', ha = 'right', fontsize = 6)


ax1.set_title('PRCP CHACALTAYA', fontsize = 12)
fig.savefig('plot_all_chacaltaya.png', dpi = 400)
#plt.show()
