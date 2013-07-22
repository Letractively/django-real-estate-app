# -*- coding: utf-8 -*-
import operator
from functools import wraps

from django.db.models import Model
from django.conf import settings
from django.contrib.admin.util import quote
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template import Context, Template, VariableNode, compile_string
from django.utils.encoding import force_unicode, smart_unicode, smart_str
from django.utils.importlib import import_module
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from real_estate_app.conf.settings import REAL_ESTATE_APP_AJAX_SEARCH, MEDIA_PREFIX

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class TranslateVariableObjectError(Exception):
	pass

def alertemail(instance=None, subtitle='', msg='', email_from='', emails_to=[],fields=()):
	if instance:
		if fields:
			fields_f = (callable(getattr(instance,field)) and getattr(instance,field)() or getattr(instance,field) for field in fields)
			msg = msg.format(*fields_f)
		send_mail(subtitle,msg,email_from,emails_to, fail_silently=False)
		return True
	raise Exception("On function alteremail instance is required.")

def format_link_callback(obj,admin_site):
        has_admin = obj.__class__ in admin_site._registry
        opts = obj._meta

        if has_admin:
            admin_url = reverse('%s:%s_%s_change'
                                % (admin_site.name,
                                   opts.app_label,
                                   opts.object_name.lower()),
                                None, (quote(obj._get_pk_val()),))
            p = '%s.%s' % (opts.app_label,
                           opts.get_delete_permission())
            # Display a link to the admin page.
            return mark_safe(u'%s: <a href="%s">%s</a>' %
                             (escape(capfirst(opts.verbose_name)),
                              admin_url,
                              escape(obj)))
        else:
            # Don't display link to edit, because it either has no
            # admin or is edited inline.
            return u'%s: %s' % (capfirst(opts.verbose_name),
                                force_unicode(obj))

def radomstring(max=10):
	import random
	string='abcdefghijklmnopqrstuvxywz1234567890'
	a=''
	for i in random.sample(string,max):
		a+=i
	return a

class RenderVariablesString(object):

	def __init__(self,text2convert=None,app=None,obj=None):
		if not obj and app:
			raise TranslateVariableObjectError("Error RenderVariablesString needed app and object.")
		self.obj = obj
		self.app = app
		self.text2convert = text2convert

	def str_variables_locale(self):
		variables = self.locale_variables_from_obj()
		string = ""
		for key, value in variables.items():
			string+="\n\t\t\t {{ %s }}" % key 
		return string

	def locale_variables_from_obj(self):
		"""
			This function is used to get translation of variables used on middles of CharFields or TextFields from models
			exemple on pt-br:
			class TermVisit(models.Model):
				text=models.TextField()
				...
			news = TermVisit('Today keys of property is outed with visitor: 
				              Name: {{ nome }}  
				              Address: {{ endereco }}...')
			
			when 'render_variables' function is called, this function 'locale_variables_from_obj' is called to translate 
			variables '{{ nome }}', '{{ endereco }}' to '{{ name }}', '{{ address }}' and return the real value of variable 
			inside of object passed.
		"""
		if LANGUAGE_CODE in ('pt_BR','pt-br'):
			try:
				code_langague=LANGUAGE_CODE.split('-')[1]
			except IndexError:
				code_langague='br'

		try:
			obj=self.obj
			if hasattr(self.obj,'__module__'):
				obj=self.obj.__module__.split('.')[-1]
			
			module_name='%s.localflavor.%s.models_variables' % (self.app,code_langague)
			variable='variables_%s_translate' % obj
			module=import_module(module_name,variable)
			return getattr(module,variable)
		except Exception, error:
			raise TranslateVariableObjectError, error


	def render_variables(self):
		
		context ={}
		locale_variables = self.locale_variables_from_obj()
		variables = [ 
			str(var_name.filter_expression.token) 
			for var_name in compile_string(self.text2convert,self.text2convert) 
			if isinstance(var_name,VariableNode)
		]
		msg=_("Doesn't exist this variable '%(field)s' for '%(object)s'.")

		try:
			for field in variables:
				context.update({
					field:getattr(
						self.obj,
						locale_variables and locale_variables.get(field,field) or field, # get real variable on obj
						msg % {'field': field, 'object': self.obj._meta.verbose_name }
					)
				})
			context=Context(context)
			return mark_safe('%s' % Template(self.text2convert).render(context))
		except Exception, error:
			raise TranslateVariableObjectError, error
		

class AutoCompleteObject(object):
	"""
	This class you pass as param to simplejson.dump for redenring according the template of model you pass.
	"""
	# TODO: better this code

	def __init__(self,model):

		self.model=model
		self.module_name=self.model._meta.module_name
		self.image_fields=[]
		self.thumbnail=[]
		self.all_fields=[]
		self.thumbnail_ajax=REAL_ESTATE_APP_AJAX_SEARCH.get(self.module_name).get('thumbnail_ajax','')
		self.return_all_fields=REAL_ESTATE_APP_AJAX_SEARCH.get(self.module_name).get('all_fields',False)
		if self.return_all_fields:
			self.all_fields=[field.name == 'id' and 'pk' or field.name for field in model._meta.fields]
		try:
			self.fields_search=REAL_ESTATE_APP_AJAX_SEARCH[self.module_name]['search_fields']
			self.return_values=REAL_ESTATE_APP_AJAX_SEARCH[self.module_name]['return_values']
		except KeyError:
			raise ImproperlyConfigured("settings.REAL_ESTATE_APP_AJAX_SEARCH not configured correctly for %s." % self.module_name)



	def getSpecialField(self,models,fields=''):
		from django.core.files.images import ImageFile
		from django.db.models.query import QuerySet

		if isinstance(models,QuerySet) and isinstance(fields,(list,tuple)) :
			from itertools import product 
			return [field for model,field in product(models,fields) 
			        if isinstance(getattr(model,field,None),ImageFile) and not field in ('pk','id')]

		return []

	def filter(self,value='',**kwargs):
		from django.db.models import Q
		
		queryset = self.model.objects.all()

		if self.fields_search and value:
			query=[Q(**{'%s__icontains' %field: value}) for field in self.fields_search]
			queryset=queryset.filter(reduce(operator.or_,query))

		if kwargs:
			queryset=queryset.filter(**kwargs)

		if isinstance(self.return_values,(list,tuple)) and self.return_values and not self.return_all_fields:
			# return only the settings.<model>[return_values] if all_fields is False
			self.image_fields=self.getSpecialField(queryset,self.return_values)
			queryset=queryset.values(*self.return_values)
		elif self.return_all_fields:
			self.image_fields=self.getSpecialField(queryset,self.all_fields)
			queryset=queryset.values(*self.all_fields)
		
		return queryset

	def render(self,value='',**kwargs):
		"""
			This render a json format for autocomplete.js plugin customized for jquery-ui autocomplete.
		"""
		from django.utils.safestring import mark_safe
		from django.template.loader import render_to_string
		return [{
					'pk':model.get('pk',model.get('id','')),
					'search_fields':[model[f] for f in self.fields_search if not (f in ('pk','id') or f in self.image_fields)],
					'real_value':' '.join([model[f] for f in self.return_values if not (f in ('pk','id') or f in self.image_fields)]),
					'return_values':dict([(f, mark_safe(model[f])) for f in self.return_values if not (f in ('pk','id') or f in self.image_fields)]),
					'value': mark_safe(render_to_string(
										  				('real_estate_app/autocompleteselectmultiple_response_ajax.html',
									   	   				'admin/real_estate_app/autocompleteselectmultiple_response_ajax.html'
									   	   				),
									   	 				{
									   	 					'model': self.forcePositionFieldsShow(model),
									   	 					'image_fields':self.image_fields,
									   	 					'MEDIA_PREFIX':MEDIA_PREFIX,
									   	 					'MEDIA_URL':settings.MEDIA_URL
									   	 				}
							   			)
					),
					'all_fields':dict([(f,mark_safe(model[f])) for f in self.all_fields if f in self.all_fields ])
				} for model in self.filter(value,**kwargs)]					

	def forcePositionFieldsShow(self,filter_values):
		"""
		This function is necessery because when you try to return a position values on dict, it's return a 
		orded keys, not position key.
		# TODO: Make a dict orded by position not by key.
		"""
		from sorl.thumbnail import get_thumbnail

		if isinstance(filter_values,dict):
			tmp_fields_values=[]
			for ct, field in enumerate(self.return_values):
				if field in self.image_fields and filter_values[field]:
					tmp_fields_values.append((field,get_thumbnail(filter_values[field],self.thumbnail_ajax, quality=99)))
				else:
					tmp_fields_values.append((field,filter_values[field]))
			
			return tmp_fields_values

		raise "Error"

def addHtmlAttr(string, attr, attr_value=''):

	attributes=string.split(' ')
	new_attr=''
	value=''
	for ct,attrs in enumerate(attributes):
		splited=attrs.split('=')
		if splited[0] == attr:
			value=splited[1].replace('"','')
			attributes.pop(ct)
			
		new_attr=''.join([' ',attr,'="',value,' ',attr_value,'"'])

	attributes.append(new_attr)
	return ''.join(attributes)
