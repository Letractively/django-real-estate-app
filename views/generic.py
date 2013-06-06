from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic.create_update import redirect, apply_extra_context, get_model_and_form_class
from django.contrib.auth.views import redirect_to_login
from django.utils.translation import ugettext
from django.contrib import messages

from django.forms.models import ModelFormMetaclass, ModelForm
from django.views.generic import GenericViewError

def create_update_object(request, model=None, object_id=None,template_name=None,
                  template_loader=loader, extra_context=None, post_save_redirect=None,
                  login_required=False, context_processors=None, form_class=None , 
                  formset_class=None, initial_form={}, initial_formset={}):
    """
    Custom generic object-creation function.

    Templates: ``<app_label>/<model_name>_form.html``
    Context:
        form
            the form for the object
    """
    # TODO: Better this generic create_object
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = get_model_and_form_class(model, form_class)
    formset = formset_class
    try:
        instance=model.objects.get(id=object_id)
    except:
        instance=False

    if request.method == 'POST':

        form = form_class(request.POST, request.FILES)

        if form.is_valid() and not formset_class:
            if instance:
                form=form_class(request.POST, request.FILES, instance=instance)

            new_object = form.save()
            msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return redirect(post_save_redirect, new_object)
        else:
            formset = formset_class(request.POST, request.FILES)

            if instance:
                form = form_class(request.POST,request.FILES, instance=instance)

            if formset.is_valid() and form.is_valid():
                new_object=form.save()
                form_opts=new_object._meta
                obj=formset.save(commit=False)
                if hasattr(form_opts,'module_name') and hasattr(obj,form_opts.module_name+'_fk_id'):
                    setattr(obj,form_opts.module_name+'_fk',new_object)
                    formset.save()
                else:
                    raise Exception('Error the model %s must has a ForeignKey named %s_fk' % (obj._meta.module_name, form_opts.module_name) )

                msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                {"verbose_name": model._meta.verbose_name}
                messages.success(request, msg, fail_silently=True)
                return redirect(post_save_redirect, new_object)

    else:
        form = form_class(**initial_form)

        if formset_class:
            formset = formset_class(**initial_formset)


    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
        'formset':formset
    }, context_processors)
    apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))