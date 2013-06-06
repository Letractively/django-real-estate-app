from django.conf.urls.defaults import url
 
info_dict = {'template_object_name': 'visitcalendar',}

visitclick_data_json_view = url (
    regex  = '^visitclick/graphs/data/$',
    view   = 'real_estate_app.apps.visitclick.views.visitclick_data_json',
    kwargs = {},
    name   = 'visitclick_data_json_view'
)