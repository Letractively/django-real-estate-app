# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.safestring import mark_safe

from real_estate_app.apps.portlets.models import Portlet
from real_estate_app.apps.newspapers.models import  News
from real_estate_app.apps.propertys.models import Property, District, StatusProperty, Classification, AditionalThings
from real_estate_app.apps.photos.models import Photo


register = template.Library()

class RealEstateNode(template.Node):
	def __init__(self,*args, **kwargs):
		self.real_estate_node_template="admin/real_estate_app/real_estate_node_list.html"
        

class PropertyAlbumNode(template.Node):
	def __init__(self, var_name, obj_id=None ,num=None):
		self.var_name=var_name
		self.id = obj_id

		if num:
			self.num = int(num)
		else:
			self.num = None


	def render(self, context):
		if self.id:
			obj = template.resolve_variable(self.id, context)

		if self.id:
			photo = Photo.objects.filter(album_property=int(obj))
			
		else:
			photo = Photo.objects.all()

		context[self.var_name] = photo[:self.num]
		return ''

def do_get_property_photo(parser, token):

	bits = token.contents.split()
	if len(bits) == 5:
		if bits[3] != 'as':
			raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
		return PropertyAlbumNode(obj_id=bits[1],num=bits[2], var_name=bits[4])
	if len(bits) == 6:
		if bits[2] != 'from':
			raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'from'" % bits[0]
		if bits[4] != 'as':
			raise template.TemplateSyntaxError, "Fourth argument to '%s' tag must be 'as'" % bits[0]
		return PropertyAlbumNode(num=bits[1], var_name=bits[5], obj_id=bits[3])

	elif len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return PropertyAlbumNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])

class PropertyRandomNode(template.Node):
	def __init__(self, var_name ,num=None):
		self.var_name=var_name

		if num:
			self.num = int(num)
		else:
			self.num = None

	def render(self, context):
		propertys = Property.objects.all_enabled().exclude(featured=True).order_by('?')

		context[self.var_name] = propertys[:self.num]
		return ''


def do_get_property(parser, token):

	bits = token.contents.split()

	if len(bits) == 4:
		if bits[2] != 'as':
			raise template.TemplateSyntaxError, " Second argument to '%s' tag must be 'as'" % bits[0]
		return PropertyRandomNode(num=bits[1], var_name=bits[3])

	elif len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return PropertyRandomNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])

class PropertyDestaqueNode(template.Node):
	def __init__(self, var_name ,num=None):
		self.var_name=var_name

		if num:
			self.num = int(num)
		else:
			self.num = None

	def render(self, context):
		propertys = Property.objects.all_destaque().order_by('?')

		context[self.var_name] = propertys[:self.num]
		return ''


def do_get_propertys_destaque(parser, token):

	bits = token.contents.split()

	if len(bits) == 4:
		if bits[2] != 'as':
			raise template.TemplateSyntaxError, " Second argument to '%s' tag must be 'as'" % bits[0]
		return PropertyDestaqueNode(num=bits[1], var_name=bits[3])

	elif len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return PropertyDestaqueNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])

class PropertyPhotoDestaqueNode(template.Node):
	def __init__(self, var_name, obj_id=None ,num=None):
		self.var_name=var_name
		self.id = obj_id

		if num:
			self.num = int(num)
		else:
			self.num = None

	def render(self, context):
		
		if self.id:
			obj = template.resolve_variable(self.id, context)
		# TODO: change field name of photo models from image_destaque to image_featured
		if self.id:
			photo = Photo.objects.filter(album_property=int(obj)).filter(image_destaque=True)
			#photo = Photo.objects.filter(album=int(obj)).filter(image_featured=True)
			
		else:
			photo = Photo.objects.filter(image_destaque=True)
			#photo =Photo.objects.filter(image_featured=True)

		context[self.var_name] = photo[:self.num]
		return ''

def do_get_property_photo_destaque(parser, token):

	bits = token.contents.split()
	if len(bits) == 5:
		if bits[3] != 'as':
			raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
		return PropertyPhotoDestaqueNode(obj_id=bits[1],num=bits[2], var_name=bits[4])
	if len(bits) == 6:
		if bits[2] != 'from':
			raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'from'" % bits[0]
		if bits[4] != 'as':
			raise template.TemplateSyntaxError, "Fourth argument to '%s' tag must be 'as'" % bits[0]
		return PropertyPhotoDestaqueNode(num=bits[1], var_name=bits[5], obj_id=bits[3])

	elif len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return PropertyDestaqueNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])

register.tag('get_property_photo',do_get_property_photo)
register.tag('get_propertys',do_get_property)
register.tag('get_propertys_destaque',do_get_propertys_destaque)
register.tag('get_property_photo_destaque',do_get_property_photo_destaque)