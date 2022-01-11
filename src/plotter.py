import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('data/percentages.csv')

x = np.arange(10)
y1 = df['Dowdall']
y2 = df['Formula 1']
y3 = df['Top 10']

# Grouped Bar Chart
plt.figure(1)
width = 0.3
plt.bar(x-0.3, y1, width, label = "Dowdall")
plt.bar(x, y2, width, label = "Formula 1")
plt.bar(x+0.3, y3, width, label = "Top 10")
plt.legend()

# Line Chart
plt.figure(2)
plt.plot(x, y1, label = "Dowdall")
plt.plot(x, y2, label = "Formula 1")
plt.plot(x, y3, label = "Top 10")
plt.legend()

plt.show()