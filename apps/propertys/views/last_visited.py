import json

from django.dispatch import receiver

from real_estate_app.conf import settings
from real_estate_app.apps.propertys.signals import property_viewed

MAX_PRODUCTS = settings.REAL_ESTATE_VIEWED_PRODUCTS

# This code is based on django-oscar create by 

def get_recently_viewed_property_ids(request):
    """
    Get lasted viewed propertys from cookie REAL_ESTATE_APP_VIEWED_PROPRETY.
    """
    property_ids = []
    if (request.COOKIES.has_key('REAL_ESTATE_APP_VIEWED_PROPRETY')):
        try:
            property_ids = _get_list_from_json_string(request.COOKIES['REAL_ESTATE_APP_VIEWED_PROPRETY'])
        except ValueError:
            # This can occur if something messes up the cookie
            pass
    return property_ids

def _update_recently_viewed_property(property, request, response):
    """
    Update lasted viewed propertys from cookie REAL_ESTATE_APP_VIEWED_PROPRETY.
    """
    property_ids = get_recently_viewed_property_ids(request)
    if property.id in property_ids:
       property_ids.remove(property.id)
    property_ids.append(property.id)
    if (len(property_ids) > MAX_PRODUCTS):
        property_ids = property_ids[len(property_ids)-MAX_PRODUCTS:]
    response.set_cookie('REAL_ESTATE_APP_VIEWED_PROPRETY',
                        _get_json_string_from_list(property_ids),
                        httponly=True)

def _get_list_from_json_string(cookie_value):
    u""" Simple function to convert lists to json """
    return json.loads(cookie_value)

def _get_json_string_from_list(list):
    """ Simple function to convert json to a python list """
    return json.dumps(list)

@receiver(property_viewed)
def receive_property_view(sender, property, user, request, response, **kwargs):
	"""
	Receiver to handle viewing single property pages
	Requires the request and response objects due to dependence on cookies
	"""

	return _update_recently_viewed_property(property, request, response)