# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import admin 
from django.contrib.auth.models import User 


from options import RealEstateAppRevertInlineModelAdmin
from real_estate_app.models import Realtor
from real_estate_app.admin.forms import RealtorAdminForm, UserAdminForm
from real_estate_app.conf.settings import MEDIA_PREFIX

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

fieldsets= (
			(_('General Information'), {
				'fields': ('first_name','last_name','email','sex','photo'),
			}),
)

if LANGUAGE_CODE in ('pt_BR','pt-br'):
	from real_estate_app.localflavor.br.admin.forms.realtor import realtor_br_fieldsets
	fieldsets = realtor_br_fieldsets


class RealtorInlineAdmin(admin.StackedInline):
	model = Realtor
	extra =1

class RealtorAdmin(RealEstateAppRevertInlineModelAdmin):
 	#fieldsets = fieldsets
	revert_inlines = [RealtorInlineAdmin,]
	revert_model = User
	revert_form = UserAdminForm
	class Media:
		#MEDIA_PREFIX+"js/real_estate_app_popup.js",
		js = (
			MEDIA_PREFIX+"js/locale/pt_BR/realtor.js",
		)







admin.site.register(Realtor, RealtorAdmin)
