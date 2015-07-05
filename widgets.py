# -*- coding: utf-8 -*-
from decimal import Decimal
from itertools import chain

from django.contrib.admin import widgets
from django.conf import settings 
from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms import MultiWidget, DateInput, TimeInput, SplitDateTimeWidget
from django.forms.widgets import TextInput, CheckboxSelectMultiple, CheckboxInput,\
								 SelectMultiple, FileInput
from django.forms.util import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.translation import ugettext_lazy as _

from real_estate_app.conf.settings import MEDIA_PREFIX, REAL_ESTATE_APP_AJAX_SEARCH
from real_estate_app.utils import AutoCompleteObject, radomstring

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

class CelphoneInputWidget(TextInput):
	
	def render(self, name, value, attrs=None):

		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s alt="celphone" />' % flatatt(final_attrs) )

class ImageInputWidget(FileInput):

	def __init__(self,width=200,height=150,attrs=None):
		self.width=width
		self.height=height
		super(ImageInputWidget,self).__init__(attrs=attrs)

	def render(self, name, value, attrs=None):
		"""
			This custom ImageInputWidget works only with bootstrap-fileupload and bootstrap.
		"""
		output=[]
		file_extists=''
		file_extists_id=''
		class_file = value and 'fileupload-exists' or 'fileupload-new'

		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			
			final_attrs['value'] = force_unicode(self._format_value(value))
			
			from sorl.thumbnail import get_thumbnail
			size = str(self.width)+'x'+str(self.height)
			try:
				img = get_thumbnail(value, size, crop='center', quality=99)
				file_extists = """<img src="%s" />""" % img.url
			except:
				# When get error on form return no image.
				file_extists = """<img src="http://www.placehold.it/%sx%s/EFEFEF/AAAAAA&text=no+image" />""" % (self.width,self.height)

			file_extists_id='-'.join(final_attrs['name'].split('-')[:-1])
			final_attrs['data-target']=u"#%s" % file_extists_id
			
			

		input_file=mark_safe(u'<input%s />' % flatatt(final_attrs))

		output.append("""<script type="text/javascript" src="%sbootstrap2/plugins/bootstrap-fileupload.min.js" ></script> \
						 <script type="text/javascript" src="%sadmin/js/real_estate_app_fileupload.js" ></script> \
						 <link media="screen" rel="stylesheet" href="%sbootstrap2/plugins/bootstrap-fileupload.min.css">""" % (MEDIA_PREFIX, MEDIA_PREFIX, MEDIA_PREFIX) )
		output.append("""<div class="fileupload %s" data-provides="fileupload" >""" % (class_file) )
		output.append("""		<div class="fileupload-new thumbnail" style="width: %spx; height: %spx;">
									<img src="http://www.placehold.it/%sx%s/EFEFEF/AAAAAA&text=no+image" />
								</div>""" % (self.width,self.height,self.width,self.height))
		output.append("""	<div class="fileupload-preview fileupload-exists thumbnail" style="max-width: %spx; max-height: %spx; line-height: 20px;"> \
								%s \
							</div> \
							<div class="photos-btn"> \
								<span class="btn btn-file"> \
									<span class="fileupload-new">Select image</span> \
									<span class="fileupload-exists">Change</span> \
									%s \
								</span> \
								<a href="#" class="btn fileupload-exists" data-dismiss="fileupload">Remove</a> \
							</div> \
						</div>"""  % (self.width, self.height, file_extists, input_file))
		
		return mark_safe(u''.join(output))


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

			module_name = rel_to._meta.module_name
			try:
				field=','.join(REAL_ESTATE_APP_AJAX_SEARCH[module_name]['label'])
			except KeyError:
				raise Exception("Error you need configure REAL_ESTATE_APP_AJAX_SEARCH for module name: %s" % module_name)
			## TO DO: Fazer tratamento para pegar se o campo e select 
			##        para ser utilizado no facebox.
			if self.can_add_related:
				output.insert(0,u'<div class="input-append">')
				output.append(u'''
				<script type="text/javascript">
					django.jQuery(document).ready(function($) {
						$('a[rel="facebox-select"]').facebox({
						loadingImage : '%simg/loading.gif',
						closeImage   : '%simg/closelabel.png',
						id: '%s',
						ajax_url: '%s',
						type_field:'select',
						field:'%s',
						})
					})
				</script>''' % ( MEDIA_PREFIX, MEDIA_PREFIX, 'id_'+name, ajax_url, field) )
				output.append(u'<a href="%s" class="add-another btn" id="id_%s" rel="facebox-select" rev="iframe" > ' %(related_url, name))
				output.append(u'<i class="icon-plus-sign"></i>  </a>')
				output.append(u'</div>')
			return mark_safe(u''.join(output))
		except NoReverseMatch:
			return super(FaceBoxFieldWrapper,self).render(name,value,*args,**kwargs)

class CheckboxSelectMultipleCustom(CheckboxSelectMultiple):
	#TODO: change to SelectMultiple and try to make like RelatedFieldWidgetWrapper
	def __init__(self, module_name=None,field=None, app_name=None,can_add_related=False,*args,**kwargs):
		self.module_name=module_name
		self.field=field
		self.app_name=app_name
		self.can_add_related = can_add_related

		return super(CheckboxSelectMultipleCustom,self).__init__(*args,**kwargs)

	def render(self, name, value, attrs=None, choices=()):

		field=self.field
		name_db=name.strip('_fk')
		rev_url = reverse('admin:index') 
		info = (rev_url, self.app_name, self.module_name)
		#related_url = reverse('admin:%s_%s_add_popup' % ('real_estate_app', name_db))
		#ajax_url = reverse('admin:%s_%s_ajax_view/' %('real_estate_app', name_db))
		related_url = '%s%s/%s/add/?_popup=1' % info
		ajax_url = '%s%s/%s/ajax/' %info

		output =[]

		if not self.field and self.module_name:
			field=','.join(REAL_ESTATE_APP_AJAX_SEARCH[self.module_name]['label'])

		if self.can_add_related:
			output.append(u'''
					<script type="text/javascript">
						django.jQuery(document).ready(function($) {
							$('a[rel="facebox-check"]').facebox({
							loadingImage : '%simg/loading.gif',
							closeImage   : '%simg/closelabel.png',
							id: '%s',
							ajax_url: '%s',
							type_field:'checkbox',
							field:'%s',
							})
						})
					</script>''' % (MEDIA_PREFIX, MEDIA_PREFIX,'id_'+self.module_name, ajax_url, field) )
			output.append(u'<a href="%s" class="add-another btn" id="id_%s" rel="facebox-check" rev="iframe" > ' %(related_url, name_db))
			output.append(u'<i class="icon-plus-sign"></i>  </a>')
		
		if value is None: value = []
		has_id = attrs and 'id' in attrs
		final_attrs = self.build_attrs(attrs, name=name)
		

		output.append(u'<ul id="id_%s" style="float:left">' %name_db)
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
				output.append(u'</ul>\n<ul id="id_%s" style="float:left">' %name_db)

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
		
		plugin_options = {
			'minLength':self.ajax_length,
			'source': reverse('%s_%s_ajax_view' % (self.apps,self.module_name)),
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
	def __init__(self, model_fk, show_help_text=False, help_text='',can_add_related=False,*args, **kwargs):
		super(AdminAjaxSelectMultipleInputWidget, self).__init__(*args, **kwargs)
		self.show_help_text=show_help_text
		self.help_text=help_text
		self.model=model_fk
		self.module_name=self.model._meta.module_name
		self.apps=self.model._meta.app_label
		self.can_add_related = can_add_related
		
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
			'can_add':self.can_add_related,
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
			'search_value':_('Search for realtors.'),
			'can_add':self.can_add_related

		}

		return mark_safe(render_to_string(
										  ('real_estate_app/autocompleteselectmultiple.html',
										   'admin/real_estate_app/autocompleteselectmultiple.html'),
										   context)
				)

	def value_from_datadict(self, data, files, name):
		return [long(val) for val in data.get(name,'').split('|') if val]

class CustomDateInput(DateInput):

	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u"""<div id="date-widget" class="input-append"> \
			                    <input%s data-format="%s" /> \
			                    <span class="add-on"> \
			                          <i data-time-icon="icon-time" data-date-icon="icon-calendar"></i> \
			                    </span> \
			                </div>""" % (flatatt(final_attrs), 'yyyy-MM-dd'))

class CustomAdminDateWidget(CustomDateInput):
    class Media:
        js = (MEDIA_PREFIX + "bootstrap2/plugins/bootstrap-datetimepicker.min.js",
              MEDIA_PREFIX + "admin/js/DateTime.js")

    def __init__(self, attrs={}, format=None):
        super(CustomAdminDateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'}, format=format)

class CustomTimeInput(TimeInput):

	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u"""<div id="time-widget" class="input-append"> \
			                    <input%s data-format="%s" /> \
			                    <span class="add-on"> \
			                          <i data-time-icon="icon-time" data-date-icon="icon-time"></i> \
			                    </span> \
			                </div>""" % (flatatt(final_attrs), 'hh:mm:ss'))

class CustomAdminTimeWidget(CustomTimeInput):
	
    class Media:
        js = (MEDIA_PREFIX + "bootstrap2/plugins/bootstrap-datetimepicker.js",
              MEDIA_PREFIX + "admin/js/DateTime.js")


	def __init__(self, attrs={}, format=None):
		super(CustomAdminTimeWidget, self).__init__(attrs={'class': 'vTimeField', 'size': '8'}, format=format)

class CustomAdminSplitDateTime(SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
    	widgets = [CustomAdminDateWidget, CustomAdminTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(u'%s %s<br />%s %s' % \
            (_('Date:'), rendered_widgets[0], _('Time:'), rendered_widgets[1]))
        