import collections as col
import numpy as np
import scipy.stats as sts
import random
import sys
import time
import subprocess
sys.path.append("C:\\diploma\\Kirichenko")
from kir_one_shadow import *



MAX_INDIVID_NUM = 1000
MAX_ITER_FAZE_1 = 99
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
				if (self.crossing_dual(*random.sample(self.individs, k = 2)) == -1):
					return -1
			else:
				if (num_tourn > individual.individ_count):
					num_tourn = individual.individ_count
				if (self.crossing_tourn(random.sample(self.individs, k = num_tourn)) == -1):
					return -1
		
		

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
				new_pol1 = ind1.get_set_of_remaining_gens(gens_crossed_1) ^ new_gens_set_1
				defected_gens1 = ind1.get_set_of_remaining_gens(gens_crossed_1) & new_gens_set_1
				new_pol2 = ind2.get_set_of_remaining_gens(gens_crossed_2) ^ new_gens_set_2
				defected_gens2 = ind2.get_set_of_remaining_gens(gens_crossed_2) & new_gens_set_2
				d1 = col.defaultdict(set)#vec:gens
				d2 = col.defaultdict(set)#gen:vecs
				#полный проход по словарю в поиске цепочек с этими генfvb
				for vec, gens_set in ind1.gen_chains_vec_gens.items():
					#если гены не пересекаются с изменёнными то наследуем
					if (gens_set & (gens_crossed_1 | defected_gens1) == set()):
						d1[vec] |= gens_set
						for gen in gens_set:
							d2[gen].add(vec)
				inh1 = [d1,d2]
				
				d3 = col.defaultdict(set)#vec:gens
				d4 = col.defaultdict(set)#gen:vecs
				for vec, gens_set in ind2.gen_chains_vec_gens.items():
					#если гены не пересекаются с изменёнными то наследуем
					if (gens_set & (gens_crossed_2 | defected_gens2) == set()):
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
					print(new_pol1)
					print('second')
					print(ind2.gens)
					print(gens_crossed_2)
					print(new_pol2)
					return -1					
				
				acp1 = False
				acp2 = False
				for ind in self.individs:
					if (new_pol1 == ind.gens):
						acp1 = True
					if (new_pol2 == ind.gens):
						acp2 = True
				if (acp1 == False): self.add_individ(new_pol1, inh1)#inharit chains
				if (acp2 == False): self.add_individ(new_pol2, inh2)#inharit chains
				break
		print("Crossing_dual_ended")
		print("id1 = ", ind1.get_id(), "id2 = ", ind2.get_id())
		return 0
			
	def crossing_tourn(self, ind_list):#ind - list of individuals
		print("Crossing_tourn_started")
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
		d_ind = col.defaultdict(list)
		for ind in ind_list:
			print("id = ", ind.get_id())
		for k in range(self.crossing_iters):
			for i in range(100):
				for ind in ind_list:
					ind.add_gen_chain()
			#checking sets
			s = set()
			for ind in ind_list:
				for next_ind in ind_list[ind_list.index(ind)+1:]:
					s1 = ind.gen_chains_vec_gens.keys()
					s2 = next_ind.gen_chains_vec_gens.keys()
					perec = s1 & s2
					if (perec != set()):
						#checking same subpols
						for vec in perec:
							if (ind.gen_chains_vec_gens[vec] != next_ind.gen_chains_vec_gens[vec]):
								s.add(vec)
								d_ind[vec].append(ind)
								d_ind[vec].append(next_ind)
				#if (len(s) != 0): break
			
			
			if (len(s) != 0):
			
				#create childs with gen_chains
				print('Crossing on iter = ', k*100)
				for vec in s:
					#choice 2 inds
					ind1, ind2 = random.sample(d_ind[vec], 2)
					
					gens_crossed_1 = ind1.gen_chains_vec_gens[vec] #positions of changed gens in pol1
					gens_crossed_2 = ind2.gen_chains_vec_gens[vec] #positions of changed gens in pol2
					new_gens_set_1 = gens_crossed_2 #set of new gens for 1 
					new_gens_set_2 = gens_crossed_1 #set of new gens for 2
					new_pol1 = ind1.get_set_of_remaining_gens(gens_crossed_1) ^ new_gens_set_1
					defected_gens1 = ind1.get_set_of_remaining_gens(gens_crossed_1) & new_gens_set_1
					new_pol2 = ind2.get_set_of_remaining_gens(gens_crossed_2) ^ new_gens_set_2
					defected_gens2 = ind2.get_set_of_remaining_gens(gens_crossed_2) & new_gens_set_2
					d1 = col.defaultdict(set)#vec:gens
					d2 = col.defaultdict(set)#gen:vecs
					#полный проход по словарю в поиске цепочек с этими генfvb
					for vec, gens_set in ind1.gen_chains_vec_gens.items():
						#если гены не пересекаются с изменёнными то наследуем
						if (gens_set & (gens_crossed_1 | defected_gens1) == set()):
							d1[vec] |= gens_set
							for gen in gens_set:
								d2[gen].add(vec)
					
					inh1 = [d1,d2]
					
					d3 = col.defaultdict(set)#vec:gens
					d4 = col.defaultdict(set)#gen:vecs
					for vec, gens_set in ind2.gen_chains_vec_gens.items():
						#если гены не пересекаются с изменёнными то наследуем
						if (gens_set & (gens_crossed_2 | defected_gens2) == set()):
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
						print(new_pol1)
						print('second')
						print(ind2.gens)
						print(gens_crossed_2)
						print(new_pol2)
						return -1
					
					acp1 = False
					acp2 = False
					for ind in self.individs:
						if (new_pol1 == ind.gens):
							acp1 = True
						if (new_pol2 == ind.gens):
							acp2 = True
					if (acp1 == False):
						self.add_individ(new_pol1, inh1)#inharit chains
						print("New individ by tourn")
					if (acp2 == False):
						self.add_individ(new_pol2, inh2)#inharit chains
						print("New individ by tourn")
					if (acp1 == False or acp2 == False):
						break
				break
		print("Crossing_tourn_ended")
		print("id1 = ", ind1.get_id(), "id2 = ", ind2.get_id())
		return 0
	
	def mutation_faze_0(self):
		#num of mutations
		#phase 0 - 0.5 mutation per unit
		for ind in self.individs:
			if (random.randint(0,1) == 1):
				if (len(ind.gens) >= 24):
					if (self.mutagen_kir(ind) == -1):
						print("Kir failed")
						return -1
				elif (len(ind.gens) >= 15):
					if (self.mutagen_shennon(ind) == -1):
						print("Shennon failed")
						return -1
				else:
					if (self.mutagen_logic_minimize(ind) == -1):
						print("Logic minimize failed")
						return -1
			
		return 0
	
	def mutagen_kir(self, ind):
		gens_before = ind.gens
		num = random.randint(20, len(ind.gens)-1)
		sample = random.sample(ind.gens, num)
		old_gens = set(sample)
		new_gens = set(kir_with_min(''.join(str(x) for x in value_by_poly(sample))))
		ind.update(old_gens, new_gens)
		if ("".join(str(x) for x in value_by_poly(list(ind.gens))) != self.vec):
			print('before pol')
			print(gens_before)
			print('old gens')
			print(old_gens)
			print('new gens')
			print(new_gens)
			print('new pol')
			print(ind.gens)
			return -1
	
	def mutagen_shennon(self, ind):
		pass
		'''
		gens_before = ind.gens
		num = random.randint(13, len(ind.gens)-1)
		sample = random.sample(ind.gens, num)
		old_gens = set(sample)
		res = subprocess.check_output(['C:\\diploma\\с#\\poli\\poli\\bin\\Debug\\poli.exe', '2', ''.join(str(x) for x in value_by_poly(sample))], encoding='utf-8')
		sharp_res = parse_sharp_out(res,N)
		new_gens = set(sharp_res)
		ind.update(old_gens, new_gens)
		if ("".join(str(x) for x in value_by_poly(list(ind.gens))) != self.vec):
			print('before pol')
			print(gens_before)
			print('old gens')
			print(old_gens)
			print('new gens')
			print(new_gens)
			print('new pol')
			print(ind.gens)
			return -1
		'''
		
	def mutagen_bruteforce(self):
		pass
	
	def mutagen_logic_minimize(self, ind):
		gens_before = ind.gens
		s = set(logic_minimize(list(ind.gens)))
		ind.update(s)
		if ("".join(str(x) for x in value_by_poly(list(ind.gens))) != self.vec):
			print('before pol')
			print(gens_before)
			print('new pol')
			print(ind.gens)
			return -1
	
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
		sharp_res = parse_sharp_out(res,N)
		if ("".join(str(x) for x in value_by_poly(sharp_res)) != self.vec):
			print("Sharp failed")
			print(sharp_res)
		pop1.add_individ(sharp_res)
		print('ind_3_created')
	
	def logic_minimize_population(self):
		pass
		
	def cleaning_same_individs(self):
		i = 0
		num_deleted = 0 
		while(i < len(self.individs)):
			for ind in self.individs[i+1:]:
				if (self.individs[i].gens == ind.gens):
					#merge vecs
					self.individs[i].gen_chains_gen_vecs.update(ind.gen_chains_gen_vecs)
					self.individs[i].gen_chains_vec_gens.update(ind.gen_chains_vec_gens)
					#remove
					self.individs.remove(ind)
					num_deleted += 1
					break
					i -= 1
			i+=1
		return num_deleted 
		
		
		
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
	
	def add_gen_chain(self): #returns vec
		col = np.random.randint(1, high = len(self.gens)-1) #unify discrete [low,high)
		gens = random.sample(self.gens, k=col) #positions of gens 
		if (gens == [1]):
			vec = "".join(str(x) for x in [1]*2**N)
		else:
			vec = "".join(str(x) for x in value_by_poly([i for i in gens]))
		for gen in gens:
			self.gen_chains_gen_vecs[gen].add(vec)
			self.gen_chains_vec_gens[vec].add(gen)
		return vec
		
	def get_set_of_remaining_gens(self, gens): #set of gens which not will be included
		return self.gens - gens
	
	def update(self, old_gens , new_gens = -1):
		if (new_gens == -1): self.gens = old_gens
		else: self.gens = (self.gens - old_gens) ^ new_gens
		d = col.defaultdict(set)
		for vec, gens in self.gen_chains_vec_gens.items():
			d[vec] = gens
		for vec, gens in d.items():
			if (self.gen_chains_vec_gens[vec] not in self.gens):
				del self.gen_chains_vec_gens[vec]
		s = set(self.gen_chains_vec_gens.keys())
		d = col.defaultdict(set)
		for gen, vecs in self.gen_chains_gen_vecs.items():
			d[gen] = vecs
		for gen, vecs in d.items():
			if (gen not in self.gens):
				del self.gen_chains_gen_vecs[gen]
			else:
				self.gen_chains_gen_vecs[gen] &= s

#main part#
vect = '1111110110100110001101011111110011101101010111101110010001111101'
N = int(math.log(len(vect), 2))
pop1 = population(vect)

pop1.gen_start()

timess = []

for its in range(10):
	print(pop1.iter_faze)
	start = time.time()
	if (pop1.crossing_faze_0() == -1):
		break
	end = time.time()
	timess.append(end-start)
	if (pop1.mutation_faze_0() == -1):
		print("Mutation failed")
		break
	#after mutations
	print(f"Deleted in faze {pop1.iter_faze} = ", pop1.cleaning_same_individs())
	for ind in pop1.individs:
		print('id = ', ind.get_id())
		print(list(ind.gens))
	print('END')

	for ind in pop1.individs:
		print(len(ind.gens))
	
	pop1.iter_faze += 1

for i in range(len(timess)):
	print(" faze = ", i, timess[i])

print("Start_lens")
len(pop1.individs[0].gens)
len(pop1.individs[1].gens)
len(pop1.individs[2].gens)

print("Min Final")
min_len = 10000000
id_min = 0
for ind in pop1.individs[3:]:
	l = len(ind.gens)
	if (l < min_len):
		min_len = l
		id_min = ind.get_id()
print("id = ", id_min)
print("min_len = ", min_len)


#19.25s - один по 100
#100/100/87



