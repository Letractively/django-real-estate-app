# -*- coding: utf-8 -*-

from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import list_detail
from real_estate_app.apps.newspapers.models import News

@requires_csrf_token
def news_list(request, *args, **kwargs):
	"""
	A view wrapper around ``django.views.generic.list_detail.object_list``.
	"""
	kwargs['queryset'] = News.objects.all()
	return list_detail.object_list(request, *args, **kwargs)


def news_detail(request, *args, **kwargs):
	"""
	A view wrapper around ``django.views.generic.list_detail.object_detail``.
	"""
	kwargs['queryset'] = News.objects.all()
	return list_detail.object_detail(request, *args, **kwargs)