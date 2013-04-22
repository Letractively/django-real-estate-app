# -*- coding: utf-8; -*-
from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from real_estate_app.apps.visitcalendar.models import VisitEvent, Visitor 
from real_estate_app.apps.propretys.models import Proprety

class VisitorForm(forms.ModelForm):

	class Meta:
		model=Visitor

class VisitEventForm(forms.ModelForm):

	class Meta:
		model = VisitEvent
		exclude = ('slug','create_date','enable_publish')

	# def save(self):
	# 	data=self.data.copy()
	# 	self.instance.slug=slugify(data['visitor_first_name']+data['visitor_last_name']+data['date_visit'])
	# 	return super(VisitEventForm,self).save()

	def __init__(self, *args, **kwargs):

		proprety_fk = kwargs.pop('proprety_fk','')
		date_visit = kwargs.pop('date_visit','')

		super(VisitEventForm, self).__init__(*args, **kwargs)
		
		if proprety_fk:
			self.fields['proprety_fk']=forms.ModelChoiceField(queryset=Proprety.objects.all_enabled(),
															  initial=Proprety.objects.get(id=proprety_fk.id))
		if date_visit:
			self.fields['date_visit']=forms.DateTimeField(initial=datetime.strptime(date_visit,'%Y-%m-%d %H:%M:%S'))