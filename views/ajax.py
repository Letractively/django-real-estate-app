import operator

from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.core.files.images import ImageFile
from django.core.files.base import File
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import get_model, Q
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe


from real_estate_app.conf.settings import REAL_ESTATE_APP_AJAX_SEARCH, MEDIA_PREFIX
from real_estate_app.utils import AutoCompleteObject

@csrf_exempt
@login_required 
def ajax_view_model(request, app_label, model_name):
	"""
	Ajax interation to construct the select options
	used a custom serialize how get some expecific fields.
	"""
	q_value=''
	model = get_model(app_label, model_name)
	queryset = model.objects.all()
	module_name=model._meta.module_name
	fields = [i.name for i in model._meta.fields]

	if request.POST:
		if request.POST.items():
			for query in request.POST.items():
				if 'csrfmiddlewaretoken' not in query:
					query=dict((query,))
					queryset=queryset.filter(**query)
	else:
		if 'term' in request.GET:
			q_value=request.GET['term']
			return HttpResponse(
								simplejson.dumps(
									AutoCompleteObject(model).render(value=q_value)
								)
								,mimetype="text/javascript")
		else:
			fields = (fields[1],)

	json = serializers.serialize("json", queryset,fields=fields)
	return HttpResponse(json, mimetype="text/javascript")
