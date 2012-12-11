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
        

    def clean(self):
        super(UserAdminForm,self).clean()
        username = self.data['email']
        # if LANGUAGE_CODE in ('pt-br','pt_BR'):
        #     username = self.data['CPF']
        
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            self.cleaned_data['username']=username
            return self.cleaned_data

        raise ValidationError(_("A user with that username already exists."))
        
