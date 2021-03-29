from z3 import *

def decToBin(dec, n):
    result = []
    while True:
        result += [dec % 2]
        dec //= 2
        if dec == 0:
            break
    if len(result) != n:
        for i in range(n - len(result)):
            result += [0]
    return result[::-1]

func = '1011'
n = 2
k = 2

# Z_ij, where i - ind of assignment (0 .. 2**n-1), j - ind of conjuction (1 .. k)
Z = [[Bool('Z_%d%d' %(i, j)) for j in range(1, k+1)] for i in range(2**n)]
# Ans_ij, where i - ind of conjuction (1 .. k+1), j - ind of x
Ans = [[Int('Ans_%d%d' %(i, j)) for j in range(1, n+1)] for i in range(1, k+1)]
# Sigm[i][j], where i - ind of assignment (0 .. 2**n-1), j - ind of x
Sigm = [decToBin(x, n) for x in range(2**n)]
# [1, 0, 1, 1] len - 2**n
inp_vec = [int(x) for x in func]

print(Z)
print(Ans)
print(Sigm)

s = Solver()
for i in range(k):
    for j in range(n):
        s.add(Ans[i][j] <= 2)
        s.add(Ans[i][j] >= 0) 
for b in inp_vec:
    #Go throw all meanings
    #zk1+zkn == b
	#