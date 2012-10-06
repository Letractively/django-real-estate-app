# -*- coding: utf-8 -*-
import os

from django.conf import settings

MEDIA_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','media')

MEDIA_PREFIX=getattr(settings,'REAL_APP_MEDIA_PREFIX','/media-real/')

MEDIA_REGEX = r'^%s(?P<path>.*)$' % MEDIA_PREFIX.lstrip('/')

REAL_ESTATE_APP_NUM_LATEST = getattr(settings,'PROPERTY_NUM_LATEST',25)

REAL_ESTATE_IMAGES_SIZE=getattr(settings,'REAL_ESTATE_IMAGES_SIZE',(626,286))

REAL_ESTATE_APP_SITE_NAME=getattr(settings,'REAL_ESTATE_SITE_NAME','')

MANAGERS = getattr(settings,'MANAGERS')

MANAGERS=list(MANAGERS)

MIN_WIDTH=REAL_ESTATE_IMAGES_SIZE[0]
MIN_HEIGHT=REAL_ESTATE_IMAGES_SIZE[1]


