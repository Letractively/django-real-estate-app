from django.views.generic.list_detail import object_detail
from real_estate_app.models import Photo

def photo_detail(request, album=None, *args, **kwargs):
    return object_detail(request, *args, **kwargs)


