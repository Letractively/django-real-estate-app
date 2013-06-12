from django.contrib.admin.util import lookup_field, display_for_field, label_for_field 
from django.contrib.admin.views.main import ALL_VAR, EMPTY_CHANGELIST_VALUE
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms.forms import pretty_name
from django.contrib.admin.templatetags.admin_list import result_hidden_fields, result_headers 
from django.utils.html import escape, conditional_escape 
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_unicode, force_unicode 
from django.template import Library

register = Library()

def items_for_result(cl, result, form,is_tag):
    """
    Generates the actual list of data.
    """
    first = True
    pk = cl.lookup_opts.pk.attname
    opts=cl.opts
    for field_name in cl.list_display:
        row_class = ''
        try:
            f, attr, value = lookup_field(field_name, result, cl.model_admin)
        except (AttributeError, ObjectDoesNotExist):
            result_repr = EMPTY_CHANGELIST_VALUE
        else:
            if f is None:
                allow_tags = getattr(attr, 'allow_tags', False)
                boolean = getattr(attr, 'boolean', False)
                if boolean:
                    allow_tags = True
                    result_repr = _boolean_icon(value)
                else:
                    result_repr = smart_unicode(value)
                # Strip HTML tags in the resulting text, except if the
                # function has an "allow_tags" attribute set to True.
                if not allow_tags:
                    result_repr = escape(result_repr)
                else:
                    result_repr = mark_safe(result_repr)
            else:
                if value is None:
                    result_repr = EMPTY_CHANGELIST_VALUE
                if isinstance(f.rel, models.ManyToOneRel):
                    result_repr = escape(getattr(result, f.name))
                else:
                    result_repr = display_for_field(value, f)
                if isinstance(f, models.DateField) or isinstance(f, models.TimeField):
                    row_class = ' class="nowrap"'
                if isinstance(f, models.DecimalField):
                    row_class = row_class+' alt="price"'

        if force_unicode(result_repr) == '':
            result_repr = mark_safe('&nbsp;')
        # If list_display_links not defined, add the link tag to the first field
        if (first and not cl.list_display_links) or field_name in cl.list_display_links:
            table_tag = {True:'td', False:'td'}[first]
            first = False
            url = cl.url_for_result(result)
            if is_tag: url = opts.app_label.lower()+'/'+opts.object_name.lower()+'/'+cl.url_for_result(result)
            if cl.is_popup:
                url+='?_popup=1'
            # Convert the pk to something that can be used in Javascript.
            # Problem cases are long ints (23L) and non-ASCII strings.
            if cl.to_field:
                attr = str(cl.to_field)
            else:
                attr = pk
            value = result.serializable_value(attr)
            result_id = repr(force_unicode(value))[1:]

            yield mark_safe(u'<%s%s><a href="%s"%s>%s</a></%s>' % \
                (table_tag, row_class, url, '', conditional_escape(result_repr), table_tag))
        else:
            # By default the fields come from ModelAdmin.list_editable, but if we pull
            # the fields out of the form instead of list_editable custom admins
            # can provide fields on a per request basis
            if form and field_name in form.fields:
                bf = form[field_name]
                result_repr = mark_safe(force_unicode(bf.errors) + force_unicode(bf))
            else:
                result_repr = conditional_escape(result_repr)
            yield mark_safe(u'<td%s>%s</td>' % (row_class, result_repr))
    if form and not form[cl.model._meta.pk.name].is_hidden:
        yield mark_safe(u'<td>%s</td>' % force_unicode(form[cl.model._meta.pk.name]))

def results(cl,is_tag):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield list(items_for_result(cl, res, form,is_tag))
    else:
        for res in cl.result_list:
            yield list(items_for_result(cl, res, None,is_tag))


def real_estate_app_result_list(cl,is_tag=False):
    """
        Custom result list can used with templatetags.
        cl = ChangeList
        is_tag = True or False, this is used to mount a url link.
    """
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': list(result_headers(cl)),
            'results': list(results(cl,is_tag))}
real_estate_app_result_list = register.inclusion_tag("admin/real_estate_app/change_list_results.html")(real_estate_app_result_list)
