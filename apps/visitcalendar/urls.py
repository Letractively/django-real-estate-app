from django.conf.urls.defaults import url
 
info_dict = {'template_object_name': 'visitcalendar',}

visitcalendar_list = url(
    regex  = '^calendar/$',
    view   = 'real_estate_app.apps.visitcalendar.views.visitcalendar_list',
    kwargs = dict(info_dict),
    name   = 'visitcalendar-list'
)

visitcalendar_list_proprety_visit = url(
	regex  = '^calendar/(?P<slug>[-\w]+)/$',
	view   = 'real_estate_app.apps.visitcalendar.views.visitcalendar_list_proprety_visit',
	kwargs = dict(info_dict),
	name   = 'visitcalendar-detail'
)

visitcalendar_list_json = url(
	regex  = '^calendar/json(/(?P<slug>[-\w]+)/|/)$',
    view   = 'real_estate_app.apps.visitcalendar.views.visitcalendar_list_json',
    kwargs = dict(info_dict),
    name   = 'visitcalendar-list-json'
)

visitcalendar_create_object = url (
    regex  = '^calendar/(?P<slug>[-\w]+)/add/$',
    view   = 'real_estate_app.apps.visitcalendar.views.visitcalendar_create_object',
    kwargs = dict(post_save_redirect='../'),
    name   = 'visitcalendar-create-object'
)

visitcalendar_update_object = url (
    regex  = '^calendar/(?P<proprety_slug>[-\w]+)/(?P<slug>[-\w]+)/edit/$',
    view   = 'real_estate_app.apps.visitcalendar.views.visitcalendar_update_object',
    kwargs = dict(slug_field='slug', post_save_redirect='../../'),
    name   = 'visitcalendar-create-object'
)