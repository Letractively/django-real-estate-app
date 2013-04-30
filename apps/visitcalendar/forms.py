# -*- coding: utf-8; -*-
from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.contrib.localflavor.br.forms import BRCPFField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from real_estate_app.apps.visitcalendar.models import VisitEvent, Visitor 
from real_estate_app.apps.propertys.models import Property
from real_estate_app.widgets import AjaxInputWidget
from real_estate_app.conf.settings import REAL_ESTATE_APP_VISIT_EVENT_HOUR

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
	if LANGUAGE_CODE in ('pt-br','pt_BR'):
		cpf = BRCPFField(
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


class VisitEventForm(forms.ModelForm):

	class Meta:
		model = VisitEvent
		exclude = ('slug','create_date','enable_publish','visitor_fk')

	def save(self,commit=True):
	  	data=self.data.copy()
	  	self.instance.slug=slugify(data['date_visit'])
	  	return super(VisitEventForm,self).save(commit)

	def __init__(self, *args, **kwargs):
		
		if kwargs.has_key('initial'):
			property_fk = kwargs.get('initial').pop('property_fk','')
			date_visit = kwargs.get('initial').pop('date_visit','')
		else:
			property_fk = kwargs.pop('property_fk','')
			date_visit = kwargs.pop('date_visit','')

		super(VisitEventForm, self).__init__(*args, **kwargs)
		
		if property_fk:
			
			if type(property_fk) == unicode:
				pk=property_fk
			else:
				pk=property_fk.id
			self.fields['property_fk']=forms.ModelChoiceField(queryset=Property.objects.all_enabled(),
															  initial=Property.objects.get(id=pk))
		if date_visit:
			if not isinstance(date_visit,datetime):
				date_ini=datetime.strptime(date_visit,'%Y-%m-%d %H:%M:%S')
				self.fields['date_visit']=forms.DateTimeField(initial=date_ini)

	def clean_date_visit(self):
		date_visit=self.cleaned_data['date_visit']
		hours=timedelta(hours=REAL_ESTATE_APP_VISIT_EVENT_HOUR-1)
		visit_agenda=self._meta.model.objects.filter(date_visit__gte=date_visit,date_visit__lte=date_visit+hours)
		if visit_agenda:
			raise forms.ValidationError(_('Alredy exist a visit registred on this date and time'))
		return date_visit

class VisitEventAdminForm(forms.ModelForm):
	def save(self,commit=True):
	  	data=self.data.copy()
	  	self.instance.slug=slugify(data['date_visit_1']+data['date_visit_0'])
	  	return super(VisitEventAdminForm,self).save(commit)