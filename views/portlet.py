from django.contrib.auth.decorators import permission_required
from django.views.generic.create_update import update_object, create_object

from real_estate_app.admin.forms import PortletAdminForm
from real_estate_app.models import Photo

@permission_required('real_estate_app.add_portlet',login_url='/admin/')
def portlet_create(request, *args, **kwargs):
	kwargs['form_class']=PortletAdminForm
	return create_object(request, *args, **kwargs)

@permission_required('real_estate_app.change_portlet',login_url='/admin/')
def portlet_edit(request, object_id=None, *args, **kwargs):
	kwargs['object_id']=object_id
	kwargs['form_class']=PortletAdminForm
	kwargs["post_save_redirect"]=request.path
	return update_object(request, *args, **kwargs)