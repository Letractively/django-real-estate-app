from django import template
from django.contrib.admin import ModelAdmin, helpers
from django.contrib.admin.util import unquote, get_deleted_objects
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.db import models, transaction, router
from django.forms.formsets import all_valid
from django.forms.models import (modelform_factory)
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.decorators import method_decorator
from django.utils.functional import curry, update_wrapper
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect

from real_estate_app import widgets
from real_estate_app.admin.actions import delete_selected_popup
from real_estate_app.conf.settings import MEDIA_PREFIX
from real_estate_app.utils import AutoCompleteObject

csrf_protect_m = method_decorator(csrf_protect)

class FaceBoxModelAdmin(ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        """  
        This is for create a widget FaceBoxFieldWrapper to add new itens on ModelAdmin.
        """
        request = kwargs.pop("request", None)

        # If the field specifies choices, we don't need to look for special
        # admin widgets - we just need to use a select widget of some kind.
        if db_field.choices:
            return self.formfield_for_choice_field(db_field, request, **kwargs)

        # ForeignKey or ManyToManyFields
        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            # Combine the field kwargs with any options for formfield_overrides.
            # Make sure the passed in **kwargs override anything in
            # formfield_overrides because **kwargs is more specific, and should
            # always win.
            if db_field.__class__ in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[db_field.__class__], **kwargs)

            # Get the correct formfield.
            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)
            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(db_field, request, **kwargs)

            # For non-raw_id fields, wrap the widget with a wrapper that adds
            # extra HTML -- the "add other" interface -- to the end of the
            # rendered output. formfield can be None if it came from a
            # OneToOneField with parent_link=True or a M2M intermediary.
            if formfield and db_field.name not in self.raw_id_fields:
                formfield.widget = widgets.FaceBoxFieldWrapper(formfield.widget, db_field.rel, self.admin_site)

            return formfield

        # If we've got overrides for the formfield defined, use 'em. **kwargs
        # passed to formfield_for_dbfield override the defaults.
        for klass in db_field.__class__.mro():
            if klass in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[klass], **kwargs)
                return db_field.formfield(**kwargs)

        # For any other type of field, just call its formfield() method.
        return db_field.formfield(**kwargs)

class RealEstateAppPopUpModelAdmin(FaceBoxModelAdmin):

    list_per_page=15

    actions=[delete_selected_popup,]

    def get_actions(self,request):
        actions = super(RealEstateAppPopUpModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def response_add(self, request, obj):
        super(RealEstateAppPopUpModelAdmin,self).response_add(request,obj)
        return HttpResponseRedirect('../../popup/')

    def response_change(self,request,obj):
        super(RealEstateAppPopUpModelAdmin,self).response_change(request,obj)
        return HttpResponseRedirect('../../popup/')

    def get_urls(self):

        from django.conf.urls.defaults import patterns, url

        urlpatterns = super(RealEstateAppPopUpModelAdmin,self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        custom_urls = patterns('',
                                url(r'^popup/add/$',
                                    wrap(self.add_view_popup),
                                    name='%s_%s_add_popup' % info
                                ),
                                url(r'^popup/(?P<object_id>\d+)/$',
                                    wrap(self.change_view_popup),
                                    name='%s_%s_chage_popup' % info 
                                ),
                                url(r'^popup/$',
                                    wrap(self.changelist_view_popup),
                                    name='%s_%s_view_popup' % info
                                ),
                                url(r'^popup/(?P<object_id>\d+)/delete/$',
                                    wrap(self.delete_view_popup),
                                    name='%s_%s_delete_popup' % info
                                ),
                                url(r'^popup/ajax/$',
                                    wrap(self.get_item_model_fk),
                                    name='%s_%s_ajax_view' % info
                                ),

        )

        return custom_urls + urlpatterns


    @csrf_protect_m
    @transaction.commit_on_success
    def add_view_popup(self, request, extra_context=None):
        return super(RealEstateAppPopUpModelAdmin,self).add_view(request,extra_context={'is_popup':True, 'notabs':True})

    @csrf_protect_m
    @transaction.commit_on_success
    def change_view_popup(self, request, object_id=None, extra_context=None):
        return super(RealEstateAppPopUpModelAdmin,self).change_view(request, object_id, extra_context={'is_popup':True,'notabs':True})

    @csrf_protect_m
    def changelist_view_popup(self, request, extra_context=None):
        return super(RealEstateAppPopUpModelAdmin,self).changelist_view(request, extra_context={'is_popup':True,'notabs':True})

    @csrf_protect_m
    @transaction.commit_on_success
    def delete_view_popup(self, request, object_id, extra_context=None):
        return super(RealEstateAppPopUpModelAdmin,self).delete_view(request,object_id, extra_context={'is_popup':True,'notabs':True})

    @csrf_protect_m 
    def get_item_model_fk(self, request, extra_context=None):
        """
        Ajax interation to construct the select options
        used a custom serialize how get some expecific fields.
        """
        q_value=''
        opts=self.model._meta

        model = self.model
        queryset = model.objects.all()
        module_name=opts.module_name
        fields = [i.name for i in model._meta.fields]

        if request.POST:
            if request.POST.items():
                for query in request.POST.items():
                    if 'csrfmiddlewaretoken' not in query:
                        query=dict((query,))
                        queryset=queryset.filter(**query)
        else:
            if 'term' in request.GET:
                q_value=request.GET['term']
                return HttpResponse(
                                    simplejson.dumps(
                                        AutoCompleteObject(model).render(value=q_value)
                                    )
                                    ,mimetype="text/javascript")
            else:
                fields = (fields[1],)

        json = serializers.serialize("json", queryset,fields=fields)
        return HttpResponse(json, mimetype="text/javascript")

    class Media:

        css = {
            'all':[
                MEDIA_PREFIX+"css/popup.css",
            ]
        }

        js = [
            "/admin-media/js/jquery.min.js",
            "/admin-media/js/jquery.init.js",
        ]

class RealEstateAppRevertInlineModelAdmin(RealEstateAppPopUpModelAdmin):

    def __init__(self, model, admin_site):
        """
            This is a custom init for create a revert inlines formsets.
        """
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        self.inline_instances = []
        for inline_class in self.revert_inlines:
            inline_instance = inline_class(self.revert_model, self.admin_site)
            self.inline_instances.append(inline_instance)
        if 'action_checkbox' not in self.list_display and self.actions is not None:
            self.list_display = ['action_checkbox'] +  list(self.list_display)
        if not self.list_display_links:
            for name in self.list_display:
                if name != 'action_checkbox':
                    self.list_display_links = [name]
                    break

        super(ModelAdmin,self).__init__()

    def get_form(self, request, obj=None, **kwargs):
        """
        Custom get_form function to returns a revert form class for use in the admin add view. 
        This is used by add_view and change_view.
        """
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        exclude.extend(kwargs.get("exclude", []))
        exclude.extend(self.get_readonly_fields(request, obj))
        # if exclude is an empty list we pass None to be consistant with the
        # default on modelform_factory
        exclude = exclude or None
        defaults = {
            "form": self.revert_form,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": curry(self.formfield_for_dbfield, request=request),
        }
        defaults.update(kwargs)
        return modelform_factory(self.revert_model, **defaults)
    @csrf_protect_m
    @transaction.commit_on_success
    def add_view_popup(self, request, extra_context=None):
        """
            Custom add_view_popup for revert_model, because self.model must be a self.revert_model
        """
        self.model = self.revert_model
        if isinstance(extra_context,dict):
            extra_context.update({'is_popup':True, 'notabs':True})
        else:
            extra_context={'is_popup':True, 'notabs':True}
        return super(RealEstateAppRevertInlineModelAdmin,self).add_view_popup(request,extra_context)

    @csrf_protect_m
    @transaction.commit_on_success
    def change_view_popup(self, request, object_id, extra_context=None):
        "The 'change' admin view for reverted model."
        model = self.model
        opts = model._meta
        if not extra_context :
            extra_context = {'is_popup':True}

        obj = self.get_object(request, unquote(object_id))
        
        revert_model_name = self.revert_model.__name__.lower()
        if hasattr(obj,revert_model_name):
            revert_obj = getattr(obj,revert_model_name)
            obj = revert_obj
        
        
        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url='../add/')

        ModelForm = self.get_form(request, obj)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, new_object),
                                       self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(request.POST, request.FILES,
                                  instance=new_object, prefix=prefix,
                                  queryset=inline.queryset(request))

                formsets.append(formset)

            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=True)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=True)

                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)

        else:
            form = ModelForm(instance=obj)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, obj), self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
            self.prepopulated_fields, self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media
        
        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': "_popup" in request.REQUEST,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)

    @csrf_protect_m
    @transaction.commit_on_success
    def delete_view_popup(self, request, object_id, extra_context=None):    
        "The 'delete' admin view for reverted model."
        opts = self.model._meta
        app_label = opts.app_label
        if not extra_context :
            extra_context = {'is_popup':True}
        obj = self.get_object(request, unquote(object_id))

        revert_model_name = self.revert_model.__name__.lower()
        if hasattr(obj,revert_model_name):
            revert_obj = getattr(obj,revert_model_name)
            obj = revert_obj

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        using = router.db_for_write(self.model)

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        (deleted_objects, perms_needed, protected) = get_deleted_objects(
            [obj], opts, request.user, self.admin_site, using)

        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_unicode(obj)
            self.log_deletion(request, obj, obj_display)
            self.delete_model(request, obj)

            self.message_user(request, _('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})

            if not self.has_change_permission(request, None):
                return HttpResponseRedirect("../../../../")
            return HttpResponseRedirect("../../")

        object_name = force_unicode(opts.verbose_name)

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {"name": object_name}
        else:
            title = _("Are you sure?")

        context = {
            "title": title,
            "object_name": object_name,
            "object": obj,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": opts,
            "root_path": self.admin_site.root_path,
            "app_label": app_label,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, context_instance=context_instance)