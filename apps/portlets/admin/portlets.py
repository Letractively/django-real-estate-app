from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.portlets.models import Portlet
from real_estate_app.conf.settings import MEDIA_PREFIX

class PortletAdmin(RealEstateAppPopUpModelAdmin):
	search_fields = ('title',)

	fieldsets = (
		(_('Portlet'), {
			'fields':['title','type_portlet','amount_featured'],
		}),
		(_('Publish'),{
			'fields':['pub_date','pub_date_end','enable_publish']
		})
	)
	
	list_display = ('title','type_portlet','amount_featured')

	list_filter = ('type_portlet',)


admin.site.register(Portlet,PortletAdmin)
