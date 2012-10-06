def radomstring(max=10):
	import random
	string='abcdefghijklmnopqrstuvxywz1234567890'
	a=''
	for i in random.sample(string,max):
		a+=i
	return a


def make_dv(num,max_num=11,b_start=1):
	dv1=0
	for ct, n in enumerate(num,start=b_start):
		dv1+=int(n)*ct

	dv1=dv1%11

	if dv1 == 10: dv1=0;

	num=num+str(dv1)
	if len(num) != max_num:
		num=make_dv(num,max_num=max_num,b_start=0)
	
	return num or None
