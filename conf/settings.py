# -*- coding: utf-8 -*-
import os
from sys import getfilesystemencoding, platform

from django.conf import settings
from django.db.models import get_app
from django.utils.translation import ugettext as _

# Where is the media directory of app real_estate_app
TMP_REAL_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','media')
if platform.startswith('win'):
	TMP_REAL_PATH=unicode(TMP_REAL_PATH,getfilesystemencoding())

MEDIA_PATH=getattr(
	settings,
	'REAL_APP_MEDIA_PATH',
	TMP_REAL_PATH
)

# Create a media prefix for real_estate_app media.
MEDIA_REAL_ESTATE = MEDIA_PREFIX=getattr(settings,'REAL_APP_MEDIA_PREFIX','/media-real/')

# This is used for debug only.
MEDIA_REGEX = r'^%s(?P<path>.*)$' % MEDIA_PREFIX.lstrip('/')

#Number for paginate.
REAL_ESTATE_APP_NUM_LATEST = getattr(settings,'PROPERTY_NUM_LATEST',25)

# Min. size of photos.
REAL_ESTATE_IMAGES_SIZE=getattr(settings,'REAL_ESTATE_IMAGES_SIZE',(626,286))
MIN_WIDTH=REAL_ESTATE_IMAGES_SIZE[0]
MIN_HEIGHT=REAL_ESTATE_IMAGES_SIZE[1]

# Site name for custom admin.
REAL_ESTATE_APP_SITE_NAME=getattr(settings,'REAL_ESTATE_SITE_NAME','')

# Used for google maps
EASY_MAPS_GOOGLE_KEY=getattr(settings,'EASY_MAPS_GOOGLE_KEY','')

# This is used for autocomplete widgets.
CUSTOM_AJAX_SEARCH = getattr(settings,'REAL_ESTATE_APP_AJAX_SEARCH',False)
REAL_ESTATE_APP_AJAX_SEARCH={
							'realtor': {
									  		'search_fields':['user__first_name','user__last_name',],
									  		'return_values':['photo','pk','user__first_name','user__last_name',],
									  		'thumbnail_ajax':'40x40',
									  		'label':['first_name','last_name']
							},
							'visitor': {
									  		'search_fields':['email',],
									  		'return_values':['pk','first_name','last_name'],
									  		'all_fields':True,
									  		'thumbnail_ajax':'40x40',
									  		'label':['first_name','last_name']
							},
							'property': {
										'search_fields':['address',],
										'return_values':['pk','address'],
										'thumbnail_ajax':'40x40',
										'label':['address',]
							},
							'district':{
										'search_fields':['district',],
										'return_values':['pk','district'],
										'thumbnail_ajax':'40x40',
										'label':['district',]
							},
							'classification': {
										'search_fields':['classification',],
										'return_values':['pk','classification'],
										'thumbnail_ajax':'40x40',
										'label':['classification',]
							},
							'statusproperty':{
										'search_fields':['statusproperty',],
										'return_values':['pk','statusproperty'],
										'thumbnail_ajax':'40x40',
										'label':['statusproperty',]
							},
							'aditionalthings': {
										'search_fields':['name',],
										'return_values':['pk','name'],
										'thumbnail_ajax':'40x40',
										'label':['name',]
							},
							'positionofsun':{ 
										'search_fields':['position',],
										'return_values':['pk','position'],
										'thumbnail_ajax':'40x40',
										'label':['position',]
							},
							'site':{ 
										'search_fields':['site',],
										'return_values':['pk','site'],
										'thumbnail_ajax':'40x40',
										'label':['site',]
							},
							'files':{ 
										'search_fields':['files',],
										'return_values':['pk','site'],
										'thumbnail_ajax':'40x40',
										'label':['files',]
							},
							'group':{
										'search_fields':['name',],
										'return_values':['pk','name'],
										'thumbnail_ajax':'40x40',
										'label':['name',]
							},
							'permission':{
										'search_fields':['name',],
										'return_values':['pk','name'],
										'thumbnail_ajax':'40x40',
										'label':['name',]
							},
}

if CUSTOM_AJAX_SEARCH:
	REAL_ESTATE_APP_AJAX_SEARCH.update(CUSTOM_AJAX_SEARCH)

# Number of lasted visited property
REAL_ESTATE_VIEWED_PRODUCTS = getattr(settings,'REAL_ESTATE_VIEWED_PRODUCTS',4)

# User for sendmail, this is a email from.
REAL_ESTATE_EMAIL = getattr(settings,'REAL_ESTATE_EMAIL','root@localhost')

# Used as a boundary between two visits of property
REAL_ESTATE_APP_VISIT_EVENT_HOUR = getattr(settings,'REAL_ESTATE_APP_VISIT_EVENT_HOUR',2)

# Used for create a menu apps in amdin site
REAL_ESTATE_APP_MENU = {
	'propertys':['property',],
	'portlets':['portlet',],
	'newspapers':['news',],
	'marketing':['marketingobject',],
	'realtors':['realtor',],
	'visitcalendar':['visitevent',]
}
CUSTOM_REAL_ESTATE_APP_MENU = getattr(settings,'REAL_ESTATE_APP_MENU', False)
if CUSTOM_REAL_ESTATE_APP_MENU:
	REAL_ESTATE_APP_MENU.update(CUSTOM_REAL_ESTATE_APP_MENU)

# Used for create a menu settings in admin site.
REAL_ESTATE_APP_SETTINGS = {
	'auth':['user','group'],
	'sites':['site',],
	'visitcalendar':['termvisit',],
}
CUSTOM_REAL_ESTATE_APP_SETTINGS = getattr(settings,'REAL_ESTATE_APP_SETTINGS', False)
if CUSTOM_REAL_ESTATE_APP_SETTINGS:
	REAL_ESTATE_APP_MENU.update(CUSTOM_REAL_ESTATE_APP_SETTINGS)

# Get the MANAGERS of site for real_estate_app
MANAGERS = getattr(settings,'MANAGERS')
MANAGERS=list(MANAGERS)

REAL_ESTATE_PROPERTY_UNKNOW_IMG=getattr(settings,'REAL_ESTATE_PROPERTY_UNKNOW_IMG', '' )
REAL_ESTATE_REALTOR_UNKNOW_IMG=getattr(settings,'REAL_ESTATE_REALTOR_UNKNOW_IMG', '' )
