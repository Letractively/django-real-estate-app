# -*- coding: utf-8; -*-
from django import forms
from django.forms import CharField, ChoiceField, DecimalField, ModelMultipleChoiceField, ModelForm
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

# TODO: better the get STATE_CHOICES for locale on settings
from django.contrib.localflavor.br.br_states import STATE_CHOICES

from real_estate_app.apps.propertys.admin.widgets import StateDistrictAdminSelect
from real_estate_app.apps.propertys.models import Property, AditionalThings 
from real_estate_app.apps.realtors.models import Realtor
from real_estate_app.widgets import MoneyInputWidget, ZipInputWidget, CheckboxSelectMultipleCustom, \
								    AreaInputWidget, AdminAjaxSelectMultipleInputWidget


class PropertyAdminForm(ModelForm):
	
	price = DecimalField(label=_('price'),widget=MoneyInputWidget)

	condominio = DecimalField(widget=MoneyInputWidget,required=False)

	iptu = DecimalField(widget=MoneyInputWidget,required=False)
	
	zip_code = CharField(label=_('Zip code'), widget=ZipInputWidget,required=False)

	aditionalthings_fk = ModelMultipleChoiceField(
									label=_('Aditional things'),
									queryset=AditionalThings.objects.all(),
									required=False,
									widget=CheckboxSelectMultipleCustom(
										app_name='propertys',
										module_name='aditionalthings',
										field='name'
									)
	)
	realtor_fk = ModelMultipleChoiceField(
									label=_('Realtor'),
									queryset=Realtor.objects.all(),
									required=False,
									widget=AdminAjaxSelectMultipleInputWidget(
											model_fk=Realtor,
											help_text=_('Enter text to search.'),
											show_help_text=True
									)
	)

	private_area = DecimalField(widget=AreaInputWidget,required=False)

	state = ChoiceField(
						label=_('State'),
						widget=StateDistrictAdminSelect,
						choices=STATE_CHOICES,
						initial='DF',
	)

	class Meta:
		model = Property