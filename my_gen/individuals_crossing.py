import collections as col
import numpy as np
import random
import sys
import time
import subprocess
sys.path.append("C:\\diploma\\Kirichenko")
from kir_one_shadow import *

def parse_sharp_out(str, n):
	#delete '\n'
	str = str[:len(str)-1]
	str = str.split(',')
	res = []
	#find 1
	if (3 in str):
		str.remove('3')
		res.append(1)
	#parse
	for con in str:
		l = [0]*n
		i = n - 1
		for x in con:
			l[i] = int(x)
			i -= 1
		res.append(tuple(l))
	return res
		

class population:
	popul_count = 0
	iter = 0
	def __init__(self, vec):
		self.individs = list() #list of individuals
		population.popul_count += 1
		self.vec = vec
	def add_individ(self, poli):
		self.individs.append(individual(poli))
	

class individual:
	individ_count = 0
	def __init__(self, poli): #poli = [(1,0,2),(1,0,1)]
		individual.individ_count += 1
		self.age = 0
		self.gens = set(poli)  #tuples inside
		self.poli = poli
		self.gen_chains_num_vecs = col.defaultdict(set) #dict: {num of gen in poli : vecs}
		self.gen_chains_vecs_num = col.defaultdict(set) #dict: {vecs: num of gen in poli}
	def add_gen_chain(self):
		col = np.random.randint(1, high = len(self.poli)) #unify discrete [low,high)
		nums = random.sample(range(0,len(self.poli)), k=col) #positions of gens 
		vec = "".join(str(x) for x in value_by_poly([self.poli[i] for i in nums]))
		for x in nums:
			self.gen_chains_num_vecs[x].add(vec)
			self.gen_chains_vecs_num[vec].add(x)
		

#def crossing(one, second, iter):

#start
vect = '1001000010110001101000010101101010000001010111011010110001100011010110011000101010000110001100111010111010101100011000011011000110000011101111001100010100010001000110010011111101101010011111111100100101111101110100100101100010100011101110010010101001100001'
N = int(math.log(len(vect), 2))
pop1 = population(vect)
pop1.add_individ(kir_with_min(vect))
print('ind_1_created')
pop1.add_individ([tuple(x) for x in parseZhigalkin(findZhegalkin([int(x) for x in vect])) if x != 1])
print('ind_2_created')
res = subprocess.check_output(['C:\\diploma\\с#\\poli\\poli\\bin\\Debug\\poli.exe', '2', vect], encoding='utf-8')
pop1.add_individ(parse_sharp_out(res,N))
print('ind_3_created')
sum = 0
for k in range(100):
	print(k)
	t = time.time()
	for i in range(100):
		pop1.individs[0].add_gen_chain()
		pop1.individs[1].add_gen_chain()
		pop1.individs[2].add_gen_chain()
	sum += time.time() - t
	s1 = pop1.individs[0].gen_chains_vecs_num.keys()
	s2 = pop1.individs[1].gen_chains_vecs_num.keys()
	s3 = pop1.individs[2].gen_chains_vecs_num.keys()
	s = s1 & s2 | s1 & s3 | s2 & s3
	print(len(s), s)
avg = sum / 100
print('time', avg)



#19.25s - один по 100
#100/100/87



