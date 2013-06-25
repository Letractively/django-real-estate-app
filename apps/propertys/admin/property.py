# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import admin 

from forms import PropertyAdminForm
from real_estate_app.apps.propertys.models import Property
from real_estate_app.apps.photos.admin import PhotoInlineAdmin 

from real_estate_app.admin.actions import duplicate_object, make_unpublished, make_published 
from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.conf.settings import MEDIA_PREFIX as MEDIA_PREFIX_REAL_ESTATE


LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

BRAZIL=[]
if LANGUAGE_CODE=='pt-br':
	BRAZIL=['condominio','iptu']

class PropertyAdmin(RealEstateAppPopUpModelAdmin):
	search_fields = ['address','code_property']
	
	fieldsets = (
			(_('General Information'), {
				'fields': ['address','slug','zip_code','description','price','state','district_fk','classification_fk','statusproperty_fk','realtor_fk']+BRAZIL,
			}),
			(_('Detailed Information'), {
				'fields':('rooms','baths','garage','elevator','private_area','position_of_sun','under_contruction','furnishing','aditionalthings_fk',),
			}),
			(_('Publish'), {
				'fields':('pub_date','pub_date_end','domain','featured',),
			}),
			(_('MAPS'), {
				'fields':('gmap_point_x','gmap_point_y',),
				'classes':('gmap',),
				'description':_('Mark on map the localization. p.s: use the right click to mark place when use zoom.'),
			}),
	)
	
	date_hierarchy = 'pub_date'
	
	list_display = ('code_property','agenda','address','district_fk','statusproperty_fk','pub_date','pub_date_end',)
	
	list_filter = ('classification_fk','statusproperty_fk','enable_publish','logical_exclude',)
	
	prepopulated_fields = {'slug': ('address',)}
	
	form = PropertyAdminForm 

	inlines = (
			PhotoInlineAdmin,
	)
	actions=[duplicate_object,make_unpublished,make_published]

	change_form_template = 'admin/propertys/property/property_change_form.html'

	class Media:
		css = {
			'all':(
					MEDIA_PREFIX_REAL_ESTATE+"admin/css/facebox.css",
					MEDIA_PREFIX_REAL_ESTATE+"admin/css/gmaps.css",
					#MEDIA_PREFIX_REAL_ESTATE+"css/autocomplete.css",
			),
		}
		js = (
			  MEDIA_PREFIX_REAL_ESTATE+"js/meio.mask.min.js",
			  MEDIA_PREFIX_REAL_ESTATE+"admin/js/facebox.js",
			  MEDIA_PREFIX_REAL_ESTATE+"admin/js/real_estate_app_masks.js",
			  MEDIA_PREFIX_REAL_ESTATE+'admin/js/tiny_mce/tiny_mce.js',
		      MEDIA_PREFIX_REAL_ESTATE+'admin/js/tiny_mce/textarea.js',
		      MEDIA_PREFIX_REAL_ESTATE+'admin/js/ajax_csrf.js',
		      'http://maps.google.com/maps/api/js?sensor=false&amp;language=en',
		      MEDIA_PREFIX_REAL_ESTATE+'js/gmap3.js',
		      MEDIA_PREFIX_REAL_ESTATE+'admin/js/real_estate_app_gmaps.js',
		)

admin.site.register(Property, PropertyAdmin)