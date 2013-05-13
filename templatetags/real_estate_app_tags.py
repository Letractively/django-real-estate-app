# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.safestring import mark_safe

from real_estate_app.models import Photo, Property, District, StatusProperty, Classification, AditionalThings, Portlet, News
from real_estate_app.views.last_visited import get_recently_viewed_proprety_ids

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
			photo = Photo.objects.published().filter(album=int(obj))
			
		else:
			photo = Photo.objects.published()

		context[self.var_name] = photo[:self.num]
		return ''

def do_get_property_photo(parser, token):

	bits = token.contents.split()
	if len(bits) == 5:
		if bits[1] != 'from':
			raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'from'" % bits[0]
		if bits[3] != 'as':
			raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'as'" % bits[0]
		return PropertyAlbumNode(obj_id=bits[2],var_name=bits[4])
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

		if self.id:
			photo = Photo.objects.filter(album=int(obj)).filter(image_destaque=True)
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

class PortletNewsNode(template.Node):
	def __init__(self, var_name):
		self.var_name=var_name
		self.real_estate_node_template="admin/real_estate_app/real_estate_node_list.html"

	def render(self, context):
		"""
			Response to render a portlet object.
		"""
		try:
			portlet_options = Portlet.objects.get(type_portlet='news')
			
			amount = portlet_options.amount_featured
			
			news=News.objects.all()[:amount]

			if portlet_options.featured:
				amount-=1
				news=News.objects.exclude(id=portlet_options.featured.id)[:amount]

			context.update({
				'portlet_objects':news,
				'portlet_featured_obj': portlet_options.featured,
				'portlet':portlet_options
			})
			
		except ObjectDoesNotExist:
			return ''

		return template.loader.get_template(self.real_estate_node_template or [
             	"admin/real_estate_app/real_estate_node_list.html",
            	"admin/real_estate_node_list.html"
		]).render(context)

def do_get_portlet_news(parser, token):
	bits = token.contents.split()
	
	if len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
		return PortletNewsNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one arguments: %s as [varname]" %(bits[0],bits[0])


class NewsNode(template.Node):
	def __init__(self, var_name ,num=None):
		self.var_name=var_name

		if num:
			self.num = int(num)
		else:
			self.num = None

	def render(self, context):
		news = News.objects.all()

		context[self.var_name] = news[:self.num]
		return ''

def do_get_news(parser, token):

	bits = token.contents.split()

	if len(bits) == 4:
		if bits[2] != 'as':
			raise template.TemplateSyntaxError, " Second argument to '%s' tag must be 'as'" % bits[0]
		return NewsNode(num=bits[1], var_name=bits[3])

	elif len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return NewsNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])

class LastedViewedProprety(template.Node):
	def __init__(self, var_name):
		self.var_name=var_name

	def render(self, context):
		request=context['request']
		proprety_ids = get_recently_viewed_proprety_ids(request)
		propretys = Property.objects.filter(id__in=proprety_ids)
		context[self.var_name] = propretys
		return ''

def do_get_last_visited_proprety(parser, token):
	
	bits = token.contents.split()

	if len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return LastedViewedProprety(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname]" % (bits[0],bits[0])

register.tag('get_property_photo',do_get_property_photo)
register.tag('get_propertys',do_get_property)
register.tag('get_propertys_destaque',do_get_propertys_destaque)
register.tag('get_property_photo_destaque',do_get_property_photo_destaque)
register.tag('get_select_district',do_get_options_select_district)
register.tag('get_select_statusproperty',do_get_options_select_statusproperty)
register.tag('get_select_classification_property',do_get_options_select_classification_property)
register.tag('get_checked_aditional_things_property',do_get_options_checked_aditonal_things_property)
register.tag('get_portlet_news',do_get_portlet_news)
register.tag('get_news',do_get_news)
register.tag('get_last_visited_proprety',do_get_last_visited_proprety)