from django.conf.urls.defaults import url

info_dict = {
    'template_object_name': 'portlet',
}

portlet_create = url(
    regex  = '^portlet/add/$',
    view   = 'real_estate_app.apps.portlets.views.portlet_create',
    kwargs = dict(),
    name   = 'portlet-add'
)


portlet_edit = url(
    regex  = '^portlet/(?P<object_id>\d+)/$',
    view   = 'real_estate_app.apps.portlets.views.portlet_edit',
    kwargs = dict(info_dict),
    name   = 'portlet-edit'
)
