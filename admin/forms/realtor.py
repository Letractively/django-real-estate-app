# -*- coding: utf-8; -*-
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.forms import ModelForm, EmailField, CharField
from django.forms.models import save_instance, construct_instance

from real_estate_app.models import Realtor

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

# utilizar formset

class RealtorAdminForm(ModelForm):

	class Meta:
		model = Realtor