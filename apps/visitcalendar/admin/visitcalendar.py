# -*- coding: utf-8 -*-
from functools import update_wrapper

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.conf.urls.defaults import url, patterns 
from django.contrib import admin 

from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.visitcalendar.forms import VisitEventAdminForm
from real_estate_app.apps.visitcalendar.models import VisitEvent, Visitor 
from real_estate_app.apps.visitcalendar.views import visitcalendar_list_property_visit, visitcalendar_create_object
from real_estate_app.conf.settings import MEDIA_PREFIX as MEDIA_PREFIX_REAL_ESTATE

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class VisitEventCalendarAdmin(RealEstateAppPopUpModelAdmin):
	fieldsets = (
	 		(_('General Information'), {
	 			'fields': ['property_fk','visitor_fk','date_visit',],
	 		}),
	 )

	form = VisitEventAdminForm

	class Media:
		css = {
			'all':(
					MEDIA_PREFIX_REAL_ESTATE+"css/facebox.css",
			),
		}
		js = (
			  MEDIA_PREFIX_REAL_ESTATE+"js/facebox.js",
		)

	def get_urls(self):
		urls = super(VisitEventCalendarAdmin, self).get_urls()

		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)

		custom_urls = patterns('',
				url(
					regex  = '^property/(?P<slug>[-\w]+)/$',
					view   = wrap(visitcalendar_list_property_visit),
					name   = 'admin_visitcalendar_list_property_visit',
					kwargs = dict(template_name='admin/visitcalendar/visitevent/change_list.html',)
				),
		)

		return custom_urls + urls

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
