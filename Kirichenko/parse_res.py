import collections as col
import pandas as pd

n_start = 3
n_end = 9
num = 100

def make_table(n_start, n_end, num):
    res_list = []
    k = 0
    for it in range(n_start, n_end+1):
        res_list.append([])
        file = open(f'result_random_vecs_{it}_{num}.txt', 'r')

        lines = file.readlines()
        file.close()
        d = col.defaultdict(list) # num : [len1, len2]
        min = 10000000
        max_delta = 0
        num_zero = 0

        in_vec = False
        j = 0

        for i in range(0,len(lines),9):
            j += 1
            d[j].append(int(lines[i+4]))
            d[j].append(int(lines[i+7]))
            delta = d[j][0] - d[j][1]
            if (delta > max_delta): max_delta = delta
            if (d[j][0] == d[j][1]): num_zero += 1
            if (d[j][1] < min): min = d[j][1]
        res_list[k].append(j)
        #print('last_len = ', d[j][1])
        avg_len = sum([d[x][1] for x in range(1, j+1)])/j
        avg_len_before = sum([d[x][0] for x in range(1, j+1)])/j
        res_list[k].append(avg_len_before)
        res_list[k].append(avg_len)
        res_list[k].append(num_zero)
        res_list[k].append(min)
        res_list[k].append(max_delta)
        k += 1
    return (res_list)

df = pd.DataFrame(make_table(n_start, n_end, num), columns = ['vecs num', 'Avg poli len Kir', 'Avg poli len after', 'Identical lens', 'Min len', 'Max delta lens'], index = [x for x in range(n_start, n_end+1)])
df.to_html('table.html')
subprocess.call(
    'wkhtmltoimage -f png --width 0 table.html table.png', shell=True)

