import collections as col
import numpy as np
import scipy.stats as sts
import random
import sys
import time
import subprocess
sys.path.append("C:\\diploma\\Kirichenko")
from kir_one_shadow import *



MAX_INDIVID_NUM = 50
MAX_ITER_FAZE_1 = 50
RESULT_INDIVID_NUM = 5
START_NUM = 3 #minimum = 2
CROSS_ITERS_START = 100

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
	iter_global = 0
	iter_faze = 0
	faze = 0
	def __init__(self, vec):
		self.individs = list() #list of individuals
		population.popul_count += 1
		self.vec = vec
		self.crossing_iters = CROSS_ITERS_START
		
	def add_individ(self, poli, inherit_vecs = -1):
		if (inherit_vecs == -1):
			self.individs.append(individual(poli))
		else:
			self.individs.append(individual(poli, inherit_vecs))
	
	def check_faze(self):
		if (self.faze == 0 and individual.individ_count >= MAX_INDIVID_NUM):
			self.faze = 1
			self.iter_faze = 0
		if (self.faze == 1 and self.iter_faze >= MAX_ITER_FAZE_1):
			self.faze = 2
			self.iter_faze = 0
		if (self.faze == 2 and individual.individ_count <= RESULT_INDIVID_NUM):
			#stop_func
			pass
	
	def crossing_num(self): 
		#percent of population from 100 in START_NUM to 20% in MAX_INDIVID_NUM
		perc = int(80/(START_NUM - MAX_INDIVID_NUM)*individual.individ_count+100-240/(START_NUM - MAX_INDIVID_NUM))
		return int(individual.individ_count*(perc/100))-1
		
	
	def crossing_params(self): #returns probabilities of dual crossing and number of individs in tournament
		if (self.faze == 0):
			poisson_rv = sts.poisson(1, loc = 3)
			num_tourn = poisson_rv.rvs(1)[0]
			probability_dual = 1 - math.log(individual.individ_count, MAX_INDIVID_NUM)
			print("Probability of dual = ", probability_dual)
			print("Num of individs in tourn = ", num_tourn)
			return (probability_dual, num_tourn)
		elif (self.faze == 1):
			pass
		elif (self.faze == 2):
			pass
		else:
			pass
			
	def crossing_faze_0(self):
		cr_num = self.crossing_num()
		print('Number of crosses: ', cr_num)
		for i in range(cr_num):
			print("Crossing ", i)
			p_dual, num_tourn = self.crossing_params()
			bernoulli_rv = sts.bernoulli(p_dual)
			tourn_or_dual = bernoulli_rv.rvs(1)[0]
			print("Tourn or dual = ", tourn_or_dual)
			if (tourn_or_dual == 1):
				self.crossing_dual(*random.sample(self.individs, k = 2))
			else:
				if (num_tourn > individual.individ_count):
					num_tourn = individual.individ_count
				self.crossing_tourn(random.sample(self.individs, k = num_tourn))
		
		

	def crossing_dual(self, ind1, ind2):
		print("Crossing_dual_started")
		print("id1 = ", ind1.get_id(), "id2 = ", ind2.get_id())
		for k in range(self.crossing_iters):
			for i in range(100):
				ind1.add_gen_chain()
				ind2.add_gen_chain()
			s1 = ind1.gen_chains_vec_gens.keys()
			s2 = ind2.gen_chains_vec_gens.keys()
			s_before = s1 & s2
			
			s = set()
			#check for indentic pols
			for vec in s_before:
				if (ind1.gen_chains_vec_gens[vec] != ind2.gen_chains_vec_gens[vec]):
					s.add(vec)
				
				
			if (len(s) != 0):
			
				#create childs with gen_chains
				print('Crossing on iter = ', k*100)
				#choose one vec if >1 crosses
				vec = list(s)[random.randint(0, len(s)-1)]
				gens_crossed_1 = ind1.gen_chains_vec_gens[vec] #positions of changed gens in pol1
				gens_crossed_2 = ind2.gen_chains_vec_gens[vec] #positions of changed gens in pol2
				new_gens_set_1 = gens_crossed_2 #set of new gens for 1 
				new_gens_set_2 = gens_crossed_1 #set of new gens for 2
				new_pol1 = ind1.get_set_of_remaining_gens(gens_crossed_1) | new_gens_set_1
				new_pol2 = ind2.get_set_of_remaining_gens(gens_crossed_2) | new_gens_set_2
				d1 = col.defaultdict(set)#vec:gens
				d2 = col.defaultdict(set)#gen:vecs
				#полный проход по словарю в поиске цепочек с этими генfvb
				for vec, gens_set in ind1.gen_chains_vec_gens.items():
					#если гены не пересекаются с изменёнными то наследуем
					if (gens_set & gens_crossed_1 == set()):
						d1[vec] |= gens_set
						for gen in gens_set:
							d2[gen].add(vec)
				inh1 = [d1,d2]
				
				d3 = col.defaultdict(set)#vec:gens
				d4 = col.defaultdict(set)#gen:vecs
				for vec, gens_set in ind2.gen_chains_vec_gens.items():
					#если гены не пересекаются с изменёнными то наследуем
					if (gens_set & gens_crossed_2 == set()):
						d3[vec] |= gens_set
						for gen in gens_set:
							d4[gen].add(vec)
				inh2 = [d3,d4]
				
				#check
				if (''.join([str(x) for x in value_by_poly(list(new_pol1))]) != self.vec or ''.join([str(x) for x in value_by_poly(list(new_pol2))]) != self.vec):
					print('crossing_error')
					print('first')
					print(ind1.gens)
					print(gens_crossed_1)	
					print('second')
					print(ind2.gens)
					print(gens_crossed_2)	
				
				self.add_individ(new_pol1, inh1)#inharit chains
				self.add_individ(new_pol2, inh2)#inharit chains
				break
		print("Crossing_dual_ended")
		print("id1 = ", ind1.get_id(), "id2 = ", ind2.get_id())
		return 0
			
	def crossing_tourn(self, ind_list):#ind - list of individuals
		print("crossing_tourn")
		'''
		for k in range(100):
			print(k)
			for i in range(100):
				pop1.individs[0].add_gen_chain()
				pop1.individs[1].add_gen_chain()
				pop1.individs[2].add_gen_chain()
			s1 = pop1.individs[0].gen_chains_vec_gens.keys()
			s2 = pop1.individs[1].gen_chains_vec_gens.keys()
			s3 = pop1.individs[2].gen_chains_vec_gens.keys()
			s = s1 & s2 | s1 & s3 | s2 & s3
			print(len(s), s)
		'''
		
	def gen_start(self):
		print('first gen started')
		pop1.add_individ(kir_with_min(vect))
		print('ind_1_created')
		lb = parseZhigalkin(findZhegalkin([int(x) for x in vect]))
		l = [tuple(x) for x in parseZhigalkin(findZhegalkin([int(x) for x in vect])) if x != 1]
		if (1 in lb):
			l.append(1)
		pop1.add_individ(l)
		print('ind_2_created')
		res = subprocess.check_output(['C:\\diploma\\с#\\poli\\poli\\bin\\Debug\\poli.exe', '2', vect], encoding='utf-8')
		pop1.add_individ(parse_sharp_out(res,N))
		print('ind_3_created')
	
class individual:
	individ_count = 0
	unique_id = 0
	def __init__(self, poli, inherit_vecs = -1): #poli = [(1,0,2),(1,0,1)]
		individual.individ_count += 1
		self.age = 0
		self.id = individual.unique_id
		individual.unique_id += 1
		self.gens = set(poli)  #tuples inside
		#self.poli = poli
		#self.gen_chains_num_vecs = col.defaultdict(set) #dict: {num of gen in poli : vecs}
		#self.gen_chains_vec_nums = col.defaultdict(set) #dict: {vecs: num of gen in poli}
		self.gen_chains_gen_vecs = col.defaultdict(set)
		self.gen_chains_vec_gens = col.defaultdict(set)
		
		
		if (inherit_vecs != -1): #list(vec:nums, num:vecs)
			self.gen_chains_vec_gens = inherit_vecs[0]
			self.gen_chains_gen_vecs = inherit_vecs[1]
			
	def get_id(self):
		return self.id
	
	def add_gen_chain(self):
		col = np.random.randint(1, high = len(self.gens)-1) #unify discrete [low,high)
		gens = random.sample(self.gens, k=col) #positions of gens 
		if (gens == [1]):
			vec = "".join(str(x) for x in [1]*2**N)
		else:
			vec = "".join(str(x) for x in value_by_poly([i for i in gens]))
		for gen in gens:
			self.gen_chains_gen_vecs[gen].add(vec)
			self.gen_chains_vec_gens[vec].add(gen)
	
	def get_set_of_remaining_gens(self, gens): #set of gens which not will be included
		return self.gens - gens
	
		


#start
vect = '1111110110100110001101011111110011101101010111101110010001111101'
N = int(math.log(len(vect), 2))
pop1 = population(vect)

pop1.gen_start()
#pop1.crossing_faze_0()

for ind in pop1.individs:
	print('id = ', ind.get_id())
	print(list(ind.gens))
print('END')

for ind in pop1.individs:
	print(len(ind.gens))
if (len(pop1.individs) >= 5):
	for ind in pop1.individs[:3]:
		if (ind.gens & pop1.individs[3].gens or ind.gens & pop1.individs[4].gens):
			print("Yes")


#19.25s - один по 100
#100/100/87



