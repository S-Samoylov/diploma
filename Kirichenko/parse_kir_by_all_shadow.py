import collections as col
import pandas as pd
import matplotlib.pyplot as plt

file = open('result_vec_1_n_5_all_shadows.txt', 'r')
lines = file.read().split('\n')
file.close()

df = pd.DataFrame(lines[8::10])
df.astype(int)
plt.style.use('ggplot')  #Красивые графики
plt.rcParams['figure.figsize'] = (15, 5)  #Размер картинок
plt.plot(df[0])
plt.show()