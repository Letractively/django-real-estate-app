# -*- coding: utf-8; -*-
from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from real_estate_app.apps.visitcalendar.models import TermVisit, Visitor
from real_estate_app.widgets import ZipInputWidget, PhoneInputWidget, CelphoneInputWidget

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class VisitorAdminForm(forms.ModelForm):
	if LANGUAGE_CODE in ('pt_BR','pt-br'):
		from django.contrib.localflavor.br import forms as br_forms
		from real_estate_app.localflavor.br.widgets import CPFInputWidget, RGInputWidget,\
														   CNPJInputWidget
		cpf = br_forms.BRCPFField(
			label='CPF',
			widget=CPFInputWidget,
		)

		rg = forms.CharField(
			label='RG',
			widget=RGInputWidget,
		)

		zip = br_forms.BRZipCodeField(
			label='CEP',
			widget=ZipInputWidget

		)

		work_zip = br_forms.BRZipCodeField(
			label='CEP Trabalho',
			widget=ZipInputWidget,
		)

		work_phone = br_forms.BRPhoneNumberField(
			label='Telefone trabalho',
			widget=PhoneInputWidget
		)
		celphone = br_forms.BRPhoneNumberField(
			label='Celular',
			widget=CelphoneInputWidget
		)

		phone = br_forms.BRPhoneNumberField(
			label='Telefone',
			widget=PhoneInputWidget
		)


	class Meta:
		model = Visitor

class VisitEventAdminForm(forms.ModelForm):
	def save(self,commit=True):
	  	data=self.data.copy()
	  	self.instance.slug=slugify(data['date_visit_1']+data['date_visit_0'])
	  	return super(VisitEventAdminForm,self).save(commit)

class TermVisitAdminForm(forms.ModelForm):
	def save(self,commit=True):
		term_visit=TermVisit.objects.all()
		if not term_visit or term_visit[0].id == getattr(self.instance,'id',''):
			return super(TermVisitAdminForm,self).save(commit)
		raise forms.ValidationError(_('Alredy exist a term visit registred on this site. You can only one.'))