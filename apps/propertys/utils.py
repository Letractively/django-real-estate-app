def make_dv(num,max_num=11,b_start=1):
	try:
		if len(num) < (max_num-2):
			tmp_n=''
			for e in range((max_num-2)-len(num)):
			 	tmp_n+='0'
			num=tmp_n+num

		dv1=0
		for ct, n in enumerate(num,start=b_start):
			dv1+=int(n)*ct

		dv1=dv1%11

		if dv1 == 10: dv1=0;

		num=num+str(dv1)
		if len(num) != max_num:
			num=make_dv(num,max_num=max_num,b_start=0)
		
		return num or None
	except TypeError:
		raise Exception('The num you pass is greater than max_num. Default max_num is 11. Please pass the max_num bigger than you has passed.')