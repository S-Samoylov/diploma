# -*- coding: utf-8 -*-

import collections as col
import pandas as pd

n_start = 5
n_end = 8
num = 100

def make_table(n_start, n_end, num):
    res_list = []
    k = 0
    for it in range(n_start, n_end+1):
        res_list.append([])
        file = open(f'result_performed_100_shadows_random_vecs_{it}_{num}.txt', 'r')

        lines = file.readlines()
        file.close()
        d = col.defaultdict(list) # num : [len1, len2]
        min_after = 10000000
        min_after_performed = 10000000
        max_delta = 0
        num_zero_after = 0
        num_zero_performed = 0

        in_vec = False
        j = 0

        for i in range(0,len(lines),12):
            j += 1
            d[j].append(int(lines[i+4]))
            d[j].append(int(lines[i+7]))
            d[j].append(int(lines[i+10]))
            #d[j].append(int(lines[i+13]))
            delta = d[j][0] - d[j][2]
            if (delta > max_delta): max_delta = delta
            if (d[j][0] == d[j][2]): num_zero_after += 1
            if (d[j][2] < min_after): min_after = d[j][2]
            #if (d[j][2] == d[j][3]): num_zero_performed += 1
            #if (d[j][3] < min_after_performed): min_after_performed = d[j][3]
        res_list[k].append(j)
        #print('last_len = ', d[j][1])
        avg_len = sum([d[x][1] for x in range(1, j+1)])/j
        avg_len_before = sum([d[x][0] for x in range(1, j+1)])/j
        avg_len_performed = sum([d[x][2] for x in range(1, j+1)])/j
        #avg_len_zhig = sum([d[x][0] for x in range(1, j+1)])/j
        #res_list[k].append(avg_len_zhig)
        res_list[k].append(avg_len_before)
        #res_list[k].append(avg_len)
        #res_list[k].append(num_zero_after)
        #res_list[k].append(min_after)
        res_list[k].append(avg_len_performed)
        res_list[k].append(num_zero_after)
        #res_list[k].append(num_zero_performed)
        #res_list[k].append(min_after_performed)
        res_list[k].append(max_delta)
        k += 1
    return (res_list)

df = pd.DataFrame(make_table(n_start, n_end, num), columns = ['Количество протестированных функций', 'Средняя длина полинома без минимизации', 'Средняя длина полинома после минимизации', 'Количество функций для которых минимизация не привела к улучшению', 'Наибольшая разница длин полиномов до и после минимизации'], index = [x for x in range(n_start, n_end+1)])
df.to_html('table2_final.html')
subprocess.call('wkhtmltoimage -f png --width 0 table.html table.png', shell=True)

