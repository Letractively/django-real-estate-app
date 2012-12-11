from django.contrib.admin import ModelAdmin
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.db import models, transaction
from django.forms.models import (modelform_factory)
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.functional import curry
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect

from real_estate_app import widgets
from real_estate_app.conf.settings import MEDIA_PREFIX
from real_estate_app.utils import AutoCompleteObject

csrf_protect_m = method_decorator(csrf_protect)

class FaceBoxModelAdmin(ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        """  
        Hook for specifying the form Field instance for a given database Field
        instance.

        If kwargs are given, they're passed to the form Field's constructor.
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

    list_per_page=5
    def response_add(self, request, obj):
        super(RealEstateAppPopUpModelAdmin,self).response_add(request,obj)
        return HttpResponseRedirect('../view_popup/')

    def response_change(self,request,obj):
        super(RealEstateAppPopUpModelAdmin,self).response_change(request,obj)
        return HttpResponseRedirect('../view_popup/')

    def get_urls(self):

        from django.conf.urls.defaults import patterns, url

        urlpatterns = super(RealEstateAppPopUpModelAdmin,self).get_urls()

        info = self.model._meta.app_label, self.model._meta.module_name

        custom_urls = patterns('',
                                url(r'^add_popup/$',
                                    self.add_view_popup,
                                    name='%s_%s_add_popup' % info
                                ),
                                url(r'^edit_popup/(?P<obj_id>\d+)/$',
                                    self.change_view_popup,
                                    name='%s_%s_chage_popup' % info 
                                ),
                                url(r'^view_popup/$',
                                    self.changelist_view_popup,
                                    name='%s_%s_view_popup' % info
                                ),
                                url(r'^ajax_view/$',
                                    self.get_item_model_fk,
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
    def change_view_popup(self, request, obj_id=None, extra_context=None):
        return super(RealEstateAppPopUpModelAdmin,self).change_view(request, obj_id, extra_context={'is_popup':True,'notabs':True})

    @csrf_protect_m
    def changelist_view_popup(self, request, extra_context=None):
        return super(RealEstateAppPopUpModelAdmin,self).changelist_view(request, extra_context={'is_popup':True,'notabs':True})

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