# -*- coding: utf-8 -*-
from django.contrib.admin import site
from django.utils.translation import ugettext_lazy as _

from real_estate_app.admin import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.propertys.models import Classification, StatusProperty, District, AditionalThings, \
								   					PositionOfSun

class DistrictAdmin(RealEstateAppPopUpModelAdmin):
	fieldsets = (
			(_('General Information'), {
				'fields': ['district','state',],
			}),
	)

class ClassificationAdmin(RealEstateAppPopUpModelAdmin):
	fieldsets = (
			(_('General Information'), {
				'fields': ['classification',],
			}),
	)

class StatusPropertyAdmin(RealEstateAppPopUpModelAdmin):
	fieldsets = (
			(_('General Information'), {
				'fields': ['statusproperty',],
			}),
	)

class AditionalThingsAdmin(RealEstateAppPopUpModelAdmin):
	fieldsets = (
			(_('General Information'), {
				'fields': ['name',],
			}),
	)

class PositionOfSunAdmin(RealEstateAppPopUpModelAdmin):
	fieldsets = (
			(_('General Information'), {
				'fields': ['position',],
			}),
	)
site.register(District,DistrictAdmin)
site.register(Classification,ClassificationAdmin)
site.register(StatusProperty,StatusPropertyAdmin)
site.register(AditionalThings,AditionalThingsAdmin)
site.register(PositionOfSun,PositionOfSunAdmin)
