# -*- coding: utf-8; -*-
from datetime import datetime, timedelta

from django import forms
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from real_estate_app.apps.visitcalendar.models import TermVisit 

class VisitEventAdminForm(forms.ModelForm):
	def save(self,commit=True):
	  	data=self.data.copy()
	  	self.instance.slug=slugify(data['date_visit_1']+data['date_visit_0'])
	  	return super(VisitEventAdminForm,self).save(commit)

class TermVisitAdminForm(forms.ModelForm):
	def save(self,commit=True):
		term_visit=TermVisit.objects.all()
		if not term_visit or term_visit[0].id == getattr(self.instance,'id',''):
			return super(TermVisitAdminForm,self).save(commit)
		raise forms.ValidationError(_('Alredy exist a term visit registred on this site. You can only one.'))