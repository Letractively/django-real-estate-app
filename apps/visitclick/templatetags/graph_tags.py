# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render_to_response
from django.template.base import compile_string, VariableNode 
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from real_estate_app.utils import radomstring

register = template.Library()

class GraphClickNode(template.Node):
		def __init__(self, var_name,html_id='chart',display='today'):
			self.var_name=var_name
			self.real_estate_node_template='admin/templatetags/graphs/graphs.html'
			self.html_id=html_id
			self.html_id+=radomstring(max=20)
			self.display=display

		def render(self, context):

			plugins_options={
				'ajaxUrl': reverse('visitclick_data_json_view'),
				'type_chart':'AreaChart',
				'gchart':{'title':str(_('Amount clicks')),},
				'display':self.display
			}

			context.update({
				'plugin_options':mark_safe(plugins_options),
				'html_id':self.html_id,
				'display':'month'
			})

			context[self.var_name]=template.loader.get_template(self.real_estate_node_template).render(context)
			return ''

def do_get_linegraph(parser, token):
		"""
			This function tag can be called with this params:

				- Call default Term visit:
				{% \get_linegraph as [varname] %}
        """
		bits = token.contents.split()
		params ={}
        
		for ct, bit in enumerate(bits):
			if bit == 'as':
				try:
					params.update({'var_name':bits[ct+1]})
				except IndexError:
					raise template.TemplateSyntaxError, "Varname argument to '%s' tag must be preceded 'as': %s as [varname]" % (bits[0], bits[0])
		return GraphClickNode(**params)
register.tag('get_linegraph',do_get_linegraph)