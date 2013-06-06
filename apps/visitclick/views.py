# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date, time
from qsstats import QuerySetStats

from django.db.models import Q, Count
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import requires_csrf_token

from real_estate_app.utils import radomstring
from real_estate_app.apps.visitclick.models import Click
from real_estate_app.apps.visitclick.utils import get_first_dow

@requires_csrf_token
def visitclick_data_json(request, *args, **kwargs):
	"""
		For default this function return a data list of week
	"""

	google_format = {'rows':[],'cols':[
			{'label':_('Time'),'type':'string','pattern':''},
			{'label':_('Click'),'type':'number','pattern':''},
	]}
	date_init = datetime.now().date()
	date_end = datetime.now()
	strftime='%H:%M'
	field='date'
	display='hours'

	if 'week' in request.GET.values() or 'week' in request.POST.values():
		date_init = get_first_dow(datetime.now().year, datetime.now().isocalendar()[1])
		date_end  = date_init+timedelta(days=7)
		strftime='%d/%m'
		display='days'

	elif 'month' in request.GET.values() or 'month' in request.POST.values():
		date_init = date(date_end.year,date_end.month,1)
		strftime='%d/%m'
		display='days'

	elif 'year' in request.GET.values() or 'year' in request.POST.values():
		date_init = datetime.now() - timedelta(days=365)
		strftime='%m/%Y'
		display='months'

	elif 'custom' in request.GET.values() or 'custom' in request.POST.values():
		date_init = datetime.strptime(request.POST.get('date_init',False) or request.GET.get('date_init'),'%Y-%m-%d')
		date_end = datetime.strptime(request.POST.get('date_end',False) or request.GET.get('date_end'),'%Y-%m-%d')
		strftime='%d/%m'
		display='days'
	
	clicks = Click.objects.filter(
			Q(date__gte=date_init),
			Q(date__lte=date_end)
	)

	if not ('clicks' in request.GET.values() or 'clicks' in request.POST.values()):
		clicks = QuerySetStats(clicks, field).time_series(date_init,date_end, display,aggregate=Count(field))
	else:
		field='url'
		clicks= clicks.values(field).order_by(field).annotate(count=Count(field))
		google_format['cols']=[
			{'label':_('Url'),'type':'string','pattern':''},
			{'label':_('Click'),'type':'number','pattern':''},
		]
		

	if field == 'date':
		google_format['cols']=[
			{'label':_('Date'),'type':'string','pattern':''},
			{'label':_('Click'),'type':'number','pattern':''},
		]
	

	for click in clicks:
		if type(click) is tuple:
			value_line=click[0]
			label_line=click[0]
			value_column=str(click[1])
			label_column=click[1]
		if type(click) is dict:
			value_line, value_column = click.values()
			label_line, label_column = click.values()

		if isinstance(value_line,datetime):
			value_line=value_line.strftime(strftime)

		google_format['rows'].append({
			'c':[
					{'v':label_line,'f':value_line},
					{'v':label_column,'f':value_column}
				]
		})

	return HttpResponse(
						simplejson.dumps(google_format,cls=DjangoJSONEncoder),
						mimetype='application/json'
	)