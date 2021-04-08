import math
import collections as col
import copy
import numpy as np

def findZhegalkin(inputVec):
    n = int(math.log2(len(inputVec)))
    zhigalkin = inputVec.copy()
    # calculate zhigalkin
    for i in range(n):
        gap = 2 ** i
        j = gap
        while j < len(zhigalkin):
            for l in range(gap):
                zhigalkin[j] = (zhigalkin[j] + zhigalkin[j - gap]) % 2
                j += 1
            j += gap
    return zhigalkin

def decToBin(dec, n):
    res_num = []

    while True:
        res_num += [dec % 2]
        dec //= 2

        if dec == 0:
            break

    if len(res_num) != n:
        for i in range(n - len(res_num)):
            res_num += [0]

    return res_num[::-1]
    

def v(con, arg):
        v = 1
        check = 0

        for i in range(len(con)):
            check += con[i]
            if con[i] == 0:
                continue
            if con[i] == 1:
                v *= arg[i]
                continue
            v *= (arg[i] + 1) % 2
        if check == 0:
            return 0
        return v
        
def truthVector(con):
        n = len(con)
        vector = []

        for i in range(2 ** n):
            vector += [v(con, decToBin(i, n))]

        return vector
    
def parseZhigalkin(zhigalkin):
    pol = []
    n = int(math.log2(len(zhigalkin)))
    for i in range(len(zhigalkin)):
        if zhigalkin[i] == 1:
            binary = decToBin(i, n)
            if sum(binary) == 0:
                pol += [1]
            else:
                pol += [binary]
    return pol
    
def con_rank(con): #con - conjunction: [1, 0, 2, 1, 0, 1] = x1*~x3*x4*x6 - rank = 4 (num of variables)
    rank = 0
    if (con == 1): return 0 
    for x in con:
        if (x != 0): rank += 1
    return rank
    
def find_not_zero_index(con):
    for i in range(len(con)):
        if (con[i] != 0): return i

def check_shadow_full(shadow):
    n = len(shadow[0])
    targ = 2**n - 1
    s = set()
    for x in shadow:
        for i in range(len(x)):
            if (x[i] == 0): continue
            else:
                x[i] = 0
                s.add(tuple(x))
                x[i] = 1
    #return len(s)
    if (len(s) == targ): return True
    else: return False
    
def vec_shadow(vector):
    result_poly = set()
    for i in range(len(vector)):
        if (vector[i] == 1):
            result_poly.add(tuple(vector[:i] + [0] + vector[i+1:]))
    return result_poly

def value_by_poly(poly): #list of lists/tuples
    if (1 in poly):
        poly.remove(1)
        if (len(poly) == 0): return 1
        result_poly = np.array([1]*2**len(poly[0]), dtype = int)
    else:
        result_poly = np.zeros(2**len(poly[0]), dtype = int)
    for x in poly:
        result_poly = np.array(truthVector(x)) ^ result_poly
    return result_poly.tolist()  

def gen_min_shadow(n):
    shadow = []
    rank = n
    s = set() 
    allvec = []
   
   #generate all rank collections
   
    for i in range(2**n - 1, -1, -1):
        allvec.append(decToBin(i, n))
    #sort by rank
    all_sorted = sorted(allvec, key = con_rank, reverse = True)
    #cycle
    sum = 0
    for k in range(n):
        one_rank_vec = all_sorted[sum:sum+math.comb(n,k)]
        for its in range(len(one_rank_vec)):
            #now check whole set and create dict {len(locla_s):{shadow_vec}}
            d_vec = col.defaultdict(list)
            for vec in one_rank_vec:
                sh = vec_shadow(vec)
                len_delta = len(s | sh) - len(s)
                d_vec[len_delta].append(vec)
            #find the best
            max_key = max(d_vec.keys())
            if (max_key == 0): break
            shadow.append(d_vec[max_key][0])
            for x in vec_shadow(d_vec[max_key][0]):
                s.add(tuple(x))
        sum += math.comb(n,k)
        if (check_shadow_full(shadow)): break
    #print(shadow)
    #print(s)
    #print(check_shadow_full(shadow))
    return shadow 

def logic_minimize(s):
    poli = copy.deepcopy(s)
    d = col.defaultdict(list)
    #generate dict {rank:list_of_cons}, f.e. {0: [1], 1: [[0, 0, 1, 0]], 2: [[1, 1, 0, 0]], 3: [[1, 1, 0, 1]], 4: [[1, 1, 1, 1]]}
    for ik in range(len(poli)):
        poli[ik] = list(poli[ik])
    for x in poli:
        if (x == 1): d[con_rank(x)].append(x)
        else: d[con_rank(x)].append(x)
    z = 0
    while (z != len(poli)):
        #print('start', z, poli)
        x = poli[z]
    #for x in poli:
        if (x == 1):
            if (1 in d.keys()):
                #print(True) 
                #optimization has found 
                #1. change dict, delete 0-key
                del d[0]
                #2. delete con from poli
                poli.remove(x)
                #3. change poli
                ind = poli.index(d[1][0])
                not_zero_ind = find_not_zero_index(d[1][0])
                if (poli[ind][not_zero_ind] == 1): poli[ind][not_zero_ind] = 2
                elif (poli[ind][not_zero_ind] == 2): poli[ind][not_zero_ind] = 1
                else: print('error1')
                #4. delete replications
                if (poli.count(poli[ind]) > 1): poli.remove(poli[ind])
                #here is needed to restart cycle with updated x
                z -= 1
        else:
            for i in range(len(x)):
                if (x[i] == 0): continue
                new = x[:i] + [0] + x[i+1:]
                if (new in d[con_rank(x) - 1]):
                    #print(True)
                    #optimization has found
                    #1. change poli
                    ind = poli.index(x)
                    if (poli[ind][i] == 1): poli[ind][i] = 2
                    elif (poli[ind][i] == 2): poli[ind][i] = 1
                    else: print('error1')
                    #2. change dict
                    d[con_rank(x) - 1].remove(new) #delete subcon
                    d[con_rank(x)][d[con_rank(x)].index(x)] = poli[ind]
                    #3. delete con from poli
                    poli.remove(new)
                    #4. delete replications
                    if (poli.count(poli[ind]) > 1):
                        poli.remove(poli[ind])
                        d[con_rank(x)].remove(poli[ind])
                    #here is needed to restart cycle with updated x
                    z -= 1
                    break
        #print('end', z, poli)
        z += 1
    for ik in range(len(poli)):
        poli[ik] = tuple(poli[ik])
    return poli
    
def poli_output(poli):
    s = []
    for con in poli:
        if (con == 1): s.append('1')
        else:
            sub_s = []
            for i in range(len(con)):
                if (con[i] == 1): sub_s.append(f'x{i+1}')
                elif (con[i] == 2): sub_s.append(f'~x{i+1}')
            s.append('*'.join(sub_s))
    return('+'.join(s))

def kir_with_min(vector, param = 1): #param = 0 - without minimize input_vec - string
    vec = copy.deepcopy(vector)
    #StartKir
    n = int(math.log(len(vec), 2))
    T_min_set = gen_min_shadow(n)
    input_vec = [int(x) for x in vec]
    zheg_input_vec = parseZhigalkin(findZhegalkin(input_vec))
    F_Tshadow_poli = T_min_set #format: x1*x2*x3 + x1*x2 + x1*x4 + x2 #Phi
    #step 3
    #Psi
    control_set = set([tuple(x) for x in F_Tshadow_poli if x != 1]) ^ set([tuple(x) for x in zheg_input_vec if x != 1])
    if ((1 in F_Tshadow_poli) ^ (1 in zheg_input_vec)): control_set.add(1)
    control_set = list(control_set)
    #step 4-5
    result_poly = [] #delta
    if (tuple([1]*n) in control_set):
        result_poly.append(tuple([1]*n))
        control_set.remove(tuple([1]*n))
    #step 6 always done
    #step 7-8
    for shadow in T_min_set:
        K = copy.deepcopy(shadow)
        K1 = copy.deepcopy(shadow)
        low_rank_list = [x for x in control_set if (con_rank(x) == con_rank(shadow)-1)]
        if (low_rank_list == [1]):
            K1[shadow.index(1)] = 2
        else:
            for x in low_rank_list:
                sub = (np.array(shadow) - np.array(x)).tolist()
                if (con_rank(sub) == 1 and 1 in sub):
                    K1[sub.index(1)] = 2
        #step 8
        result_poly.append(tuple(K1))
        control_set.append(tuple(K))
        control_set.append(tuple(K1))
        control_set = parseZhigalkin(findZhegalkin(value_by_poly(control_set)))
    if (param):
        return logic_minimize(result_poly)
    else:
        return result_poly

if (__name__ == "__main__"):
    f = '1001000010110001101000010101101010000001010111011010110001100011010110011000101010000110001100111010111010101100011000011011000110000011101111001100010100010001000110010011111101101010011111111100100101111101110100100101100010100011101110010010101001100001'
    #f = input()
    print('Input vector')
    print(f)
    res = kir_with_min(f, 1)
    print('Kirichenko')
    print(len(res))
    print(poli_output(res))

    after_min = logic_minimize(res)
    print('Min_Kirichenko')
    print(len(after_min))
    print(poli_output(after_min))
