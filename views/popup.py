from django.conf import settings                          
from django.contrib.auth.decorators import login_required
from django.contrib.admin import site
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import PermissionDenied
from django.db.models import get_model
from django.forms.models import modelform_factory
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
from django import forms

from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode


@login_required
def popup_add(request, app_label, model_name, obj_id=None, paginate_by=5, 
			  page=None, allow_empty=True, extra_context=None):
	"""
		Foreign Keys content with facebox.
	"""
	message_404  = False	

	model = get_model(app_label, model_name)
	queryset = model.objects.all()

	paginator = Paginator(queryset, paginate_by, allow_empty_first_page=allow_empty)

	model_admin = site._registry.get(model)
	ModelForm = model_admin.get_form(request)

	if not model_admin.has_add_permission(request):
		raise PermissionDenied

	if request.method == 'POST':
		form =  ModelForm(request.POST)
		if form.is_valid():	
				new_obj = form.save()
				model_admin.log_addition(request, new_obj)
				model_admin.message_user(request, _("Sucessfully additioned."))
		try:
			if new_obj:
				form = ModelForm()
		except UnboundLocalError:
			model_admin.message_user(request, _("Ops... you try simething wrong"))
	else:
		form = ModelForm()


	if not page:
		page = request.GET.get('page',1)
	try:
		page_number = int(page)
	except ValueError:
		if page=='last':
			page_number = paginator.num_pages
		else:
			message_404 = _("Sorry, but the number of the page you request don't exist")

	try:
		page_obj = paginator.page(page_number)
	except InvalidPage:
		message_404 = _("Sorry, but the number of the page you request don't exist")
	
	if not message_404: 
		context = {
			'is_popup':True,
			'form':form,
			'results_list': page_obj.object_list,
			'paginator':paginator,
			'page_obj':page_obj,
			'is_paginated':page_obj.has_other_pages(),
			'results_per_page':paginator.per_page,
			'has_next':page_obj.has_next(),
			'has_previous':page_obj.has_previous(),
			'page':page_obj.number,
			'next':page_obj.next_page_number(),
			'previous':page_obj.previous_page_number(),
			'fist_on_page': page_obj.start_index(),
			'last_on_page': page_obj.end_index(),
			'pages':paginator.num_pages,
			'hits':paginator.count,
			'page_range':paginator.page_range,
			'app_label': app_label,
			'model_name':model_name,
		}
	else:
		context = { 'message_404': message_404, 'is_popup': True }
	
	return render_to_response('admin/real_estate_app/content_popup.html',
							   context,
							   context_instance=RequestContext(request)
			)
	 
@login_required
def popup_edit_delete(request, app_label, model_name, obj_id=None, paginate_by=5, 
			  page=None, allow_empty=True, extra_context=None):
	"""
		Foreign Keys content with facebox.
	"""
	from real_estate_app.models import Property

	message_404 = False	
	model = get_model(app_label, model_name)
	queryset = model.objects.all()

	paginator = Paginator(queryset, paginate_by, allow_empty_first_page=allow_empty)

	model_admin = site._registry.get(model)
	
	action = request.GET.get('action')

	if obj_id:
			obj = get_object_or_404(model, id=obj_id)
			ModelForm = model_admin.get_form(request, obj)
	else: 
		message_404 = _("Sorry, but the object you're requested didn't exist.")


	if action == 'delete' and model_admin.has_delete_permission(request, obj):
		obj_display = force_unicode(obj)
		# if exist and if is used, don't delete, just desactive the model
		if Property.objects.filter(id=obj.id):
			obj.logical_exclude=True
			obj.save()
		else:
			obj.delete()
		model_admin.log_deletion(request,obj, obj_display)
		model_admin.message_user(request, _("Sucessfully deleted."))
		return HttpResponseRedirect('../')

	elif not model_admin.has_delete_permission(request,obj):
		raise PermissionDenied
	elif not model_admin.has_change_permission(request,obj):
		raise PermissionDenied
	
	else:	
		
		if request.method == 'POST':
			form = ModelForm(request.POST, instance=obj) 	
			if form.is_valid():
					new_obj=form.save()
					msg_change = model_admin.construct_change_message(request,form, None)
					model_admin.log_change(request, new_obj, msg_change)
					model_admin.message_user(request, _("Sucessfully changed."))
			try:
				if new_obj:
					return HttpResponseRedirect('../')
			except UnboundLocalError:
				model_admin.message_user(request, _("Ops... you try simething wrong"))

		else:
			form = ModelForm(instance=obj)
			
	
	if not page:
		page = request.GET.get('page',1)
	
	try:
		page_number = int(page)
	except ValueError:
		if page=='last':
			page_number = paginator.num_pages
		else:
			message_404 = _("Sorry, but the number of the page you request don't exist")

	try:
		page_obj = paginator.page(page_number)
	except InvalidPage:
		message_404 = _("Sorry, but the number of the page you request don't exist")
	

	if not message_404: 
		context = {
			'is_popup':True,
			'form':form,
			'results_list': page_obj.object_list,
			'paginator':paginator,
			'page_obj':page_obj,
			'is_paginated':page_obj.has_other_pages(),
			'results_per_page':paginator.per_page,
			'has_next':page_obj.has_next(),
			'has_previous':page_obj.has_previous(),
			'page':page_obj.number,
			'next':page_obj.next_page_number(),
			'previous':page_obj.previous_page_number(),
			'fist_on_page': page_obj.start_index(),
			'last_on_page': page_obj.end_index(),
			'pages':paginator.num_pages,
			'hits':paginator.count,
			'page_range':paginator.page_range,
			'app_label': app_label,
			'model_name':model_name,
		}
	else:
		context = { 'message_404': message_404, 'is_popup': True }
	
	return render_to_response('admin/real_estate_app/content_popup.html',
							   context,
							   context_instance=RequestContext(request)
			)

