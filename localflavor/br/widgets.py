# -*- coding: utf-8 -*-

from django.forms.widgets import TextInput
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

class CPFInputWidget(TextInput):
	
	def render(self, name, value, attrs=None):

		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s alt="cpf" />' % flatatt(final_attrs) )

class RGInputWidget(TextInput):
	
	def render(self, name, value, attrs=None):

		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s alt="rg" />' % flatatt(final_attrs) )

class CNPJInputWidget(TextInput):
	
	def render(self, name, value, attrs=None):

		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s alt="cnpj" />' % flatatt(final_attrs) )