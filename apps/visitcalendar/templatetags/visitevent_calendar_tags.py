# -*- coding: utf-8 -*-
from datetime import datetime

from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from real_estate_app.apps.propertys.models import Property
from real_estate_app.apps.visitcalendar.models import VisitEvent 

register = template.Library()
       
class CalendarVisitEventNode(template.Node):
        def __init__(self, var_name, object_id=None, date='', display='month', height=None, 
                     editable=False, admin=False, headers=False, events=True):

            try:
                self.object_id = object_id and int(object_id) or object_id
            except ValueError:
                self.object_id =  template.Variable(object_id)

            self.var_name=var_name
            self.display=display
            self.date=date
            self.events=events
            self.height=height
            self.headers=headers
            self.admin = admin
            self.editable = editable

            if self.object_id and not self.admin:
                self.add_url = reverse('visitcalendar-create-object',args=(object_id,))
            else:
                self.add_url = reverse('admin:visitcalendar_visitevent_add')
            
            
            self.real_estate_node_template="visitcalendar/admin/visitcalendar_list_%s_node.html" % self.display

            if self.display == 'week':
                self.display='agendaWeek'
            if self.display == 'day':
                self.display='agendaDay'


        def render(self, context):
            """
                Response to render a portlet object.
            """
            # TODO: Better the acept null amount.
            property=False
            if self.object_id and type(self.object_id) != int:
                try:
                    self.object_id=int(self.object_id)
                except:
                    self.object_id=self.object_id.resolve(context)
                

            try:
                queryset=VisitEvent.objects.all()
                if self.object_id:
                    queryset=queryset.filter(property_fk=self.object_id)
                    property = Property.objects.get(id=self.object_id)

                if self.date:
                    queryset=queryset.filter(date_visit=self.date)
            except ObjectDoesNotExist:
                return []

            fullcalendar_options = {
                                    'monthNames': ['Janeiro','Fevereiro','Mar&ccedil;o','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
                                    'monthNamesShort': ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
                                    'dayNames': ['Domingo','Segunda','Ter&ccedil;a','Quarta','Quinta','Sexta','S&aacute;bado'],
                                    'dayNamesShort': ['Dom','Seg','Ter','Qua','Qui','Sex','S&aacute;b'],
                                    'buttonText': {
                                        'prev': '&nbsp;&#9668;&nbsp;',
                                        'next': '&nbsp;&#9658;&nbsp;',
                                        'prevYear': '&nbsp;&lt;&lt;&nbsp;',
                                        'nextYear': '&nbsp;&gt;&gt;&nbsp;',
                                        'today': 'Hoje',
                                        'month': 'M&ecirc;s',
                                        'week': 'Semana',
                                        'day': 'Dia'
                                    },      
                                    'titleFormat': {
                                        'month': 'MMMM yyyy',
                                        'week': "d [ yyyy]{ '&#8212;'[ MMM] d MMM yyyy}",
                                        'day': 'dddd, d MMM, yyyy'
                                    },
                                    'columnFormat': {
                                        'month': 'ddd',
                                        'week': 'ddd d/M',
                                        'day': 'dddd d/M'
                                    },
                                    'defaultView': self.display,
                                    'allDaySlot': 0,
                                    'slotMinutes':60,
                                    'axisFormat': 'H:mm',
                                    'timeFormat': {
                                        '': 'H:mm',
                                        'agenda': 'H:mm{ - H:mm}'
                                    },
            }

            if self.height:
                fullcalendar_options.update({'height': self.height})

            if self.headers:
                fullcalendar_options.update({
                    'header': {
                        'left': 'prev,next today',
                        'center': 'title',
                        'right': 'month,agendaWeek,agendaDay'
                    }
                });

            context.update({
                'show_events':self.events,
                'fullcalendar_options':mark_safe(fullcalendar_options),
                'property':property,
                'add_url':self.add_url,
                'admin':self.admin
            })
            
            context[self.var_name] = template.loader.get_template(
                    self.real_estate_node_template or [
                    "admin/visitcalendar/visitcalendar_list_%s_node.html" % self.display,
                    "admin/visitcalendar_list_%s_node.html" % self.display
                ]).render(context)
            return ''

def do_get_calendarvisitevent(parser, token):
        """
            This function tag can be called with this params:

                - Call default calendar:
                    {\% \get_calendarvisitevent as [varname] %}

                - Call default calendar where events are not displayed:
                    {\% \get_calendarvisitevent as [varname] no_show_events %}

                - Call calendar visit type of display like day week month:
                    {\% \get_calendarvisitevent display month as [varname] %}

                - Call calendar visit of especific property:
                    {\% \get_calendarvisitevent from [property_fk] date [date] as [varname] %}

                - Call calendar visit of especific day of property:
                    {\% \get_calendarvisitevent from [property_fk] date [date] as [varname] %}
        """
        bits = token.contents.split()
        params ={}

        for ct, bit in enumerate(bits):
            if bit == 'as':
                #{% get_calendarvisitevent as varname %}
                try:
                    params.update({'var_name':bits[ct+1]})
                except IndexError:
                    raise template.TemplateSyntaxError, "Varname argument to '%s' tag must be preceded 'as': %s as [varname]" % (bits[0], bits[0])

            if bit == 'from':
                #{% get_calendarvisitevent from [property_id] as varname %}
                #{% get_calendarvisitevent from [property_id] date [date] as [varname] %}
                try:
                    params.update({'object_id':bits[ct+1]})
                except IndexError:
                    raise template.TemplateSyntaxError, "Proprety object id argument to '%s' tag must be preceded 'from': %s from [property_id] as [varname]" % (bits[0], bits[0])

            if bit == 'display':
                #{% get_calendarvisitevent from [property_id] display [month|year|week|day] [date] as varname %}
                try:
                    if bits[ct+1] in ['day', 'month','week' ]:
                        params.update({'display':bits[ct+1]})
                    else:
                        raise template.TemplateSyntaxError, "Display arguments is only [day|week|month] to '%s'." % bits[0]
                except IndexError:
                    raise template.TemplateSyntaxError, "Display arguments [day|week|month] to '%s' tag must be preceded 'display': %s from [property_id] display [day|week|month] as [varname]" % (bits[0], bits[0])
            
            if bit == 'date':
                #{% get_calendarvisitevent from [property_id] date [date] as [varname] %}
                try:
                    params.update({'date':bits[ct+1]})
                except IndexError:
                    raise template.TemplateSyntaxError, "Date argument to '%s' tag must be preceded 'date': %s from [property_id] date [date] as [varname]" % (bits[0], bits[0])

            if bit == 'no_show_events':
                #{% get_calendarvisitevent [no_show_events] as varname %}
                params.update({'events':False})

            if bit == 'show_header':
                params.update({'headers':True})

            if bit == 'editable':
                if not params.has_key('admin'):
                    params.update({'editable':True})
                else:
                    raise template.TemplateSyntaxError, "Editable argument to '%s' tag can't used with admin argument." % bits[0]

            if bit == 'admin':
                if not params.has_key('editable'):
                    ## TODO: check user permission
                    params.update({'admin':True})
                else:
                    raise template.TemplateSyntaxError, "Admin argument to '%s' tag can't used with editable argument." % bits[0]

        return CalendarVisitEventNode(**params)


register.tag('get_calendarvisitevent',do_get_calendarvisitevent)
