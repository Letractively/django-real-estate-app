# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from real_estate_app.apps.portlets.models import Portlet
from real_estate_app.apps.portlets.utils import get_portlet_model

register = template.Library()
       
class PortletsNode(template.Node):
        def __init__(self, var_name, type_portlet):
                self.var_name=var_name
                self.type_portlet=type_portlet
                self.real_estate_node_template="admin/portlets/real_estate_node_list.html"

        def render(self, context):
                """
                        Response to render a portlet object.
                """
                # TODO: Better the acept null amount.
                try:
                        PortletObjects=get_portlet_model(self.type_portlet)

                        portlet_options = Portlet.objects.get(type_portlet=self.type_portlet)
                       
                        amount = portlet_options.amount_featured or 10

                        PortletObjects=PortletObjects.objects.all()[:amount]

                        if portlet_options.featured:
                                amount-=1
                                PortletObjects=PortletObjects.objects.exclude(id=portlet_options.featured.id)[:amount]

                        context.update({
                                'portlet_objects':PortletObjects,
                                'portlet_featured_obj': portlet_options.featured,
                                'portlet':portlet_options
                        })
                
                except ObjectDoesNotExist:
                        url = reverse('portlet-add')
                        return mark_safe(
                        """<a href="%s" >%s</a> """ % (url, _('Add portlet'))
                        )

                return template.loader.get_template(self.real_estate_node_template or [
                "admin/real_estate_app/real_estate_node_list.html",
                "admin/real_estate_node_list.html"
                ]).render(context)

def do_get_portlets(parser, token):
        bits = token.contents.split()
       
        if len(bits)==4:
                if bits[1]!='as':
                        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
                return PortletsNode(var_name=bits[2],type_portlet=bits[3])
        else:
                raise template.TemplateSyntaxError, "'%s' tag takes one arguments: %s as [varname] [type_portlet]" %(bits[0],bits[0])

register.tag('get_portlets',do_get_portlets)
