from django.contrib import admin
from real_estate_app.views.popup import popup_add, popup_edit_delete
from real_estate_app.views.ajax import ajax_view_model

def admin_urls_wrapper(urls):
	"""
		Wrapper AdminSite.get_urls to put the custom_urls
	"""
	def get_urls():
		from django.conf.urls.defaults import patterns, url, include
		custom_urls = patterns('',
								url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/add_popup/$',
									admin.site.admin_view(popup_add)
								),
								url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/add_popup/(?P<obj_id>\d+)/$',
									admin.site.admin_view(popup_edit_delete)
								),
								url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/ajax_view/$',
									admin.site.admin_view(ajax_view_model)
								),


		)
		return custom_urls + urls
	return get_urls

admin_urls = admin_urls_wrapper(admin.site.get_urls())
admin.site.get_urls = admin_urls 
admin.site.index_template='admin/index-custom.html'
