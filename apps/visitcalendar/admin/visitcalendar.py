# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import admin 

from real_estate_app.apps.visitcalendar.models import VisitEvent

from real_estate_app.conf.settings import MEDIA_PREFIX as MEDIA_PREFIX_REAL_ESTATE


LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

BRAZIL=[]
if LANGUAGE_CODE=='pt-br':
	BRAZIL=['condominio','iptu']

class VisitEventCalendarAdmin(admin.ModelAdmin):
	#search_fields = ['visitor_first_name','visitor_last_name','visitor_email']
	
	date_hierarchy = 'date_visit'
	
	#list_display = ('code_property','address','state','district_fk', 'classification_fk','statusproprety_fk','date_init','date_end',)
	
	#list_filter = ('classification_fk','statusproprety_fk','enable_publish')
	
	#prepopulated_fields = {'slug': ('visitor_first_name','visitor_last_name','date_visit')}
	

admin.site.register(VisitEvent, VisitEventCalendarAdmin)
