# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin 
from django.contrib.auth.models import User 
from django.db import models, transaction
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from options import RealEstateAppRevertInlineModelAdmin
from real_estate_app.models import Realtor
from real_estate_app.admin.forms import RealtorAdminForm, UserAdminForm
from real_estate_app.conf.settings import MEDIA_PREFIX

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

csrf_protect_m = method_decorator(csrf_protect)

if LANGUAGE_CODE in ('pt_BR','pt-br'):
	from real_estate_app.localflavor.br.admin.forms.realtor import realtor_br_fieldsets
	fieldsets = realtor_br_fieldsets


class RealtorInlineAdmin(admin.StackedInline):
	model = Realtor
	extra = 1
	form = RealtorAdminForm
	if LANGUAGE_CODE:
		template = 'admin/real_estate_app/%s/edit_inline/stacked-realtor.html' % LANGUAGE_CODE



class RealtorAdmin(RealEstateAppRevertInlineModelAdmin):

	revert_inlines = [RealtorInlineAdmin,]
	revert_model = User
	revert_form = UserAdminForm

	class Media:

		if LANGUAGE_CODE == 'pt-br':
			css = {
				'all':(
					MEDIA_PREFIX+"css/tabs.css",
				)
			}

			js = (
				MEDIA_PREFIX+"js/locale/pt_BR/realtor.js",
			)

admin.site.register(Realtor, RealtorAdmin)