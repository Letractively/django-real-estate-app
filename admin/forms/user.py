# -*- coding: utf-8; -*-
from django.contrib.auth.models import User
from django.conf import settings
from django.forms import EmailField, CharField, ValidationError, HiddenInput
from django.utils.translation import ugettext_lazy as _

from real_estate_app.conf.settings import MEDIA_PREFIX
from real_estate_app.admin.forms.popup import PopUpModelForm

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class UserAdminForm(PopUpModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username=CharField(widget=HiddenInput, required=False)
    
    first_name=CharField(label=_('First name'), required=True)

    last_name=CharField(label=_('Last name'), required=True)

    email=EmailField(label=_('E-mail'), required=True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email',) 

    def clean_username(self):
        username = self.data['email']
        return username

    def clean_email(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(_("A user with that email already exists."))
        
