import random
n = 3
col = 100
f = open(f'random_vecs_{n}_100.txt', 'w')
for i in range(col):
    l = []
    for x in range(2**n):
        l.append(random.randint(0,1))
    f.write("".join(str(x) for x in l) + '\n')
f.close()