# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.safestring import mark_safe

from real_estate_app.apps.propertys.models import Property
from real_estate_app.apps.propertys.views.last_visited import get_recently_viewed_property_ids

register = template.Library()


class LastedViewedProperty(template.Node):
	def __init__(self, var_name):
		self.var_name=var_name

	def render(self, context):
		request=context['request']
		property_ids = get_recently_viewed_property_ids(request)
		propertys = Property.objects.filter(id__in=property_ids)
		context[self.var_name] = propertys
		return ''

def do_get_last_visited_property(parser, token):
	
	bits = token.contents.split()

	if len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return LastedViewedProperty(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname]" % (bits[0],bits[0])

register.tag('get_last_visited_property',do_get_last_visited_property)