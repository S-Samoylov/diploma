import math
import collections as col
import copy
import numpy as np
import random

NUMBER_OF_SHADOW_COVERAGES = 100

ONE = 0
TWO = 0
THREE = 0
FOUR = 0
DEL_DUPL = 0

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
    cop = copy.deepcopy(poly)
    if (1 in cop):
        cop.remove(1)
        if (len(cop) == 0): return 1
        result_poly = np.array([1]*2**len(cop[0]), dtype = int)
    else:
        result_poly = np.zeros(2**len(cop[0]), dtype = int)
    for x in cop:
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
    
def logic_minimize(s): #accept only list with tuples, returns same
    global ONE
    global TWO
    global THREE
    global FOUR
    global DEL_DUPL
    poli = copy.deepcopy(s)
    d = col.defaultdict(list)
    #generate dict {rank:list_of_cons}, f.e. {0: [1], 1: [[0, 0, 1, 0]], 2: [[1, 1, 0, 0]], 3: [[1, 1, 0, 1]], 4: [[1, 1, 1, 1]]}
    for ik in range(len(poli)):
        if (poli[ik] != 1): poli[ik] = list(poli[ik])
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
                #4. delete if replications
                deleted_before = 0
                repl_count = poli.count(poli[ind])
                if (repl_count > 1):
                    DEL_DUPL += 1
                    while(repl_count > 1):
                        if (poli.index(poli[ind]) <= z): deleted_before += 1
                        poli.remove(poli[ind])
                        if (poli.index(poli[ind]) <= z): deleted_before += 1
                        poli.remove(poli[ind])
                        repl_count-=2
                #here is needed to restart cycle with updated x
                ONE += 1
                z = z - 1 - deleted_before
        else:
            for i in range(len(x)):
                if (x[i] == 0): continue
                new = x[:i] + [0] + x[i+1:]
                if (new in d[con_rank(x) - 1]):
                    #optimization has found
                    #1. change poli
                    ind = poli.index(x)
                    if (poli[ind][i] == 1): poli[ind][i] = 2
                    elif (poli[ind][i] == 2): poli[ind][i] = 1
                    else: print('error1')
                    #2. change dict
                    d[con_rank(new)].remove(new) #delete subcon
                    #d[con_rank(x)][d[con_rank(x)].index(x)] = poli[ind]
                    #3. delete con from poli
                    poli.remove(new)
                    x = copy.deepcopy(poli[ind])
                    #4. delete if replications
                    deleted_before = 0
                    repl_count = poli.count(x)
                    ONE += 1
                    if (repl_count > 1):
                        DEL_DUPL += 1
                        while(repl_count > 1):
                            if (poli.index(x) <= z): deleted_before += 1
                            poli.remove(x)
                            if (poli.index(x) <= z): deleted_before += 1
                            poli.remove(x)
                            d[con_rank(x)].remove(x)
                            d[con_rank(x)].remove(x)
                            repl_count-=2
                    #here is needed to restart cycle with updated x
                    z = z - 1 - deleted_before
                    break
        #print('end', z, poli)
        z += 1
        if (z < 0 ): z = 0
        if (len(poli) == 0): break
    for ik in range(len(poli)):
        if (poli[ik] != 1): poli[ik] = tuple(poli[ik])
    #delete duplicates
    s = set()
    if (len(set(poli)) != len(poli)):
        DEL_DUPL += 0
        for x in set(poli):
            l = poli.count(x)
            if (l == 1 or (l > 1 and l % 2 == 1)): s.add(x)
        poli = list(s)
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

def kir_with_min(vector, cover = 0, param = 1): #param = 0 - without minimize input_vec - string
    vec = copy.deepcopy(vector)
    #StartKir
    n = int(math.log(len(vec), 2))
    if (cover == 0):
        T_min_set = gen_min_shadow(n)
    else:
        T_min_set = []
        for vect in cover:
            T_min_set.append(list(vect))
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
    control_set = set(control_set)
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
        #newcode
        dop_l = []
        dop_l.append(tuple(K))
        dop_l.append(tuple(K1))
        dop_l = parseZhigalkin(findZhegalkin(value_by_poly(dop_l)))
        dop_ll = [tuple(x) for x in dop_l if x != 1]
        if (1 in dop_l):
            dop_ll.append(1)
        dop_ll = set(dop_ll)
        control_set = control_set ^ dop_ll
        #control_set.append(tuple(K))
        #control_set.append(tuple(K1))
        #control_set = parseZhigalkin(findZhegalkin(value_by_poly(control_set)))
    if (param == 1):
        return logic_minimize(result_poly)
    elif (param == 2):
        polo = logic_minimize(result_poly)
        while (True):
            s = dop_formuls(polo)
            if (s == polo):
                break
            else:
                polo = s
        return logic_minimize(polo)
    else: return result_poly

def checktype(v1, v2):
    s = tuple(np.array(v1) - np.array(v2))
    r = con_rank(s)
    if (r == 2):
        first = 0
        for i in range(len(s)):
            if (s[i] != 0):                
                if (v1[i] == 0 or v2[i] == 0):
                    return 0
                if (first != 0):
                    if (s[i] == first):
                        return 1
                    else:
                        return 2
                first = s[i]
    return 0

def dop_formuls(pol):# type1 : 1 + x1x2+~x1~x2 = ~x1x2+x1~x2 & type2 :  1+~x1x2+x1~x2 = x1x2+~x1~x2
    global ONE
    global TWO
    global THREE
    global FOUR
    global DEL_DUPL
    s = copy.deepcopy(pol)
    one = False
    if (1 in s):
        one = True
        s.remove(1)
    if (s == []): return [1]
    n = len(s[0])
    pairs = []#[[type,(vec),(vec), ind1_pol, ind2_pol],...] 
    for i in range(len(s)-1):
        for j in range(i+1,len(s)):
            typ = checktype(s[i],s[j])
            if (typ != 0):
                pairs.append([typ,s[i],s[j],i,j])
    used_ind = set()
    for_del = set()
    for l in pairs:
        if (l[3] in used_ind or l[4] in used_ind):
            continue
        v1 = l[1]
        v2 = l[2]
        new_con = []
        for i in range(len(v1)):
            if (v1[i] == v2[i]):
                new_con.append(v1[i])
            else:
                new_con.append(0)
        if (tuple(new_con) in s or new_con == [0]*n and one):
            if (new_con == [0]*n and one):
                one = False
            #third condition true
            if (l[0] == 1): #type = 1
                if (new_con != [0]*n):
                    if (s.index(tuple(new_con)) in used_ind):
                        continue
                    used_ind.add(s.index(tuple(new_con)))
                    for_del.add(s.index(tuple(new_con)))
                used_ind.add(l[4])
                used_ind.add(l[3])
                FOUR += 1
                med = tuple(np.array(s[l[3]]) - np.array(s[l[4]]))
                for i in range(len(med)):
                    if (med[i] != 0):
                        pr = list(s[l[3]])
                        if (pr[i] == 1):
                            pr[i] = 2
                        elif (pr[i] == 2):
                            pr[i] = 1
                        s[l[3]] = tuple(pr)
                        pr = list(s[l[4]])
                        if (pr[i] == 1):
                            pr[i] = 2
                        elif (pr[i] == 2):
                            pr[i] = 1
                        s[l[4]] = tuple(pr)
                        break
            elif(l[0] == 2): #type = 2
                if (new_con != [0]*n):
                    if (s.index(tuple(new_con)) in used_ind):
                        continue
                    used_ind.add(s.index(tuple(new_con)))
                    for_del.add(s.index(tuple(new_con)))
                used_ind.add(l[4])
                used_ind.add(l[3])
                THREE += 1
                med = tuple(np.array(s[l[3]]) - np.array(s[l[4]]))
                for i in range(len(med)):
                    if (med[i] != 0):
                        pr = list(s[l[3]])
                        if (pr[i] == 1):
                            pr[i] = 2
                        elif (pr[i] == 2):
                            pr[i] = 1
                        s[l[3]] = tuple(pr)
                        pr = list(s[l[4]])
                        if (pr[i] == 1):
                            pr[i] = 2
                        elif (pr[i] == 2):
                            pr[i] = 1
                        s[l[4]] = tuple(pr)
                        break
    new_s = []
    for i in range(len(s)):
        if (i not in for_del):
            new_s.append(s[i])
    if (one): new_s.append(1)
    return new_s        

def gen_some_shadows(n, colect): #returns list of sets with colect number of shadow coverages
    rank = n
    allvec = []
   
   #generate all rank collections
    shadow_coverages = []
    col_coverages = 0
    
    for i in range(2**n - 1, -1, -1):
        allvec.append(decToBin(i, n))
    #sort by rank
    all_sorted = sorted(allvec, key = con_rank, reverse = True)
    
    while (col_coverages < colect):
        #start cycle
        sum = 0
        shadow = []
        s = set() 
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
                num = random.randint(0,len(d_vec[max_key])-1)
                shadow.append(d_vec[max_key][num])
                for x in vec_shadow(d_vec[max_key][num]):
                    s.add(tuple(x))
            sum += math.comb(n,k)
            if (check_shadow_full(shadow)):
                break
        set_s = set()
        for vec in shadow:
            set_s.add(tuple(vec))
            
        if (set_s not in shadow_coverages):
            shadow_coverages.append(set_s)
            col_coverages += 1
            
    return shadow_coverages

def get_shadow(inp):
    inp = [int(x) for x in input().replace('[','').replace(']','').split(',')]
    shadow = []
    for i in range(n,len(inp)+1,n):
        shadow.append(inp[i-n:i])
    print(shadow)
    return shadow 
    
ALL_SHADOWS = [[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 1]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 0]],\
[[1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 0, 1]]]
    
if (__name__ == "__main__"):
    f = input()
    print('Input vector')
    print(f)
    #coverages = gen_some_shadows(int(math.log(len(f), 2)), NUMBER_OF_SHADOW_COVERAGES)
    coverages = ALL_SHADOWS
    min_pol = [] # 0 - len_kir, 1 - poli_len, 2 - min_len, 3 - poli_len, 4 - len_perf, 5 - poli_perf
    min_len = 1000000000
    new = []
    for coverage in coverages:
            pol = []
            new.append(sorted([list(x) for x in coverage], key = con_rank, reverse = True))
    coverages = new
    for coverage in coverages:
        pol = []
        res = kir_with_min(f, cover = coverage, param = 2)
        if (value_by_poly(res) != [int(x) for x in f]):
            df = open("log.txt","a")
            df.writelines(f)
            df.writelines(str(coverage))
            df.writelines(str(poli_output(res)))
            df.close()
        
        if (ONE > 0 or THREE > 0 or FOUR > 0):
            print('Coverage')
            print(str(coverage))
            print('Kirichenko')
            print(poli_output(kir_with_min(f, cover = coverage, param = 0)))
            print('Performed')
            print(poli_output(res))
            print(str(ONE))
            print(str(THREE))
            print(str(FOUR))
            if (ONE > 0 and (THREE > 0 or FOUR > 0)):
                df = open("best.txt","a")
                df.writelines('Input vector')
                df.writelines('\n')
                df.writelines(f)
                df.writelines('\n')
                df.writelines('Coverage')
                df.writelines('\n')
                df.writelines(str(coverage))
                df.writelines('\n')
                df.writelines('Kirichenko')
                df.writelines('\n')
                df.writelines(poli_output(kir_with_min(f, cover = coverage, param = 0)))
                df.writelines('\n')
                df.writelines('Performed')
                df.writelines('\n')
                df.writelines(poli_output(res))
                df.writelines('\n')
                df.writelines(str(ONE))
                df.writelines('\n')
                df.writelines(str(THREE))
                df.writelines('\n')
                df.writelines(str(FOUR))
                df.writelines('\n')
                df.close()
        ONE = 0
        TWO = 0
        THREE = 0
        FOUR = 0
        DEL_DUPL = 0