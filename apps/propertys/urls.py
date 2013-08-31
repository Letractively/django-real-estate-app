from django.conf.urls.defaults import url
from django.contrib.sitemaps import GenericSitemap

from real_estate_app.conf.settings import REAL_ESTATE_APP_NUM_LATEST

from feeds import PropertyFeed
from models import Property
 
info_dict = {'template_object_name': 'property',}

feeds_property = {'rss': PropertyFeed,}
property_info = {'queryset':Property.objects.all_enabled(),}
sitemap_info = {'property':GenericSitemap(property_info,priority=0.8),}

property_list = url(
    regex  = '^$',
    view   = 'real_estate_app.apps.propertys.views.property_list',
    kwargs = dict(info_dict, paginate_by=REAL_ESTATE_APP_NUM_LATEST),
    name   = 'propretry-list'
)

property_detail = url(
	regex  = '^(?P<slug>[-\w]+)/$',
	view   = 'real_estate_app.apps.propertys.views.property_detail',
	kwargs = dict(info_dict, slug_field='slug'),
	name   = 'property-detail'
)

feeds_property_url = url(
	regex  = '^rss/$',
	view   = PropertyFeed(),
	name   = 'property-feeds'
)

property_sitemap = url(
	regex  = '^sitemap\.xml$', 
	view   = 'django.contrib.sitemaps.views.sitemap', 
	kwargs = dict(sitemaps=sitemap_info),
	name   = 'property-sitemap'
)
