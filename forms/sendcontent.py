from django import forms
from captcha.fields import CaptchaField

from real_estate_app.fields import EmailsListField  

class ContentMailForm(forms.Form):
	name = forms.CharField(label='Nome', max_length=150)
	from_email = forms.EmailField(label='De', max_length=100)
	to = EmailsListField(label='Para',max_length=900)
	url = forms.CharField(label='URL', max_length=900)
	captcha = CaptchaField(label='Validador')                     

