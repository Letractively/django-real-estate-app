# -*- coding: utf-8 -*-
from decimal import Decimal
from itertools import chain

from django.contrib.admin import widgets
from django.conf import settings 
from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms.widgets import TextInput, CheckboxSelectMultiple, CheckboxInput, SelectMultiple
from django.forms.util import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.translation import ugettext_lazy as _

from real_estate_app.conf.settings import MEDIA_PREFIX, REAL_ESTATE_APP_AJAX_SEARCH
from real_estate_app.utils import AutoCompleteObject


class MoneyInputWidget(TextInput):

	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			
			if str(value).find('.') == -1:
				value=Decimal(str(value)+'.00')
			elif str(value).split('.'):
				if len(str(value).split('.')[1]) < 2:
					value=Decimal(str(value)+'0')
				
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s alt="money" />' % flatatt(final_attrs) )

class ZipInputWidget(TextInput):
	
	def render(self, name, value, attrs=None):

		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s alt="zip_code" />' % flatatt(final_attrs) )

class PhoneInputWidget(TextInput):
	
	def render(self, name, value, attrs=None):

		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s alt="phone" />' % flatatt(final_attrs) )

class FaceBoxFieldWrapper(widgets.RelatedFieldWidgetWrapper):

    def render(self, name, value, *args, **kwargs):

		rel_to = self.rel.to

		try:
			rev_url = reverse('admin:index') 

			info = (rev_url, rel_to._meta.app_label, rel_to._meta.object_name.lower())
			
			#related_url = reverse('admin:%s_%s_add_popup' % (rel_to._meta.app_label, rel_to._meta.object_name.lower() ) )
			#ajax_url = reverse('admin:%s_%s_ajax_view/' % (rel_to._meta.app_label, rel_to._meta.object_name.lower()) )

			related_url = '%s%s/%s/add/?_popup=1' % info
			ajax_url = '%s%s/%s/ajax/' %info

			self.widget.choices = self.choices
			output = [self.widget.render(name, value, *args, **kwargs)]
			field = rel_to._meta.fields[1].name
			## TO DO: Fazer tratamento para pegar se o campo e select 
			##        para ser utilizado no facebox.
			output.append(u'''
			<script type="text/javascript">
				django.jQuery(document).ready(function($) {
					django.jQuery('a[rel="facebox-select"]').facebox({
					loadingImage : '/media-real/img/loading.gif',
					closeImage   : '/media-real/img/closelabel.png',
					id: '%s',
					ajax_url: '%s',
					type_field:'select'
					})
				})
			</script>''' % ('id_'+name, ajax_url) )
			output.append(u'<a href="%s" class="add-another" id="id_%s" rel="facebox-select" rev="iframe" > ' %(related_url, name))
			output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))

			return mark_safe(u''.join(output))
		except NoReverseMatch:
			return super(FaceBoxFieldWrapper,self).render(name,value,*args,**kwargs)

class CheckboxSelectMultipleCustom(CheckboxSelectMultiple):

	def render(self, name, value, attrs=None, choices=()):

		name_db=name.strip('_fk')
		rev_url = reverse('admin:index') 
		info = (rev_url, 'real_estate_app', name_db)
		#related_url = reverse('admin:%s_%s_add_popup' % ('real_estate_app', name_db))
		#ajax_url = reverse('admin:%s_%s_ajax_view/' %('real_estate_app', name_db))
		related_url = '%s%s/%s/add/?_popup=1' % info
		ajax_url = '%s%s/%s/ajax/' %info

		output =[]

		output.append(u'''
			<script type="text/javascript">
				django.jQuery(document).ready(function($) {
					django.jQuery('a[rel="facebox-check"]').facebox({
					loadingImage : '/media-real/img/loading.gif',
					closeImage   : '/media-real/img/closelabel.png',
					id: '%s',
					ajax_url: '%s',
					type_field:'checkbox'
					})
				})
			</script>''' % ('id_'+name_db, ajax_url) )
		
		if value is None: value = []
		has_id = attrs and 'id' in attrs
		final_attrs = self.build_attrs(attrs, name=name)
		output.append(u'<a href="%s" class="add-another" id="id_%s" rel="facebox-check" rev="iframe" > ' %(related_url, name_db))
		output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a><br />' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))

		output.append(u'<ul id=id_%s style="float:left">' %name_db)
		# Normalize to strings
		str_values = set([force_unicode(v) for v in value])
		limit=5
		
		for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):

			# If an ID attribute was given, add a numeric index as a suffix,
			# so that the checkboxes don't all have the same ID attribute.
			if has_id:
				final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
				label_for = u' for="%s"' % final_attrs['id']
			else:
				label_for = ''
			
			cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
			option_value = force_unicode(option_value)
			rendered_cb = cb.render(name, option_value)
			option_label = conditional_escape(force_unicode(option_label))
			output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
			
			if ((i+1)%limit == 0) :
				output.append(u'</ul>\n<ul id=id_%s style="float:left">' %name_db)

		output.append(u'</ul>')
		return mark_safe(u'\n'.join(output))

class AreaInputWidget(TextInput):

	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			
			if str(value).find('.') == -1:
				value=Decimal(str(value)+'.00')
			elif str(value).split('.'):
				if len(str(value).split('.')[1]) < 2:
					value=Decimal(str(value)+'0')
				
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s alt="area" /> m²' % flatatt(final_attrs) )

class AjaxInputWidget(TextInput):
	"""
		This code is based on app django-ajax-selects
	"""
	def __init__(self, model_fk, show_help_text=False, help_text='',ajax_length=3, *args, **kwargs):
		super(AjaxInputWidget, self).__init__(*args, **kwargs)
		self.show_help_text=show_help_text
		self.help_text=help_text
		self.model=model_fk
		self.module_name=self.model._meta.module_name
		self.apps=self.model._meta.app_label
		self.ajax_length=ajax_length

		try:
			self.fields_show=REAL_ESTATE_APP_AJAX_SEARCH[self.module_name]['search_fields']
		except KeyError:
			raise Exception('You have to put on settings file the dictionary named REAL_ESTATE_APP_AJAX_SEARCH={"model":<list of fields>}')

	def render(self,name, value, attrs=None, choices=()):
		if value is None: value = []
		
		autocompleteobject=AutoCompleteObject(self.model)

		if self.show_help_text: 
			help_text=self.help_text
		else:
			help_text=''

		final_attrs = self.build_attrs(attrs, name=name)
		self.html_id = final_attrs.pop('id', name)
		#import pdb;pdb.set_trace()
		plugin_options = {
			'minLength':self.ajax_length,
			'source': reverse('%s_%s_ajax_view' % (self.apps,self.module_name)),
			#'initial': autocompleteobject.render(id__in=str(value)),
			'fields':self.fields_show,
		}
		
		context = {
			'name':name,
			'current':value,
			'html_id':self.html_id,
			'help_text':help_text,
			'plugin_options':mark_safe(simplejson.dumps(plugin_options)),
			'MEDIA_PREFIX': MEDIA_PREFIX,
			'ADMIN_MEDIA_PREFIX':settings.ADMIN_MEDIA_PREFIX,
			'search_value':_('Search...')

		}

		return mark_safe(render_to_string(
										  ('real_estate_app/autocompleteinput.html',
										   'admin/real_estate_app/autocompleteinput.html'),
										   context)
				)

class AdminAjaxSelectMultipleInputWidget(SelectMultiple):
	"""
		This code is based on app django-ajax-selects
	"""
	def __init__(self, model_fk, show_help_text=False, help_text='',*args, **kwargs):
		super(AdminAjaxSelectMultipleInputWidget, self).__init__(*args, **kwargs)
		self.show_help_text=show_help_text
		self.help_text=help_text
		self.model=model_fk
		self.module_name=self.model._meta.module_name
		self.apps=self.model._meta.app_label
		
		try:
			self.fields_show=REAL_ESTATE_APP_AJAX_SEARCH[self.module_name]['search_fields']
		except KeyError:
			raise u'You have to put on settings file the dictionary named REAL_ESTATE_APP_AJAX_SEARCH={"model":<list of fields>}'

	def render(self,name, value, attrs=None, choices=()):
		if value is None: value = []
		
		autocompleteobject=AutoCompleteObject(self.model)

		if self.show_help_text: 
			help_text=self.help_text
		else:
			help_text=''

		final_attrs = self.build_attrs(attrs, name=name)
		self.html_id = final_attrs.pop('id', name)

		if value:
			current_ids = "|" + "|".join( str(pk) for pk in value ) + "|" # |pk|pk| of current
		else:
			current_ids = "|"
		
		related_url_facebox=reverse('admin:%s_%s_add_popup' % (self.apps,self.module_name))+'?_popup=1'
		# TODO: check persmission of can add on admin site.
		plugin_options = {
			'source': reverse('admin:%s_%s_ajax_view' % (self.apps,self.module_name)),
			'initial': autocompleteobject.render(id__in=[str(v) for v in value]),
			'fields':self.fields_show,
			'ajax_url_facebox': related_url_facebox,
			'can_add':True,
		}
		
		context = {
			'name':name,
			'current':value,
			'html_id':self.html_id,
			'help_text':help_text,
			'plugin_options':mark_safe(simplejson.dumps(plugin_options)),
			'MEDIA_PREFIX': MEDIA_PREFIX,
			'related_url_facebox':related_url_facebox,
			'ADMIN_MEDIA_PREFIX':settings.ADMIN_MEDIA_PREFIX,
			'add_text': _('Add Another'),
			'search_value':_('Search for realtors.')

		}

		return mark_safe(render_to_string(
										  ('real_estate_app/autocompleteselectmultiple.html',
										   'admin/real_estate_app/autocompleteselectmultiple.html'),
										   context)
				)

	def value_from_datadict(self, data, files, name):
		return [long(val) for val in data.get(name,'').split('|') if val]


