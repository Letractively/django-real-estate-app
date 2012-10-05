# -*- coding: utf-8; -*-
from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
	name = forms.CharField(label="Nome", max_length=50)
	from_email = forms.EmailField(label="E-mail", max_length=100)
	message = forms.CharField(
							  label="Mensagem", 
							  max_length=9000,
                              widget=forms.Textarea()
	)

	captcha = CaptchaField(label="Validador")
