# -*- coding: utf-8 -*-
from datetime import datetime

from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template.base import compile_string, VariableNode 
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from real_estate_app.utils import RenderVariablesString
from real_estate_app.apps.propertys.models import Property
from real_estate_app.apps.visitcalendar.models import VisitEvent, TermVisit

register = template.Library()
       
class TermVisitNode(template.Node):
        def __init__(self, var_name, object_id=None):

            try:
                self.object_id = object_id and int(object_id) or object_id
            except ValueError:
                self.object_id =  template.Variable(object_id)

            self.var_name=var_name

        def render(self, context):
            context_termvisit= {}

            if self.object_id and type(self.object_id) != int:
                try:
                    self.object_id=int(self.object_id)
                except:
                    self.object_id=self.object_id.resolve(context)
                
            try:
                visitevent=VisitEvent.objects.get(id=self.object_id)
                if not visitevent.visitor_fk:
                    raise template.TemplateSyntaxError, "Error occur when get visitor for VisitEvent: %s" % visitevent
            except ObjectDoesNotExist:
                return ''

            visitor = visitevent.visitor_fk
            term_text=TermVisit.objects.all()[0].text
            context[self.var_name]= RenderVariablesString(term_text,'real_estate_app.apps.visitcalendar',visitor).render_variables()
            return ''

def do_get_termvisit(parser, token):
        """
            This function tag can be called with this params:

                - Call default Term visit:
                {% \get_termvisit from [property_id] as [varname] %}
        """
        bits = token.contents.split()
        params ={}
        if 'as' not in bits and 'from' not in bits:
            raise template.TemplateSyntaxError, "'%s' tag must has 'as' and 'from' params: %s from [visitevent_id] as [varname]" % (bits[0], bits[0])

        for ct, bit in enumerate(bits):
            if bit == 'as':
                try:
                    params.update({'var_name':bits[ct+1]})
                except IndexError:
                    raise template.TemplateSyntaxError, "Varname argument to '%s' tag must be preceded 'as': %s as [varname]" % (bits[0], bits[0])

            if bit == 'from':
                try:
                    params.update({'object_id':bits[ct+1]})
                except IndexError:
                    raise template.TemplateSyntaxError, "Proprety object id argument to '%s' tag must be preceded 'from': %s from [property_id] as [varname]" % (bits[0], bits[0])


        return TermVisitNode(**params)


register.tag('get_termvisit',do_get_termvisit)