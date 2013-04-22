from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from real_estate_app.conf.settings import MEDIA_PREFIX
from real_estate_app.apps.portlets.models import Portlet

class PortletAdmin(admin.ModelAdmin):
	search_fields = ('title',)

	fieldsets = (
		(_('Portlet'), {
			'fields':['title','type_portlet'],
		}),
	)
	
	list_display = ('title','type_portlet')

	list_filter = ('type_portlet',)

	class Media:
		css = {
			'all':(
					MEDIA_PREFIX+"css/tabs.css",
			),
		}
		js = (
		      MEDIA_PREFIX+'js/jquery.createtabs.js',
		)

admin.site.register(Portlet,PortletAdmin)
