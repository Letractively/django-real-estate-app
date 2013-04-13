from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

from real_estate_app.fields import EmailsListField  

class ContentMailForm(forms.Form):
	name = forms.CharField(label=_('Name'), max_length=150)
	from_email = forms.EmailField(label=_('To'), max_length=100)
	to = EmailsListField(label=_('From'),max_length=900)
	url = forms.CharField(label=_('URL'), max_length=900)
	captcha = CaptchaField(label=_('Validator'))                     

