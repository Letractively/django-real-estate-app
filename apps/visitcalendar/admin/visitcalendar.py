# -*- coding: utf-8 -*-
from functools import update_wrapper

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.conf.urls.defaults import url, patterns 
from django.contrib import admin 
from django.views.generic.simple import direct_to_template

from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.visitcalendar.admin.forms import VisitEventAdminForm, TermVisitAdminForm, VisitorAdminForm
from real_estate_app.apps.visitcalendar.models import VisitEvent, Visitor, TermVisit
from real_estate_app.apps.visitcalendar.views import visitcalendar_list_property_visit, visitcalendar_create_object
from real_estate_app.apps.visitcalendar.localflavor.br.forms import fieldsets_visitor_form
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
					MEDIA_PREFIX_REAL_ESTATE+"admin/css/facebox.css",
			),
		}
		js = (
			  MEDIA_PREFIX_REAL_ESTATE+"admin/js/facebox.js",
		)
	def changelist_view_day(self,*args,**kwargs):
		d_date=kwargs.pop('d_date',False)
		kwargs['extra_context']={ 'd_date':d_date }
		return super(VisitEventCalendarAdmin,self).changelist_view(*args,**kwargs)

	def get_urls(self):
		urls = super(VisitEventCalendarAdmin, self).get_urls()

		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)

		info = self.model._meta.app_label, self.model._meta.module_name

		custom_urls = patterns('',
				url(
					regex  = '^property/(?P<slug>[-\w]+)/$',
					view   = wrap(visitcalendar_list_property_visit),
					name   = 'admin_visitcalendar_list_property_visit',
					kwargs = dict(template_name='admin/visitcalendar/visitevent/change_list.html',)
				),
				url(
					regex  = '^(?P<object_id>\d+)/term/$',
					view   = wrap(direct_to_template),
					name   = 'admin_term_view',
					kwargs = dict(template='admin/visitcalendar/termvisit/termvisit_view.html')
				),
				url(
					regex  = '^day/$',
					view   = wrap(self.changelist_view_day),
					name   = '%s_%s_changelist_day' % info,
				),
				url(
					regex  = '^day/(?P<d_date>[-\w]+)/$',
					view   = wrap(self.changelist_view_day),
					name   = '%s_%s_changelist_day' % info,
				)
		)

		return custom_urls + urls

class VisitorAdmin(RealEstateAppPopUpModelAdmin):
	search_fields = ['first_name','last_name','email']
	list_display = ('first_name','last_name','email',)

	form = VisitorAdminForm
	general_information = ['first_name','last_name','email','celphone',]

	if LANGUAGE_CODE in ('pt-br','pt_BR'):
		general_information += fieldsets_visitor_form['general-information']

	fieldsets = (
		 	(_('General Information'), {
	 	 		'fields': general_information,
	 		}),
	 		(_('Home address'),{
	 			'fields': ['address','zip','phone',]
	 		}),
	 		(_('Work address'),{
	 			'fields': ['work_address', 'work_zip', 'work_phone',]
	 		})
	)
	
	class Media:
		css = {
			'all':(
					MEDIA_PREFIX_REAL_ESTATE+"css/facebox.css",
			),
		}
		js = (
			  MEDIA_PREFIX_REAL_ESTATE+"js/facebox.js",
			  MEDIA_PREFIX_REAL_ESTATE+"js/meio.mask.min.js",
			  MEDIA_PREFIX_REAL_ESTATE+"admin/js/real_estate_app_masks.js"
		)

class TermVisitAdmin(RealEstateAppPopUpModelAdmin):
	fieldsets = (
	 		(_('General Information'), {
	 			'fields': ['title','slug','text',],
	 		}),
	 )
	prepopulated_fields = {'slug': ('title',)}
	
	form = TermVisitAdminForm

	class Media:
		js = (
			  MEDIA_PREFIX_REAL_ESTATE+'admin/js/tiny_mce/tinymce.min.js',
		      MEDIA_PREFIX_REAL_ESTATE+'admin/js/tiny_mce/textarea.js',
		)

admin.site.register(Visitor, VisitorAdmin)
admin.site.register(VisitEvent, VisitEventCalendarAdmin)
admin.site.register(TermVisit, TermVisitAdmin)
