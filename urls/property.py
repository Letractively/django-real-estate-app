from django.conf.urls.defaults import url
from real_estate_app.conf.settings import REAL_ESTATE_APP_NUM_LATEST
from real_estate_app.feeds import PropertyFeed 

info_dict = {
    'template_object_name': 'property',
}

feeds_property = {
	'rss': PropertyFeed,
}

property_list = url(
    regex  = '^$',
    view   = 'real_estate_app.views.property.property_list',
    kwargs = dict(info_dict, paginate_by=REAL_ESTATE_APP_NUM_LATEST),
    name   = 'propertry-list'
)


property_detail = url(
	regex  = '^(?P<slug>[-\w]+)/$',
	view   = 'real_estate_app.views.property.property_detail',
	kwargs = dict(info_dict, slug_field='slug'),
	name   = 'property-detail'
)
