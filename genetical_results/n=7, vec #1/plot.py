#%matplotlib inline

import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')  # Красивые графики
plt.rcParams['figure.figsize'] = (15, 5)  # Размер картинок

file = open("population.txt",'r')
lines = file.readlines()
file.close()

final = [int(x) for x in lines[1::2]]


#fixed_df = pd.read_csv('results_n4_step1.csv',  # Это то, куда вы скачали файл
#                       sep=',', encoding='Windows-1251')


plt.xlabel('Номер итерации алгоритма')
plt.ylabel('Число особей в популяции')
#plt.plot(fixed_df[' Длина минимального полинома'])
plt.plot(final)
plt.show()