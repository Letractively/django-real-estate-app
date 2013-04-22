from django.conf.urls.defaults import url
from django.contrib.sitemaps import GenericSitemap

from real_estate_app.conf.settings import REAL_ESTATE_APP_NUM_LATEST

from feeds import PropretyFeed
from models import Proprety
 
info_dict = {'template_object_name': 'proprety',}

feeds_property = {'rss': PropretyFeed,}
proprety_info = {'queryset':Proprety.objects.all(),}
sitemap_info = {'proprety':GenericSitemap(proprety_info,priority=0.8),}

proprety_list = url(
    regex  = '^$',
    view   = 'real_estate_app.apps.propretys.views.proprety_list',
    kwargs = dict(info_dict, paginate_by=REAL_ESTATE_APP_NUM_LATEST),
    name   = 'propretry-list'
)

proprety_detail = url(
	regex  = '^(?P<slug>[-\w]+)/$',
	view   = 'real_estate_app.apps.propretys.views.proprety_detail',
	kwargs = dict(info_dict, slug_field='slug'),
	name   = 'proprety-detail'
)

feeds_proprety_url = url(
	regex  = '^rss/$',
	view   = PropretyFeed(),
	name   = 'proprety-feeds'
)

proprety_sitemap = url(
	regex  = '^sitemap\.xml$', 
	view   = 'django.contrib.sitemaps.views.sitemap', 
	kwargs = dict(sitemaps=sitemap_info),
	name   = 'proprety-sitemap'
)
