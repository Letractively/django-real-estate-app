# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import admin 

from forms import PropretyAdminForm
from real_estate_app.apps.propretys.models import Proprety
from real_estate_app.apps.photos.admin import PhotoInlineAdmin 

from real_estate_app.admin.actions import duplicate_object, make_unpublished, make_published 
from real_estate_app.admin.options import FaceBoxModelAdmin
from real_estate_app.conf.settings import MEDIA_PREFIX as MEDIA_PREFIX_REAL_ESTATE


LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

BRAZIL=[]
if LANGUAGE_CODE=='pt-br':
	BRAZIL=['condominio','iptu']

class PropretyAdmin(FaceBoxModelAdmin):
	search_fields = ['address','code_property']
	
	fieldsets = (
			(_('General Information'), {
				'fields': ['address','slug','zip_code','description','price','state','district_fk','classification_fk','statusproprety_fk','realtor_fk']+BRAZIL,
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

	date_hierarchy = 'date_init'
	
	list_display = ('code_property','address','state','district_fk', 'classification_fk','statusproprety_fk','date_init','date_end',)
	
	list_filter = ('classification_fk','statusproprety_fk','enable_publish')
	
	prepopulated_fields = {'slug': ('address',)}
	
	form = PropretyAdminForm 

	inlines = (
			PhotoInlineAdmin,
	)
	actions=[duplicate_object,make_unpublished,make_published]

	class Media:
		css = {
			'all':(
					MEDIA_PREFIX_REAL_ESTATE+"css/facebox.css",
					MEDIA_PREFIX_REAL_ESTATE+"css/tabs.css",
					MEDIA_PREFIX_REAL_ESTATE+"css/gmaps.css",
					MEDIA_PREFIX_REAL_ESTATE+"css/change-list.css",
					MEDIA_PREFIX_REAL_ESTATE+"css/autocomplete.css",
			),
		}
		js = (MEDIA_PREFIX_REAL_ESTATE+"js/meio.mask.min.js",
			  MEDIA_PREFIX_REAL_ESTATE+"js/facebox.js",
			  MEDIA_PREFIX_REAL_ESTATE+"js/real_estate_app_masks.js",
			  MEDIA_PREFIX_REAL_ESTATE+'js/tiny_mce/tiny_mce.js',
		      MEDIA_PREFIX_REAL_ESTATE+'js/tiny_mce/textarea.js',
		      MEDIA_PREFIX_REAL_ESTATE+'js/ajax_csrf.js',
		      MEDIA_PREFIX_REAL_ESTATE+'js/real_estate_app_district.js',
		      MEDIA_PREFIX_REAL_ESTATE+'js/jquery.createtabs.js',
		)

admin.site.register(Proprety, PropretyAdmin)
