import json

from django.dispatch import receiver

from real_estate_app.conf import settings
from real_estate_app.apps.propretys.signals import proprety_viewed

MAX_PRODUCTS = settings.REAL_ESTATE_VIEWED_PRODUCTS

# This code is based on django-oscar create by 

def get_recently_viewed_proprety_ids(request):
    """
    Get lasted viewed propretys from cookie REAL_ESTATE_APP_VIEWED_PROPRETY.
    """
    proprety_ids = []
    if (request.COOKIES.has_key('REAL_ESTATE_APP_VIEWED_PROPRETY')):
        try:
            proprety_ids = _get_list_from_json_string(request.COOKIES['REAL_ESTATE_APP_VIEWED_PROPRETY'])
        except ValueError:
            # This can occur if something messes up the cookie
            pass
    return proprety_ids

def _update_recently_viewed_proprety(proprety, request, response):
    """
    Update lasted viewed propretys from cookie REAL_ESTATE_APP_VIEWED_PROPRETY.
    """
    proprety_ids = get_recently_viewed_proprety_ids(request)
    if proprety.id in proprety_ids:
       proprety_ids.remove(proprety.id)
    proprety_ids.append(proprety.id)
    if (len(proprety_ids) > MAX_PRODUCTS):
        proprety_ids = proprety_ids[len(proprety_ids)-MAX_PRODUCTS:]
    response.set_cookie('REAL_ESTATE_APP_VIEWED_PROPRETY',
                        _get_json_string_from_list(proprety_ids),
                        httponly=True)

def _get_list_from_json_string(cookie_value):
    u""" Simple function to convert lists to json """
    return json.loads(cookie_value)

def _get_json_string_from_list(list):
    """ Simple function to convert json to a python list """
    return json.dumps(list)

@receiver(proprety_viewed)
def receive_proprety_view(sender, proprety, user, request, response, **kwargs):
	"""
	Receiver to handle viewing single proprety pages
	Requires the request and response objects due to dependence on cookies
	"""

	return _update_recently_viewed_proprety(proprety, request, response)