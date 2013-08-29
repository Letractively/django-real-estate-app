from django.conf.urls.defaults import url
from real_estate_app.conf import settings as real_estate_app_conf

debug_media_real = url(
	regex  = real_estate_app_conf.MEDIA_REGEX,
	view   = 'django.views.static.serve',
	kwargs = {'document_root': real_estate_app_conf.MEDIA_PATH, 'show_indexes':True},
	name   = 'debug-media-real'
)
