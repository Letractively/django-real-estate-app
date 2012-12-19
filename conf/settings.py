# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app


MEDIA_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','media')

MEDIA_PREFIX=getattr(settings,'REAL_APP_MEDIA_PREFIX','/media-real/')

MEDIA_REGEX = r'^%s(?P<path>.*)$' % MEDIA_PREFIX.lstrip('/')

REAL_ESTATE_APP_NUM_LATEST = getattr(settings,'PROPERTY_NUM_LATEST',25)

REAL_ESTATE_IMAGES_SIZE=getattr(settings,'REAL_ESTATE_IMAGES_SIZE',(626,286))

REAL_ESTATE_APP_SITE_NAME=getattr(settings,'REAL_ESTATE_SITE_NAME','')

EASY_MAPS_GOOGLE_KEY=getattr(settings,'EASY_MAPS_GOOGLE_KEY','')

MANAGERS = getattr(settings,'MANAGERS')

REAL_ESTATE_APP_AJAX_SEARCH = getattr(settings,
									  'REAL_ESTATE_APP_AJAX_SEARCH',
									  {'realtor': {
									  				'search_fields':['user__first_name','user__last_name',],
									  				'return_values':['photo','pk','user__first_name','user__last_name',],
									  				'thumbnail_ajax':'40x40'
									  			   },
									  }
)


MANAGERS=list(MANAGERS)

MIN_WIDTH=REAL_ESTATE_IMAGES_SIZE[0]
MIN_HEIGHT=REAL_ESTATE_IMAGES_SIZE[1]

try:
	import sorl.thumbnail
except ImportError:
	raise ImproperlyConfigured("You need install sorl-thumbnail app")