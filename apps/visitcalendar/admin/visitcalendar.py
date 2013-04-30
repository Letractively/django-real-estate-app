# -*- coding: utf-8 -*-
from functools import update_wrapper

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.conf.urls.defaults import url, patterns 
from django.contrib import admin 

from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.visitcalendar.models import VisitEvent, Visitor 
from real_estate_app.apps.visitcalendar.views import visitcalendar_list
from real_estate_app.conf.settings import MEDIA_PREFIX as MEDIA_PREFIX_REAL_ESTATE


LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

BRAZIL=[]
if LANGUAGE_CODE=='pt-br':
	BRAZIL=['condominio','iptu']

class VisitEventCalendarAdmin(RealEstateAppPopUpModelAdmin):
	fieldsets = (
			(_('General Information'), {
				'fields': ['property_fk','visitor_fk','date_visit',],
			}),
	)

	class Media:
		css = {
			'all':(
					MEDIA_PREFIX_REAL_ESTATE+"css/facebox.css",
			),
		}
		js = (
			  MEDIA_PREFIX_REAL_ESTATE+"js/facebox.js",
		)

class VisitorAdmin(RealEstateAppPopUpModelAdmin):
	search_fields = ['visitor_first_name','visitor_last_name','visitor_email']
	list_display = ('visitor_first_name','visitor_last_name','visitor_email',)
	#list_filter = ('classification_fk','statusproperty_fk','enable_publish')
	
	class Media:
		css = {
			'all':(
					MEDIA_PREFIX_REAL_ESTATE+"css/facebox.css",
			),
		}
		js = (
			  MEDIA_PREFIX_REAL_ESTATE+"js/facebox.js",
		)
	
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(VisitEvent, VisitEventCalendarAdmin)
