# -*- coding: utf-8; -*-
import operator

from django import template
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.admin import helpers
from django.contrib.admin.util import get_deleted_objects, model_ngettext
from django.db import router
from django.db.models import Q
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _

from real_estate_app.apps.propertys.models import Property
from real_estate_app.apps.realtors.models import Realtor
from real_estate_app.utils import format_link_callback

def duplicate_object(modeladmin,request,queryset):
	rows=[obj.clone() for obj in queryset]
	msg=_("Successfully duplicated %(count)d %(items)s") % {'count': len(rows), 'items': model_ngettext(modeladmin.opts,rows)} 
	modeladmin.message_user(request, msg)
duplicate_object.short_description=_("Duplicate selected %(verbose_name_plural)s")

def make_unpublished(modeladmin,request,queryset):
	rows=queryset.update(enable_publish=False)
	if rows == 1:
		msg=_("1 property was")
	else:
		msg=_("%s properties were") %rows 
	modeladmin.message_user(request,_("%s successfully marked unpublished.") %msg)

make_unpublished.short_description=_("Unpublish selected %(verbose_name_plural)s")

def make_published(modeladmin,request,queryset):
	rows=queryset.update(enable_publish=True)
	if rows == 1:
		msg=_("1 property was")
	else:
		msg=_("%s properties were") % rows
	modeladmin.message_user(request,_("%s successfully marked published.") % msg)
make_published.short_description=_("Publish selected %(verbose_name_plural)s")

def make_enabled(modeladmin,request,queryset):
    objs=queryset.update(logical_exclude=False)
    rows=objs
    msg=_("Successfully enabled %(count)d %(items)s.") % {"count": rows, "items": model_ngettext(modeladmin.opts, rows)}
    modeladmin.message_user(request, msg)
make_enabled.short_description=_("Enable selected %(verbose_name_plural)s")

def make_disabled(modeladmin,request,queryset):
    objs=queryset.update(logical_exclude=True)
    rows=objs
    msg=_("Successfully disabled %(count)d %(items)s.") % {"count": rows, "items": model_ngettext(modeladmin.opts, rows)}
    modeladmin.message_user(request, msg)
make_disabled.short_description=_("Disable selected %(verbose_name_plural)s")


def delete_selected_popup(modeladmin, request, queryset):
    """
    Default action which deletes the selected objects.

    This action first displays a confirmation page whichs shows all the
    deleteable objects, or, if the user has no permission one of the related
    childs (foreignkeys), a "permission denied" message.

    Next, it delets all selected objects and redirects back to the change list.
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label
    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    using = router.db_for_write(modeladmin.model)

    # Populate deletable_objects, a data structure of all related objects that
    # will also be deleted.
    deletable_objects, perms_needed, protected = get_deleted_objects(
        queryset, opts, request.user, modeladmin.admin_site, using)

    disabled_objects=[]

    # The user has already confirmed the deletion.
    # Do the deletion and return a None to display the change list view again.
    if request.POST.get('post'):
        query=[]
        d=0
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()

        if n:
            # TODO: create a custom get_delete_objects to put
            # all this validations.
            for obj in queryset:
                obj_display = force_unicode(obj)
                obj_fk = obj._meta.module_name+'_fk'
                obj_name=obj._meta.module_name

                try:
                    if hasattr(Property,obj_fk) and not isinstance(obj,Property):
                        Property.objects.get(**{obj_fk:obj.id})
                        query.append( Q(**{'id': obj.id}) )
                        modeladmin.log_change(request, obj,'%s' % _('Logical exclude object.'))
                except ObjectDoesNotExist:
                    modeladmin.log_deletion(request, obj, obj_display)
        
            # TODO: create a custom get_delete_objects to put
            # all this validations.
            # Exclude objects which has relation with Property to be deleted
            if query:
                # Distinct object to deleted and disabled
                disabled_objects=queryset.filter(reduce(operator.or_,query))
                deletable_objects=queryset.exclude(reduce(operator.or_, query))


                d=disabled_objects.count()
                n=deletable_objects.count()
                
                # Disable all object was relation with Property
                disabled_objects.update(logical_exclude=True)
            else:
                deletable_objects=queryset

            try:
                # Check if the instance is Realtor models because we have to delete
                # the django User models, when Realtor doesn't has active on Property
                if isinstance(queryset[0],Realtor):
                    for delete_obj in deletable_objects:
                        delete_obj.user.delete()
            except IndexError:
                raise

            deletable_objects.delete()

            if d >=1 and n >=1:
                msg= _("Successfully deleted %(count)d and disabled %(count_two)d %(items_two)s.") % {
                       "count": n, "items": model_ngettext(modeladmin.opts, n),
                       "count_two": d, "items_two": model_ngettext(modeladmin.opts, d)
                    }
            elif d >=1 and n ==0:
                msg= _("Successfully disebled %(count)d %(items)s.") % {
                       "count": d, "items": model_ngettext(modeladmin.opts, d)
                    }
            else:
                msg= _("Successfully deleted %(count)d %(items)s.") % {
                       "count": n, "items": model_ngettext(modeladmin.opts, n)
                    }

            modeladmin.message_user(request,msg)
        # Return None to display the change list page again.
        return None
    else:

        # Get all object in queryset and check if this object has foreingkey in Property
        # The way to use this delete you have to saw Realto models.
        query=[]
        for obj in queryset:
            obj_display = force_unicode(obj)
            obj_fk = obj._meta.module_name+'_fk'
            obj_name=obj._meta.module_name

            # TODO: create a custom get_delete_objects to put
            # all this validations.
            if hasattr(obj,'user') and isinstance(obj,Realtor):
                protected.append(format_link_callback(obj.user,modeladmin.admin_site))

            if hasattr(Property,obj_fk) and not isinstance(obj,Property):
                try:
                    Property.objects.get(**{obj_fk:obj.id})
                    query.append( Q(**{'id': obj.id}) )
                except ObjectDoesNotExist:
                    continue

        # TODO: create a custom get_delete_objects to put
        # all this validations.
        if query:
            disabled_objects=queryset.filter(reduce(operator.or_,query))
            deletable_objects=queryset.exclude(reduce(operator.or_, query))

            if disabled_objects:
                disabled_objects=[format_link_callback(obj,modeladmin.admin_site) for obj in disabled_objects]
            if deletable_objects:
                    deletable_objects=[format_link_callback(obj,modeladmin.admin_site) for obj in deletable_objects]


    if (len(deletable_objects) == 1):
        objects_name_delete = force_unicode(opts.verbose_name)
    else:
        objects_name_delete = force_unicode(opts.verbose_name_plural)

    if (disabled_objects and len(disabled_objects)==1):
        objects_name_disable = force_unicode(opts.verbose_name)
    elif disabled_objects:
        objects_name_disable = force_unicode(opts.verbose_name_plural)
    else:
        objects_name_disable = ''

    if perms_needed or protected:
        title = _("Cannot delete %(name)s") % {"name": objects_name_delete.lower()}
    else:
        title = _("Are you sure?")
    
    if deletable_objects:
        try:
            deletable_objects=[format_link_callback(obj,modeladmin.admin_site) for obj in deletable_objects]
        except:
            pass
    
    context = {
        "title": title,
        "objects_name_delete": objects_name_delete,
        "objects_name_disable": objects_name_disable,
        "deletable_objects": deletable_objects ,
        'queryset': queryset,
        "perms_lacking": perms_needed,
        "protected": protected,
        "opts": opts,
        "root_path": modeladmin.admin_site.root_path,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'is_popup': "_popup" in request.REQUEST or "pop" in request.REQUEST,
        'disabled_objects': disabled_objects,
        'queryset_obj_disabled':disabled_objects,
    }

    # Display the confirmation page
    return render_to_response(modeladmin.delete_selected_confirmation_template or [
        "admin/%s/%s/delete_selected_confirmation_popup.html" % (app_label, opts.object_name.lower()),
        "admin/%s/delete_selected_confirmation_popup.html" % app_label,
        "admin/delete_selected_confirmation_popup.html"
    ], context, context_instance=template.RequestContext(request))

delete_selected_popup.short_description = _("Delete selected %(verbose_name_plural)s")
