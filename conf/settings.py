# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db.models import get_app

# Where is the media directory of app real_estate_app
MEDIA_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','media')

# Create a media prefix for real_estate_app media.
MEDIA_PREFIX=getattr(settings,'REAL_APP_MEDIA_PREFIX','/media-real/')

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
REAL_ESTATE_APP_AJAX_SEARCH = getattr(settings,
									  'REAL_ESTATE_APP_AJAX_SEARCH',
									  {'realtor': {
									  				'search_fields':['user__first_name','user__last_name',],
									  				'return_values':['photo','pk','user__first_name','user__last_name',],
									  				'thumbnail_ajax':'40x40'
									  			   },
									  	'visitor': {
									  				'search_fields':['cpf',],
									  				'return_values':['pk','visitor_first_name','visitor_last_name'],
									  				'all_fields':True,
									  	}
									  }
)

# Number of lasted visited property
REAL_ESTATE_VIEWED_PRODUCTS = getattr(settings,'REAL_ESTATE_VIEWED_PRODUCTS',4)

# User for sendmail, this is a email from.
REAL_ESTATE_EMAIL = getattr(settings,'REAL_ESTATE_EMAIL','root@localhost')

# Used as a boundary between two visits of property
REAL_ESTATE_APP_VISIT_EVENT_HOUR = getattr(settings,'REAL_ESTATE_APP_VISIT_EVENT_HOUR',2)

# Get the MANAGERS of site for real_estate_app
MANAGERS = getattr(settings,'MANAGERS')
MANAGERS=list(MANAGERS)