import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

with open('wyniki.csv', newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    data = list(datareader)

df = pd.DataFrame(data, columns=['x', 'y1', 'y2', 'y3', 'y4', 'y5'])
df = df.apply(pd.to_numeric)

with open('historia_eventow.csv', newline='') as csvfile:
    datareader_event = csv.reader(csvfile, delimiter=',')
    data_event = list(datareader_event)

x_event = np.array([float(row[0]) for row in data_event])  # Convert x_event to float
y_event = np.array([list(row[1:2]) for row in data_event])  # Convert y_event to float

x = df['x'][1:]
y1 = df['y1'][1:]
y2 = df['y2'][1:]
y3 = df['y3'][1:]
y4 = df['y4'][1:]
y5 = df['y5'][1:]

fig2,ax2 = plt.subplots()
fig1,ax1 = plt.subplots()
# Plotting the main graph
line1, = ax1.plot(x, y1, color='r', label='y1')
line2, = ax1.plot(x, y2, color='b', label='y2')
line3, = ax1.plot(x, y3, color='y', label='y3')
line4, = ax1.plot(x, y4, color='c', label='y4')
line5, = ax1.plot(x, y5, color='k', label='y5')

text1 = ax1.text(1, 1, 'Prawica', color='r')
text2 = ax1.text(1, 1, 'Studencka Partia Przyjaciół Piwa', color='b')
text3 = ax1.text(1, 1, 'Obóz Liberalny', color='y')
text4 = ax1.text(1, 1, 'Przyszłość dla Wszystkich', color='c')
text5 = ax1.text(1, 1, 'Harmonia Społeczna', color='k')

ax1.set_xlabel('Tury')
ax1.set_ylabel('Poparcie partii wśród społeczeństwa [%]')
ax1.set_title('Wyniki wyborów w czasie')

ax2.set_axis_off()  
event_descriptions = []

def myupdating(i):
    global b
    line1.set_data(x[:i], y1[:i])
    line2.set_data(x[:i], y2[:i])
    line3.set_data(x[:i], y3[:i])
    line4.set_data(x[:i], y4[:i])
    line5.set_data(x[:i], y5[:i])

    if i > 0 and i < 402:  # Żeby nie wyleciało poza zakres
        text1.set_position((x[i], y1[i]))
        text2.set_position((x[i], y2[i]))
        text3.set_position((x[i], y3[i]))
        text4.set_position((x[i], y4[i]))
        text5.set_position((x[i], y5[i]))

        if b < len(x_event):
            if x_event[b] == i:
                ax1.axvline(x=x_event[e], color='black', linestyle='--')  # Czarna linia w miejscu eventu
                 # Dodawanie numeru eventu na szczycie linii
                ax1.text(x_event[e], 1, f"{e + 1}.", color='red', ha='center', va='top')
                b += 1
b = 0

def myupdating_event(i):
        global e

        # if e == len(x_event):
        #     print("0")
        # elif x_event[e] == i:
        #     ax2.text(0, 1 - e * 0.03, f"{e + 1}. Event: {y_event[e][0]}", color='red', fontsize=7)
        #     e += 1
        if e < len(x_event):
            if x_event[e] == i:
                ax2.text(0, 1 - e * 0.03, f"{e + 1}. Event: {y_event[e][0]}", color='red', fontsize=7)
                e += 1
e = 0
i = 0
#if i == 0:
myanimation = FuncAnimation((fig1), myupdating, frames=501, interval=10)
myanimation_event = FuncAnimation((fig2), myupdating_event, frames=501, interval=20)


plt.show()
