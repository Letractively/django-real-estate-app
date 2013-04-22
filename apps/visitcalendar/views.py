# -*- coding: utf-8 -*-
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import list_detail
from django.views.generic.create_update import update_object
from django.utils.safestring import mark_safe

from django.forms.models import modelform_factory

from real_estate_app.apps.visitcalendar.models import VisitEvent, Visitor
from real_estate_app.apps.visitcalendar.forms import VisitEventForm
from real_estate_app.apps.propretys.models import Proprety
from real_estate_app.views.generic import create_object

def visitcalendar_list_json(request, *args, **kwargs):
	if kwargs['slug']:
		proprety=get_object_or_404(Proprety,slug=kwargs['slug'])
		visitsevents = VisitEvent.objects.filter(proprety_fk=proprety)
		kwargs['extra_context']= {'calendar_url_json':'/imoveis/calendar/json/'+kwargs['slug']}
		events = []
		
		for visitevent in visitsevents:
			events.append(dict(
						title=_('Has visit'),
						start = visitevent.date_visit.strftime('%Y-%m-%d %H:%M:%S'),
						url = visitevent.get_absolute_url()
			))

	else:
		visitsevents = VisitEvent.objects.all()

		events = []
		for visitevent in visitsevents:
			events.append(dict(
						title= _('Has visit: \n %s') % visitevent.proprety_fk.address,
						start = visitevent.date_visit.strftime('%Y-%m-%d %H:%M:%S'),
						url = visitevent.get_absolute_url()
			))

	return HttpResponse(simplejson.dumps(events),mimetype='application/json')
	

@requires_csrf_token
def visitcalendar_list(request, *args, **kwargs):	
	kwargs['queryset'] = VisitEvent.objects.all()
	kwargs['extra_context']= {'calendar_url_json':'/imoveis/calendar/json/'}
	return list_detail.object_list(request, *args, **kwargs)

def visitcalendar_list_proprety_visit(request, *args, **kwargs):
	"""
	A view wrapper around ``django.views.generic.list_detail.object_list`.
	"""
	proprety=get_object_or_404(Proprety,slug=kwargs['slug'])
	kwargs['queryset'] = VisitEvent.objects.filter(proprety_fk=proprety)
	kwargs['extra_context']= {'calendar_url_json':'/imoveis/calendar/json/'+kwargs['slug'],'proprety':proprety}
	kwargs.pop('slug')

	return list_detail.object_list(request, *args, **kwargs)

@requires_csrf_token
def visitcalendar_create_object(request, *args, **kwargs):
	date_visit=request.GET.get('date_visit','')
	proprety=get_object_or_404(Proprety,slug=kwargs['slug'])


	kwargs.pop('slug')
	kwargs['form_class']=modelform_factory(Visitor)
	#import pdb;pdb.set_trace()
	#kwargs['initial']={'visitevent_proprety_fk':proprety,'visitevent_date_visit':date_visit}
	
	return create_object(request, *args, **kwargs)

@requires_csrf_token
def visitcalendar_update_object(request, *args, **kwargs):
	proprety=get_object_or_404(Proprety,slug=kwargs['proprety_slug'])
	kwargs.pop('proprety_slug')
	kwargs['form_class']=VisitEventForm
	
	return update_object(request, *args, **kwargs)