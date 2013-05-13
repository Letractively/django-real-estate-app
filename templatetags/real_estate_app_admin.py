# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django import template
from django.conf import settings
from django.db.models import Q
from real_estate_app.models import Photo, Property, District, StatusProperty

register = template.Library()

class PropertyWillExpiredNode(template.Node):
	def __init__(self, var_name, num=None):
		self.var_name= var_name

		if num:
			self.num = int(num)
		else:
			self.num = None

	def render(self,context):
		last_days = datetime.now()+timedelta(days=5)
		propertys = Property.objects.all_enabled().filter(Q(date_end__lte=last_days))
		context[self.var_name] = propertys[:self.num]
		return ''

def do_get_property_expired(parser,token):
	bits = token.contents.split()

	if len(bits) == 4:
		if bits[2] != 'as':
			raise template.TemplateSyntaxError, " Second argument to '%s' tag must be 'as'" % bits[0]
		return PropertyWillExpiredNode(num=bits[1], var_name=bits[3])

	elif len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return PropertyWillExpiredNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])

register.tag('get_property_will_expired',do_get_property_expired)
