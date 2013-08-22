# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django import template
from django.conf import settings
from django.contrib.admin.templatetags.admin_list import result_hidden_fields
from django.contrib.admin.util import lookup_field, display_for_field, label_for_field 
from django.contrib.admin.views.main import ALL_VAR, EMPTY_CHANGELIST_VALUE
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms.forms import pretty_name
from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode, smart_unicode, force_unicode 
from django.utils.html import escape, conditional_escape 
from django.utils.safestring import mark_safe
from django.utils.translation import ungettext, ugettext as _

from real_estate_app.admin import site
from real_estate_app.apps.propertys.models import Property, District, StatusProperty
from real_estate_app.apps.photos.models import Photo

register = template.Library()

class PropertyWillExpiredNode(template.Node):
    def __init__(self, var_name, num=None):
            self.var_name= var_name

            if num:
                    self.num = int(num)
            else:
                    self.num = None

    def render(self,context):
            last_days = datetime.now()+timedelta(days=5)
            propertys = Property.objects.all_enabled().filter(models.Q(pub_date_end__lte=last_days))
            context[self.var_name] = propertys[:self.num]
            return ''

def do_get_property_expired(parser,token):
    bits = token.contents.split()

    if len(bits) == 4:
            if bits[2] != 'as':
                    raise template.TemplateSyntaxError, " Second argument to '%s' tag must be 'as'" % bits[0]
            return PropertyWillExpiredNode(num=bits[1], var_name=bits[3])

    elif len(bits)==3:
            if bits[1]!='as':
                    raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
            return PropertyWillExpiredNode(var_name=bits[2])
    else:
            raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])
                
class PropertyChageListAdminNode(template.Node):

    def __init__(self, var_name):
        self.var_name=var_name
        self.template='admin/propertys/templatetags/changelist_templatetags.html'

    def render(self,context):
        from django.contrib.admin.views.main import ERROR_FLAG
        
        PropertyAdmin = site._registry[Property]
        list_display = PropertyAdmin.list_display
        request = context.get('request')
        ChangeList = PropertyAdmin.get_changelist(request)
        opts = PropertyAdmin.model._meta
        app_label = opts.app_label
        actions = PropertyAdmin.get_actions(request)

        try:
            cl = ChangeList(request, PropertyAdmin.model, list_display, PropertyAdmin.list_display_links,
            PropertyAdmin.list_filter, PropertyAdmin.date_hierarchy, PropertyAdmin.search_fields,
            PropertyAdmin.list_select_related, PropertyAdmin.list_per_page, PropertyAdmin.list_editable, PropertyAdmin)
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET.keys():
                return render_to_response('admin/invalid_setup.html', {'title': _('Database error')})
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

        formset = cl.formset = None
        if cl.list_editable:
            FormSet = PropertyAdmin.get_changelist_formset(request)
            formset = cl.formset = FormSet(queryset=cl.result_list)

        if actions:
            action_form = PropertyAdmin.action_form(auto_id=None)
            action_form.fields['action'].choices = PropertyAdmin.get_action_choices(request)
        else:
            action_form = None

        selection_note_all = ungettext('%(total_count)s selected',
                                       'All %(total_count)s selected', cl.result_count)
        
        new_context = {
            'object_name':opts.object_name,
            'module_name': force_unicode(opts.verbose_name_plural),
            'selection_note': _('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
            'selection_note_all': selection_note_all % {'total_count': cl.result_count},
            'title': cl.title,
            'is_popup': cl.is_popup,
            'cl': cl,
            'has_add_permission': PropertyAdmin.has_add_permission(request),
            'has_change_permission':PropertyAdmin.has_change_permission(request),
            'root_path': PropertyAdmin.admin_site.root_path,
            'app_label': app_label,
            'action_form': action_form,
            'actions_on_top': PropertyAdmin.actions_on_top,
            'actions_on_bottom': PropertyAdmin.actions_on_bottom,
            'actions_selection_counter': PropertyAdmin.actions_selection_counter,
            'media':PropertyAdmin.media,
        }
        context.update(new_context or {})
        context[self.var_name]= template.loader.get_template(self.template).render(context)
        return ''

def do_get_property_chagelist_view(parser,token):
    bits = token.contents.split()
    if len(bits) == 3:
            if bits[1]!='as':
                    raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
            return PropertyChageListAdminNode(var_name=bits[2])

register.tag('get_property_will_expired',do_get_property_expired)
register.tag('get_property_chagelist_view',do_get_property_chagelist_view)