import operator
from functools import wraps

from django.conf import settings
from django.contrib.admin.util import quote
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode, smart_unicode, smart_str
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst

from real_estate_app.conf.settings import REAL_ESTATE_APP_AJAX_SEARCH, MEDIA_PREFIX


def alertemail(function):
	#print 'alertemail: ',args, kwargs
	@wraps(function)
	def wrapper(self,*args,**kwargs):
		function.func_globals['self']=self
		print 'funtion: ', args, kwargs
		return function(self,*args,**kwargs)
	return wrapper
	
class A(object):
	teste='Variavel teste'
	@alertemail
	def alo(self, tunts,puts):
		print 'self.alo foi sem problemas'	
	

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
					'real_value':' '.join([model[f] for f in self.return_values if not (f in ('pk','id') or f in self.image_fields)]),
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
					'all_fields':[{f:mark_safe(model[f])} for f in self.all_fields if f in self.all_fields ]
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