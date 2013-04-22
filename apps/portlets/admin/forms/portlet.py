# -*- coding: utf-8; -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from real_estate_app.apps.portlets.models import Portlet

class PortletAdminForm(forms.ModelForm):
	class Meta:
		model = Portlet 