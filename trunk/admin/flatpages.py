# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from real_estate_app.conf.settings import MEDIA_PREFIX

class FlatPageAdminCustom(FlatPageAdmin):
	class Media:
		js = (
			  MEDIA_PREFIX+'js/tiny_mce/tiny_mce.js',
		      MEDIA_PREFIX+'js/tiny_mce/textarea.js',
		)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage,FlatPageAdminCustom)

