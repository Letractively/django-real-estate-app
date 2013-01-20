# -*- coding: utf-8; -*-
from django import forms
from django.forms import DecimalField, CharField, ModelMultipleChoiceField, ModelForm 
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from real_estate_app.widgets import MoneyInputWidget, ZipInputWidget, CheckboxSelectMultipleCustom, AreaInputWidget, AjaxSelectMultipleInputWidget
from real_estate_app.models import Property, AditionalThings, Realtor

class PropertyAdminForm(ModelForm):
	
	price = DecimalField(label=_('price'),widget=MoneyInputWidget)

	condominio = DecimalField(widget=MoneyInputWidget,required=False)

	iptu = DecimalField(widget=MoneyInputWidget,required=False)
	
	zip_code = CharField(label=_('Zip code'), widget=ZipInputWidget,required=False)

	aditionalthings_fk = ModelMultipleChoiceField(
									label=_('Aditional things'),
									queryset=AditionalThings.objects.all(),
									required=False,
									widget=CheckboxSelectMultipleCustom
	)
	realtor_fk = ModelMultipleChoiceField(
									label=_('Realtor'),
									queryset=Realtor.objects.all(),
									required=False,
									widget=AjaxSelectMultipleInputWidget(
											model_fk=Realtor,
											help_text=_('Enter text to search.'),
											show_help_text=True
									)
	)

	private_area = DecimalField(widget=AreaInputWidget,required=False)

	class Meta:
		model = Property