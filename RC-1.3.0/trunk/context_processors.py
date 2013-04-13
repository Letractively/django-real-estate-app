# -*- conding: utf-8; -*-
from django.contrib.sites.models import Site
from django.conf import settings
from conf.settings import MEDIA_PREFIX,REAL_ESTATE_APP_SITE_NAME, EASY_MAPS_GOOGLE_KEY

def custom_processor(request):
	return {
			'MEDIA_REAL_ESTATE': MEDIA_PREFIX,
			'MEDIA_URL':settings.MEDIA_URL,
			'SITE': Site.objects.get(id=settings.SITE_ID),
			'SITE_TITLE':REAL_ESTATE_APP_SITE_NAME,
			'EASY_MAPS_GOOGLE_KEY': EASY_MAPS_GOOGLE_KEY,
			'REAL_ESTATE_APP_SITE_NAME': REAL_ESTATE_APP_SITE_NAME
	}

