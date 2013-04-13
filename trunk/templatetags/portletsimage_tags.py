# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from real_estate_app.models import PortletPropagandaImage

register = template.Library()


class PortletImagemNode(template.Node):
	def __init__(self, var_name ,num=None):
		self.var_name=var_name

		if num:
			self.num = int(num)
		else:
			self.num = None

	def render(self, context):
		portlets = PortletPropagandaImage.objects.all().order_by('?')
		context[self.var_name] = portlets[:self.num]
		return ''


def do_get_portlet_image(parser, token):

	bits = token.contents.split()

	if len(bits) == 4:
		if bits[2] != 'as':
			raise template.TemplateSyntaxError, " Second argument to '%s' tag must be 'as'" % bits[0]
		return PortletImagemNode(num=bits[1], var_name=bits[3])

	elif len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return PortletImagemNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])
register.tag('get_portlet_image',do_get_portlet_image)
