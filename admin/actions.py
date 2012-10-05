# -*- coding: utf-8; -*-

from django.utils.translation import ugettext_lazy as _

def duplicate_object(modeladmin,request,queryset):
	[obj.clone() for obj in queryset]
	
duplicate_object.short_description=_("Duplicate selected record")

def make_unpublished(modeladmin,request,queryset):
	rows=queryset.update(enable_publish=False)
	if rows == 1:
		msg=_("1 property was")
	else:
		msg=_("%s properties were") %rows 
	modeladmin.message_user(request,_("%s successfully marked unpublished.") %msg)

make_unpublished.short_description=_("Unpublish selected record")

def make_published(modeladmin,request,queryset):
	rows=queryset.update(enable_publish=True)
	if rows == 1:
		msg=_("1 property was")
	else:
		msg=_("%s properties were") % rows
	modeladmin.message_user(request,_("%s successfully marked published.") % msg)
make_published.short_description=_("Publish selected record")
