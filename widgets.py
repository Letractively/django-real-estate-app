# -*- coding: utf-8 -*-
from decimal import Decimal
from itertools import chain

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.forms.widgets import TextInput, Select, CheckboxSelectMultiple, CheckboxInput
from django.forms.util import flatatt
from django.conf import settings 
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, NoReverseMatch

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

class FaceBoxFieldWrapper(widgets.RelatedFieldWidgetWrapper):

    def render(self, name, value, *args, **kwargs):

		rel_to = self.rel.to

		try:
			rev_url = reverse('admin:index') 
			info = (rev_url, rel_to._meta.app_label, rel_to._meta.object_name.lower())

			related_url = '%s%s/%s/add_popup' % info
			ajax_url = '%s%s/%s/ajax_view/' %info

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
			
			output.append(u'<a href="%s" class="add-another" id="id_%s" rel="facebox-select" rev="iframe|400" > ' %(related_url, name))
			output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))

			return mark_safe(u''.join(output))
		except NoReverseMatch:
			pass

class CheckboxSelectMultipleCustom(CheckboxSelectMultiple):

	def render(self, name, value, attrs=None, choices=()):

		name_db=name.strip('_fk')
		rev_url = reverse('admin:index') 
		info = (rev_url, 'real_estate_app', name_db)
		related_url = '%s%s/%s/add_popup' % info
		ajax_url = '%s%s/%s/ajax_view/' %info

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
		output.append(u'<a href="%s" class="add-another" id="id_%s" rel="facebox-check" rev="iframe|350" > ' %(related_url, name_db))
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

