from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic.create_update import get_model_and_form_class, redirect, apply_extra_context
from django.contrib.auth.views import redirect_to_login
from django.utils.translation import ugettext
from django.contrib import messages

def create_object(request, model=None, template_name=None,
        template_loader=loader, extra_context=None, post_save_redirect=None,
        login_required=False, context_processors=None, form_class=None , initial={}):
    """
    Generic object-creation function.

    Templates: ``<app_label>/<model_name>_form.html``
    Context:
        form
            the form for the object
    """
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = get_model_and_form_class(model, form_class)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            new_object = form.save()
            if hasattr(new_object,'save_m2m'):
                new_object.save_m2m()

            msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return redirect(post_save_redirect, new_object)
    else:
        form = form_class(**initial)

    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    }, context_processors)
    apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))