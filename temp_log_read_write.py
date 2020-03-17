import pandas as pd
import datetime 
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

now = datetime.datetime.now()
headers = ['Date', 'Time', 'Temperature', 'Humidity']
df = pd.read_csv('/home/pi/Desktop/python_scripts/Watch/temp_logbook.csv', names=headers,skiprows=[0], index_col=0)
plot = df.plot(title='Temp & Humidity Change', lw=1, marker='.')


x = df['Time']
y= df['Temperature']

plt.show()