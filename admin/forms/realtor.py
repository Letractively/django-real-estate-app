# -*- coding: utf-8; -*-
from django.conf import settings
from django.forms import ModelForm, CharField, ValidationError
from django.forms.fields import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

from real_estate_app.models import Realtor

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

# utilizar formset
from django.forms.models import BaseInlineFormSet

# class RealtorAdminForm(ModelForm):

# 	class Meta:
# 		model = Realtor

class RealtorAdminForm(BaseInlineFormSet):
	
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
				elif data.has_key('tipo_pessoa') and data.get('tipo_pessoa') == 'PJ':
					fields_check=['cnpj','razao_social','creci']
				else:
					fields_check=['cpf','rg','ssp','cnpj','razao_social','creci']

				try:
					self.check_empty_fields(form,data,fields_check)
				except:			
					raise ValidationError('Ops... you try something wrong!')

				if not (data.get('tipo_pessoa', False) or (data.get('cpf', False) and data.get('cnpj', False)) ):
					return False
					

		return super(RealtorAdminForm,self).clean()