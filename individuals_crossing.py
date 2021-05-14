import collections as col
import numpy as np
import scipy.stats as sts
import random
import sys
import time
import subprocess

from kir_one_shadow_performed_for_some_shadows import *



MAX_INDIVID_NUM = 25
MAX_ITER_FAZE_1 = 10
RESULT_INDIVID_NUM = 5
START_NUM = 3 #minimum = 2
CROSS_ITERS_START = 50

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
	
	#bad mutations
	bad_kir = 0
	bad_shannon = 0
	bad_minimize = 0
	#good mutations
	good_kir = 0
	good_shannon = 0
	good_minimize = 0
	def __init__(self, vec):
		self.individs = list() #list of individuals
		self.vec = vec
		self.crossing_iters = CROSS_ITERS_START
		
	def add_individ(self, poli, inherit_vecs = -1):
		if (inherit_vecs == -1):
			self.individs.append(individual(poli))
		else:
			self.individs.append(individual(poli, inherit_vecs))
	
	def check_faze(self):
		if (self.faze == 0 and self.popul_count >= MAX_INDIVID_NUM):
			self.faze = 1
			self.iter_faze = 0
		if (self.faze == 1 and self.iter_faze >= MAX_ITER_FAZE_1):
			self.faze = 2
			self.iter_faze = 0
		if (self.faze == 2 and self.popul_count <= RESULT_INDIVID_NUM):
			self.final()
			return -1
	
	def crossing_num(self):
		if (self.faze == 0):
			#percent of population from 100 in START_NUM to 20% in MAX_INDIVID_NUM
			perc = int(80/(START_NUM - MAX_INDIVID_NUM)*self.popul_count+100-240/(START_NUM - MAX_INDIVID_NUM))
			return int(self.popul_count*(perc/100))-1
		elif (self.faze == 1):
			return int(self.popul_count/5)
		elif (self.faze == 2):
			return int(self.popul_count/6)
	
	def crossing_params(self): #returns probabilities of dual crossing and number of individs in tournament
		if (self.faze == 0):
			poisson_rv = sts.poisson(1, loc = 3)
			num_tourn = poisson_rv.rvs(1)[0]
			probability_dual = 1 - math.log(self.popul_count, MAX_INDIVID_NUM)
			print("Probability of dual = ", probability_dual)
			print("Num of individs in tourn = ", num_tourn)
			return (probability_dual, num_tourn)
		elif (self.faze == 1):
			probability_dual = 0.2
			num_tourn = 4
			return (probability_dual, num_tourn)
		elif (self.faze == 2):
			probability_dual = 0.5
			num_tourn = 3
			return (probability_dual, num_tourn)
			
			
	def crossing(self):
		cr_num = self.crossing_num()
		print('Number of crosses: ', cr_num)
		for i in range(cr_num):
			print("Crossing ", i)
			p_dual, num_tourn = self.crossing_params()
			if (p_dual >= 0.1):
				bernoulli_rv = sts.bernoulli(p_dual)
				tourn_or_dual = bernoulli_rv.rvs(1)[0]
			else:
				tourn_or_dual = 1
			print("Tourn or dual = ", tourn_or_dual)
			if (tourn_or_dual == 1):
				if (self.crossing_dual(*random.sample(self.individs, k = 2)) == -1):
					return -1
			else:
				if (num_tourn > self.popul_count):
					num_tourn = self.popul_count
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
					f = open('log.txt','a')
					f.writelines('crossing_dual_error\n')
					f.writelines('first\n')
					f.writelines(str(ind1.gens)+ '\n')
					f.writelines(str(gens_crossed_1)+ '\n')
					f.writelines(str(new_pol1)+ '\n')
					f.writelines('second\n')
					f.writelines(str(ind2.gens)+ '\n')
					f.writelines(str(gens_crossed_2)+ '\n')
					f.writelines(str(new_pol2)+ '\n')
					f.writelines('crossing_dual_err_end\n')
					f.close()					
				else:
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
						f = open('log.txt','a')
						f.writelines('crossing_tourn_error\n')
						f.writelines('first\n')
						f.writelines(str(ind1.gens)+ '\n')
						f.writelines(str(gens_crossed_1)+ '\n')
						f.writelines(str(new_pol1)+ '\n')
						f.writelines('second\n')
						f.writelines(str(ind2.gens)+ '\n')
						f.writelines(str(gens_crossed_2)+ '\n')
						f.writelines(str(new_pol2)+ '\n')
						f.writelines('crossing_tourn_err_end\n')
						f.close()
					else:
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
		return 0
	
	def mutation(self):
		if (self.faze == 0):
			self.mutation_faze_0()
		elif (self.faze == 1):
			self.mutation_faze_1()
		elif (self.faze == 2):
			self.mutation_faze_2()
			
			
	def mutation_faze_0(self):
		#num of mutations
		#~ 0.5 mutation per unit
		for ind in self.individs:
			if (random.randint(0,1) == 1):
				if (len(ind.gens) >= 22):
					self.mutagen_kir(ind)
				elif (len(ind.gens) >= 14):
					self.mutagen_shennon(ind)
				else:
					self.mutagen_logic_minimize(ind)
		return 0
	
	def mutation_faze_1(self):
		#num of mutations
		#~ 0.5 mutation per unit
		for ind in self.individs:
			if (random.randint(0,1) >= 1):
				if (len(ind.gens) >= 22):
					self.mutagen_kir(ind)
				elif (len(ind.gens) >= 14):
					self.mutagen_shennon(ind)
				else:
					self.mutagen_logic_minimize(ind)
		return 0
	
	def mutation_faze_2(self):
		#num of mutations
		#~ 0.66% mutation per unit
		for ind in self.individs:
			if (random.randint(0,2) >= 1):
				if (len(ind.gens) >= 22):
					self.mutagen_kir(ind)
				elif (len(ind.gens) >= 14):
					self.mutagen_shennon(ind)
				else:
					self.mutagen_logic_minimize(ind)
		return 0
	
	def mutagen_kir(self, ind):
		gens_before = ind.gens
		num = random.randint(16, len(ind.gens)-1)
		sample = random.sample(ind.gens, num)
		old_gens = set(sample)
		new_gens = set(kir_with_min(''.join(str(x) for x in value_by_poly(sample))))
		if ("".join(str(x) for x in value_by_poly(list(ind.mini_upd(old_gens, new_gens)))) != self.vec):
			f = open('log.txt','a')
			f.writelines("Kir failed\n")
			f.writelines('before pol\n')
			f.writelines(str(gens_before)+ '\n')
			f.writelines('old gens\n')
			f.writelines(str(old_gens)+ '\n')
			f.writelines('new gens\n')
			f.writelines(str(new_gens)+ '\n')
			f.writelines('new pol\n')
			f.writelines(str(ind.mini_upd(old_gens, new_gens))+ '\n')
			f.writelines("Kir fail end\n")
			f.close()
			population.bad_kir += 1
		else:
			ind.update(old_gens, new_gens)
			population.good_kir += 1
	
	def mutagen_shennon(self, ind):
		gens_before = ind.gens
		num = random.randint(10, len(ind.gens)-1)
		sample = random.sample(ind.gens, num)
		old_gens = set(sample)
		res = subprocess.check_output(['poli.exe', '2', ''.join(str(x) for x in value_by_poly(sample))], encoding='utf-8')
		sharp_res = parse_sharp_out(res,N)
		new_gens = set(sharp_res)
		if ("".join(str(x) for x in value_by_poly(list(ind.mini_upd(old_gens, new_gens)))) != self.vec):
			f = open('log.txt','a')
			f.writelines("Shennon failed\n")
			f.writelines('before pol\n')
			f.writelines(str(gens_before)+ '\n')
			f.writelines('old gens\n')
			f.writelines(str(old_gens)+ '\n')
			f.writelines('new gens\n')
			f.writelines(str(new_gens)+ '\n')
			f.writelines('new pol\n')
			f.writelines(str(ind.mini_upd(old_gens, new_gens))+ '\n')
			f.writelines("Shennon fail end\n")
			f.close()
			population.bad_shannon += 1
		else:
			ind.update(old_gens, new_gens)
			population.good_shannon += 1
		
	def mutagen_bruteforce(self):
		pass
	
	def mutagen_logic_minimize(self, ind):
		try:
			gens_before = ind.gens
			s = set(logic_minimize(list(ind.gens)))
			if ("".join(str(x) for x in value_by_poly(list(ind.mini_upd(s)))) != self.vec):
				f = open('log.txt','a')
				f.writelines('Minimize failed\n')
				f.writelines('before pol\n')
				f.writelines(str(gens_before)+ '\n')
				f.writelines('new pol\n')
				f.writelines(str(ind.mini_upd(s))+ '\n')
				f.writelines('Minimize fail end\n')
				f.close()
				population.bad_minimize +=1
			else:
				ind.update(s)
				population.good_minimize +=1
		except:
			f = open('log.txt','a')
			f.writelines('Minimize failed with unexpected error\n')
			f.close()
		
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
		res = subprocess.check_output(['poli.exe', '2', vect], encoding='utf-8')
		sharp_res = parse_sharp_out(res,N)
		if ("".join(str(x) for x in value_by_poly(sharp_res)) != self.vec):
			print("Sharp failed")
			print(sharp_res)
		pop1.add_individ(sharp_res)
		print('ind_3_created')
		print("Start_lens")
		len(pop1.individs[0].gens)
		len(pop1.individs[1].gens)
		len(pop1.individs[2].gens)
	
	def selection(self):
		if (self.faze == 0):
			self.selection_faze_0()
		elif (self.faze == 1):
			self.selection_faze_1()
		elif (self.faze == 2):
			self.selection_faze_2()
	
	def selection_faze_0(self):
		pass
		
	def selection_faze_1(self):
		#probability 0.2 kill of > avg_len num
		avg_pop_len = 0
		k = 0
		for ind in self.individs:
			avg_pop_len += len(ind.gens) 
			k += 1
		avg_pop_len = int(avg_pop_len/k)
		i = 0
		while(i < len(self.individs)):
			if (len(self.individs[i].gens) > avg_pop_len):
				if (random.randint(1,10) >= 5):
					self.individs.remove(self.individs[i])
					i -= 1
			i += 1
	def selection_faze_2(self):
		#kill max ~0.5 prob
		while (self.popul_count < len(self.individs) + 1):
			max_ind = 0
			max = 0
			for ind in range(len(self.individs)):
				if (len(self.individs[ind].gens) > max):
					max_ind = ind
					max = len(self.individs[ind].gens)
			self.individs.remove(self.individs[max_ind])
	
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
	
	def end_of_iter(self):
		#cleaning_same
		#checking faze
		#info about iter
		self.cleaning_same_individs()
		self.iter_faze += 1
		self.iter_global += 1
		if (self.check_faze() == -1):
			return -1
		f = open(f"faze_{self.faze}_lens.txt","a")
		f.writelines(f"End of iter {self.iter_faze}\n")
		for ind in pop1.individs:
			f.writelines(str(len(ind.gens))+ '\n')
		f.close()
		#population_count
		f = open(f"population.txt","a")
		f.writelines(f"End of global iter {self.iter_global}\n")
		self.popul_count = len(self.individs)
		f.writelines(f"{self.popul_count}\n")
		f.close()
	
	def final(self):
		print("End")
		print("bad_kir = ", self.bad_kir)
		print("bad_shannon = ", self.bad_shannon)
		print("bad_minimize = ", self.bad_minimize)
		print("good_kir = ", self.good_kir)
		print("good_shannon = ", self.good_shannon)
		print("good_minimize = ", self.good_minimize)
		print("Min Final")
		min_len = 10000000
		id_min = 0
		for ind in range(len(pop1.individs)):
			l = len(pop1.individs[ind].gens)
			if (l < min_len):
				min_len = l
				id_min = pop1.individs[ind]
		print("min_len = ", min_len)
		print(pop1.individs[ind].gens)
	
	
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
				
	def mini_upd(self, old_gens, new_gens = -1):
		if (new_gens == -1): return old_gens
		else: return (self.gens - old_gens) ^ new_gens

#main part#
vect = '0111010100010000011000000101101010110001100000011001100101001110'
#vect = input()

N = int(math.log(len(vect), 2))
pop1 = population(vect)
pop1.gen_start()

while(True):
	print(pop1.iter_global)
	pop1.crossing()
	pop1.mutation()
	pop1.selection()
	if (pop1.end_of_iter() == -1):
		break

