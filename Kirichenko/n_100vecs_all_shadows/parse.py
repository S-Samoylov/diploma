f = open('result_vec_100_n_3_all_shadows.txt','r')
lines = f.read().split('\n')
f.close()
n = 3
d = dict()
j = 0
min = 10000
for x in lines[9::10]:
	if (j == 9):
		j = 0
		print(min)
		print(d.values())
		min = 10000
		d = dict()
	pol = []
	s = x.replace('x','').split('+')
	for v in range(len(s)):
		pol.append([0]*n)
	i = 0
	for v in s:
		v = v.split('*')# 	['~1','2']
		for f in v:
			if (f[0] == '~'):
				pol[i][int(f[1])-1] = 2
			else:
				pol[i][int(f[0])-1] = 1
		i += 1
	if (min > len(pol)): min = len(pol)
	if (str(pol) in d):
		d[str(pol)] += 1
	else:
		d[str(pol)] = 1
	j += 1