# -*- coding: utf-8; -*-
from django import forms
from django.forms import DecimalField, CharField, ModelMultipleChoiceField, ModelForm 
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from real_estate_app.widgets import MoneyInputWidget, ZipInputWidget, CheckboxSelectMultipleCustom, AreaInputWidget
from real_estate_app.models import Property, AditionalThings

class PropertyAdminForm(ModelForm):
	price = DecimalField(widget=MoneyInputWidget)

	condominio = DecimalField(widget=MoneyInputWidget,required=False)
	iptu = DecimalField(widget=MoneyInputWidget,required=False)
	
	zip_code = CharField(widget=ZipInputWidget,required=False)

	aditionalthings_fk = ModelMultipleChoiceField(
									queryset=AditionalThings.objects.all(),
									required=False,
									widget=CheckboxSelectMultipleCustom
	)
	private_area = DecimalField(widget=AreaInputWidget,required=False)

	class Meta:
		model = Property

	#def clean_address(self):
		#address_key = self.cleaned_data['address']
		#if address_key:
		##	if self.Meta.model.get_by_key_name(slug_key):
			#try:
				#self.Meta.model.objects.get(slug=slugify(address_key))
				#print dir(Property._meta)
				#raise forms.ValidationError(_('Propertys with this address already exists.'))
			#except Property.DoesNotExist:
				#pass
		#else:
			#raise forms.ValidationError("This field is required....")

		#return address_key 

