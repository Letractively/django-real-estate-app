# -*- coding: utf-8 -*-
import operator
from datetime import datetime

from django.db.models import Max, Min, Q
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import list_detail
from real_estate_app.models import Property, StatusProperty, District, Classification, AditionalThings

@requires_csrf_token
def property_list(request, *args, **kwargs):
	"""
	A view wrapper around ``django.views.generic.list_detail.object_list``.
	"""
	kwargs['queryset'] = Property.objects.all_enabled()
	post={}
	get={}

	if request.GET and request.GET.get('statusproperty'):
		
		status_id=StatusProperty.objects.filter(statusproperty=request.GET.get('statusproperty'))
		kwargs['queryset'] = kwargs['queryset'].filter(statusproperty_fk=status_id)	
		get=request.GET
	
	if request.POST:
		queryset = kwargs['queryset']
		post = request.POST.copy()
		post['aditionalthings_fk']=[]
		query_or=[]
		for query in request.POST.items():
			query=list(query)

			if query[0] not in ('x','y','csrfmiddlewaretoken') and query[1] != 'any' and query[1] != 'Em qualquer lugar':

				if query[0] == 'statusproperty_fk':
					try:
						query[1]=StatusProperty.objects.get(statusproperty=query[1])
					except StatusProperty.DoesNotExist:
						pass

				if query[0] == 'district_fk':
					try: 
						query[1]=District.objects.get(district=query[1])
						post['state_fk']=query[1].state_name
					except:
						pass

				if query[0] == 'classification_fk':
					try:
						query[1]=Classification.objects.get(classification=query[1])
						post['classification_fk']=query[1].classification
					except:
						pass

				if type(query[0]) == unicode:	
					query[0]=str(query[0])

				if query[0].startswith('aditionalthings_fk'):
					aditional=AditionalThings.objects.get(name=query[1])
					query_or.append(Q(aditionalthings_fk=aditional))
					post['aditionalthings_fk'].append(aditional.name)
					
				if not query[0].startswith('aditionalthings_fk'):
					query=dict((query,))
					queryset=queryset.filter(**query)

		if query_or:
			queryset=queryset.filter(reduce(operator.or_,query_or)).distinct()

		kwargs['queryset']=queryset

	return list_detail.object_list(request,extra_context={'post':post,'get':get}, *args, **kwargs)


def property_detail(request, *args, **kwargs):
	"""
	A view wrapper around ``django.views.generic.list_detail.object_detail``.
	"""
	kwargs['queryset'] = Property.objects.all_enabled()
	return list_detail.object_detail(request, *args, **kwargs)