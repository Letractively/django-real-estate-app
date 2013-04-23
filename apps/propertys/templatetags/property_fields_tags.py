# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.safestring import mark_safe

from real_estate_app.apps.propertys.models import District, StatusProperty, Classification, AditionalThings


register = template.Library()

class SelectLocationFormNode(template.Node):
	def __init__(self, var_name):
		self.var_name=var_name

	def render(self, context):
		options = District.objects.get_selected()

		context[self.var_name] = options
		return ''

def do_get_options_select_district(parser, token):
	bits = token.contents.split()
	
	if len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
		return SelectLocationFormNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one arguments: %s as [varname]" %(bits[0],bits[0])

class SelectStatusFormNode(template.Node):
	def __init__(self, var_name):
		self.var_name=var_name

	def render(self, context):
		options = StatusProperty.objects.all().exclude(logical_exclude=True)

		context[self.var_name] = options
		return ''

def do_get_options_select_statusproperty(parser, token):
	bits = token.contents.split()
	
	if len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
		return SelectStatusFormNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one arguments: %s as [varname]" %(bits[0],bits[0])

class SelectClassificationFormNode(template.Node):
	def __init__(self, var_name):
		self.var_name=var_name

	def render(self, context):
		options = Classification.objects.all().exclude(logical_exclude=True)

		context[self.var_name] = options
		return ''

def do_get_options_select_classification_property(parser, token):
	bits = token.contents.split()
	
	if len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
		return SelectClassificationFormNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one arguments: %s as [varname]" %(bits[0],bits[0])

class CheckedAditionalThingsFormNode(template.Node):
	def __init__(self, var_name):
		self.var_name=var_name

	def render(self, context):
		options = AditionalThings.objects.all().exclude(logical_exclude=True)

		context[self.var_name] = options
		return ''

def do_get_options_checked_aditonal_things_property(parser, token):
	bits = token.contents.split()
	
	if len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
		return CheckedAditionalThingsFormNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one arguments: %s as [varname]" %(bits[0],bits[0])



register.tag('get_select_district',do_get_options_select_district)
register.tag('get_select_statusproperty',do_get_options_select_statusproperty)
register.tag('get_select_classification_property',do_get_options_select_classification_property)
register.tag('get_checked_aditional_things_property',do_get_options_checked_aditonal_things_property)