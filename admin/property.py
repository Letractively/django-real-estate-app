# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import admin 
from options import FaceBoxModelAdmin

from real_estate_app.admin.forms import PropertyAdminForm
from real_estate_app.admin.photo import PhotoInlineAdmin 
from real_estate_app.admin.actions import duplicate_object, make_unpublished, make_published 
from real_estate_app.conf.settings import MEDIA_PREFIX
from real_estate_app.models import Property

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

BRAZIL=[]
if LANGUAGE_CODE=='pt-br':
	BRAZIL=['condominio','iptu']

class PropertyAdmin(FaceBoxModelAdmin):
	search_fields = ['address','code_property']
	
	fieldsets = (
			(_('General Information'), {
				'fields': ['address','slug','zip_code','description','price','state','district_fk','classification_fk','statusproperty_fk','realtor_fk']+BRAZIL,
			}),
			(_('Detailed Information'),{
				'fields':('rooms','baths','garage','elevator','private_area','position_of_sun','under_contruction','furnishing','aditionalthings_fk',),
			}),
			(_('Publish'),{
				'fields':('date_init','date_end','domain', 'enable_publish','featured',),
			}),
			(_('MAPS'),{
				'fields':('gmap_point_x','gmap_point_y',),
				'classes':('gmap',),
				'description':_('Mark on map the localization. p.s: use the right click to mark place when use zoom.'),
			}),
	)
	
	list_display = ('code_property','address','state','district_fk', 'classification_fk','statusproperty_fk','date_init','date_end',)
	
	list_filter = ('classification_fk','statusproperty_fk','enable_publish')
	
	prepopulated_fields = {'slug': ('address',)}
	
	form = PropertyAdminForm 

	inlines = (
			PhotoInlineAdmin,
	)
	actions=[duplicate_object,make_unpublished,make_published]

	class Media:
		css = {
			'all':(
					MEDIA_PREFIX+"css/facebox.css",
					MEDIA_PREFIX+"css/tabs.css",
					MEDIA_PREFIX+"css/gmaps.css",
					MEDIA_PREFIX+"css/change-list.css",
					MEDIA_PREFIX+"css/autocomplete.css",
			),
		}
		js = (MEDIA_PREFIX+"js/meio.mask.min.js",
			  MEDIA_PREFIX+"js/facebox.js",
			  MEDIA_PREFIX+"js/real_estate_app_masks.js",
			  MEDIA_PREFIX+"js/real_estate_app_gmaps.js",
			  MEDIA_PREFIX+'js/tiny_mce/tiny_mce.js',
		      MEDIA_PREFIX+'js/tiny_mce/textarea.js',
		      MEDIA_PREFIX+'js/ajax_csrf.js',
		      MEDIA_PREFIX+'js/real_estate_app_district.js',
		      MEDIA_PREFIX+'js/jquery.createtabs.js',
		      MEDIA_PREFIX+'js/property-load.js',
			  'http://maps.google.com/maps/api/js?sensor=true',
		)

admin.site.register(Property, PropertyAdmin)
