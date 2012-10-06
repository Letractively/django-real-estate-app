from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import get_model
from django.http import HttpResponse, Http404
from django.core import serializers

@csrf_exempt
@login_required 
def ajax_view_model(request, app_label, model_name):
	"""
	Ajax interation to construct the select options
	"""
	model = get_model(app_label, model_name)
	queryset = model.objects.all()
	fields = [i.name for i in model._meta.fields]
	if request.POST:
		if request.POST.items():
			for query in request.POST.items():
				if 'csrfmiddlewaretoken' not in query:
					query=dict((query,))
					queryset=queryset.filter(**query)
	else:
		fields = (fields[1],)

	json = serializers.serialize("json", queryset,fields=fields)
	return HttpResponse(json, mimetype="text/javascript")
