# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin 
from django.contrib.auth.models import User 
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from real_estate_app.admin.forms import UserAdminForm
from real_estate_app.admin.options import RealEstateAppRevertInlineModelAdmin
from real_estate_app.conf.settings import MEDIA_PREFIX as MEDIA_PREFIX_REAL_ESTATE
from real_estate_app.apps.realtors.models import Realtor
from real_estate_app.apps.realtors.admin.forms import RealtorAdminFormSet



LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class RealtorInlineAdmin(admin.StackedInline):
	model = Realtor
	extra = 1
	formset = RealtorAdminFormSet
	template = 'admin/real_estate_app/%s/edit_inline/stacked-realtor.html' % LANGUAGE_CODE

	if LANGUAGE_CODE in ('pt_BR','pt-br'):
		from django.contrib.localflavor.br import forms as br_forms
		from real_estate_app.localflavor.br.admin.forms.realtor import realtor_br_custom_fields

		fields = realtor_br_custom_fields

		cpf = br_forms.BRCPFField(
							label=u'CPF',
							required=False
		)

		cnpj = br_forms.BRCNPJField(
							label=u'CNPJ',
							required=False
		)
	
class RealtorAdmin(RealEstateAppRevertInlineModelAdmin):

	revert_inlines = [RealtorInlineAdmin,]
	
	revert_model = User
	
	revert_form = UserAdminForm
	
	model = Realtor

	search_fields=['user__first_name','user__last_name','user__email']
	
	list_display = ['name','user']
	
	list_filter=['logical_exclude']

	if LANGUAGE_CODE == 'pt-br':
		list_display+=['tipo_pessoa','creci']
		list_filter+=['tipo_pessoa']
		search_fields+=['creci']

	class Media:

		js = [
				MEDIA_PREFIX_REAL_ESTATE+"js/meio.mask.min.js",
				MEDIA_PREFIX_REAL_ESTATE+"js/real_estate_app_masks.js"
		]

		if LANGUAGE_CODE == 'pt-br':
			css = {
				'all':(
					MEDIA_PREFIX_REAL_ESTATE+"css/tabs.css",
					MEDIA_PREFIX_REAL_ESTATE+"css/jscrollpane.css",
					MEDIA_PREFIX_REAL_ESTATE+"css/jscrollpane-custom.css",
				)
			}

			js += [
				MEDIA_PREFIX_REAL_ESTATE+"js/locale/pt_BR/realtor.js",
				MEDIA_PREFIX_REAL_ESTATE+"js/jquery.mousewheel.js",
		      	MEDIA_PREFIX_REAL_ESTATE+"js/jquery.jscrollpane.min.js",
		      	MEDIA_PREFIX_REAL_ESTATE+"js/real_estate_app_popup_scroll.js"
			]

admin.site.register(Realtor, RealtorAdmin)