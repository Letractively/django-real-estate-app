# -*- coding: utf-8; -*-
from django import forms
from captcha.fields import CaptchaField
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.Form):
	name = forms.CharField(label=_("Name"), max_length=50)
	from_email = forms.EmailField(label=_("E-mail"), max_length=100)
	message = forms.CharField(
							  label=_("Mensage"), 
							  max_length=9000,
                              widget=forms.Textarea()
	)

	captcha = CaptchaField(label=_("Validator"))
