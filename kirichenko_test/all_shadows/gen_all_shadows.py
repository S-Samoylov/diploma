import kir_one_shadow
import time
import math

def NextSet(a, N, m): #a - list of ints
    k = m
    for i in range(k-1, -1,-1):
        if (a[i] < N - k + i + 1):
            a[i] += 1
            for j in range(i+1, k):
                a[j] = a[j-1] + 1
            return True
    return False

def c(vect, N, m): #list vect n, m
    #l = []
    num = 0
    a = [0]*N
    for i in range(0, N):
        a[i] = i + 1
    s = []
    for i in a[:m]:
        s.append(vect[i-1])     
        if (kir_one_shadow.check_shadow_full(s)):
            print(s)
            num += 1
    #l.append(s)
    if (N >= m):
        while (NextSet(a, N, m)):
            #print(a[:m], a, N, m)
            if (a[1] >= math.comb(int(n),1)+1): break
            s = []
            for i in a[:m]:
                s.append(vect[i-1])
            
            if (kir_one_shadow.check_shadow_full(s)):
                print(s)
                num += 1
                #l.append(s)
            #if (len(l) == 2): break
    return num
    
def gen_all_shadows(n):
    vs = kir_one_shadow.gen_min_shadow(n)
    print(vs)
    min_len = len(vs)
    allvec = []
    for i in range(2**n - 1, -1, -1):
            allvec.append(kir_one_shadow.decToBin(i, n))
    vec = sorted(allvec, key = kir_one_shadow.con_rank, reverse = True)
    res = c(vec, len(allvec), min_len)
    #print(len(res), len(res[0]), len(res[1]))
    #print(res[0])
    return res

n = input()
start = time.time()
result = gen_all_shadows(int(n))
end = time.time()
#f = open(f'n_{n}_all_shadows_time.txt', 'w')
#f.writelines(str(result) + '\n')
#f.writelines(str(end-start) + '\n')
#f.close()