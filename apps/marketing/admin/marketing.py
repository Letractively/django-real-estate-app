from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from real_estate_app.admin.options import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.marketing.models import MarketingObject
from real_estate_app.conf.settings import MEDIA_PREFIX

class MarketingObjectAdmin(RealEstateAppPopUpModelAdmin):

	search_fields=('title','description','files')

	fieldsets = (
		(_('Marketing'), {
			'fields':['title','description','files',],
		}),
		(_('Publish'),{
			'fields':['pub_date','pub_date_end','enable_publish',],
		})
	)

	list_display=('title','pub_date','pub_date_end','enable_publish',)

admin.site.register(MarketingObject, MarketingObjectAdmin)
