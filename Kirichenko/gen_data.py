import random
n = 9
col = 100
f = open('random_vecs_9_100.txt', 'w')
for i in range(col):
    l = []
    for x in range(2**n):
        l.append(random.randint(0,1))
    f.write("".join(str(x) for x in l) + '\n')
f.close()