# -*- coding: utf-8; -*-
from django.conf import settings
from django.forms import ValidationError, ModelForm, CharField
from django.forms.fields import EMPTY_VALUES
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _

from real_estate_app.apps.realtors.models import Realtor
from real_estate_app.widgets import PhoneInputWidget, CelphoneInputWidget

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class RealtorAdminForm(ModelForm):
	if LANGUAGE_CODE in ('pt_BR','pt-br'):
		from django.contrib.localflavor.br import forms as br_forms
		from real_estate_app.localflavor.br.widgets import CPFInputWidget, RGInputWidget,\
														   CNPJInputWidget

		cpf = br_forms.BRCPFField(
							label=u'CPF',
							widget=CPFInputWidget,
							required=False
		)

		cnpj = br_forms.BRCNPJField(
							label=u'CNPJ',
							widget=CNPJInputWidget,
							required=False
		)

		phone = br_forms.BRPhoneNumberField(
							label=_('Phone'),
							widget=PhoneInputWidget,
							required=False
		)

		celphone = br_forms.BRPhoneNumberField(
							label=_('Celphone'),
							widget=CelphoneInputWidget,
							required=False
		)

		rg = CharField(
							label='RG',
							widget=RGInputWidget,
							required=False
		)



	class Meta:
		model = Realtor

class RealtorAdminFormSet(BaseInlineFormSet):

	model = Realtor	

	def check_empty_fields(self,form, data, fields=[]):
		for field in fields:
			if data.get(field) in EMPTY_VALUES:
				form.errors[field]=form.error_class([_(u'This field is required.')])
	
	def clean(self):

		for form in self.forms:

			if not hasattr(form, 'cleaned_data'):
				continue

			data = form.cleaned_data.copy()
			
			if LANGUAGE_CODE in ('pt_BR','pt-br'):
				
				if data.has_key('tipo_pessoa') and data.get('tipo_pessoa') == 'PF':
					fields_check=['cpf','rg','ssp','creci']
					remove_values=['cnpj','razao_social']
				elif data.has_key('tipo_pessoa') and data.get('tipo_pessoa') == 'PJ':
					fields_check=['cnpj','razao_social','creci']
					remove_values=['cpf','rg','ssp']
				else:
					fields_check=['cpf','rg','ssp','creci','cnpj','razao_social']
					remove_values=[]
				try:
					self.check_empty_fields(form,data,fields_check)					
				except:			
					raise ValidationError('Ops... you try something wrong!')

				if not (data.get('tipo_pessoa', False) or (data.get('cpf', False) and data.get('cnpj', False)) ):
					return False
					

		return super(RealtorAdminFormSet,self).clean()