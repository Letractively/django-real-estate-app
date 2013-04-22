from django.conf.urls.defaults import url
from real_estate_app.apps.photos.models import Photo

photo_info_dict = {
    'queryset': Photo.objects.all(),
    'template_object_name': 'photo',
}

photo_detail = url(
    regex  = '^(?P<album>[-\w]+)/(?P<slug>[-\w]+)/$',
    view   = 'real_estate_app.apps.photos.views.photo_detail',
    kwargs = dict(photo_info_dict, slug_field='slug'),
    name   = 'apps-photos'
)