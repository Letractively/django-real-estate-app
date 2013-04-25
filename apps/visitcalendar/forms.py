# -*- coding: utf-8; -*-
from datetime import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from real_estate_app.apps.visitcalendar.models import VisitEvent, Visitor 
from real_estate_app.apps.propertys.models import Property
from real_estate_app.widgets import AjaxInputWidget

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

if LANGUAGE_CODE in ('pt-br','pt_BR'):
	from real_estate_app.apps.visitcalendar.localflavor.br.forms import fields_visitor_form
else:
	from real_estate_app.apps.visitcalendar.localflavor.forms import fields_visitor_form

class VisitorForm(forms.ModelForm):

	pk = forms.CharField(
		'pk',
		widget=forms.widgets.HiddenInput,
		required=False,
	)

	cpf = forms.CharField(
						label=u'CPF',
						widget=AjaxInputWidget(
									model_fk=Visitor,
									help_text=_('Enter text to search.'),
									show_help_text=True,
									ajax_length=10
						)
	)

	class Meta:
		model=Visitor
		fields=fields_visitor_form
		#exclude=('create_date','enable_publish',)

class VisitEventForm(forms.ModelForm):

	class Meta:
		model = VisitEvent
		exclude = ('slug','create_date','enable_publish','visitor_fk')

	def save(self,commit=True):
	  	data=self.data.copy()
	  	self.instance.slug=slugify(data['date_visit'])
	  	return super(VisitEventForm,self).save(commit)

	def __init__(self, *args, **kwargs):

		property_fk = kwargs.pop('property_fk','')
		date_visit = kwargs.pop('date_visit','')

		super(VisitEventForm, self).__init__(*args, **kwargs)
		
		if property_fk:
			self.fields['property_fk']=forms.ModelChoiceField(queryset=Property.objects.all_enabled(),
															  initial=Property.objects.get(id=property_fk.id))
		if date_visit:
			self.fields['date_visit']=forms.DateTimeField(initial=datetime.strptime(date_visit,'%Y-%m-%d %H:%M:%S'))