from django.contrib.admin import ModelAdmin
from django.contrib.admin import site
from real_estate_app.admin import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.propertys.models import Classification, StatusProperty, District, AditionalThings, \
								   					PositionOfSun
from property import PropertyAdmin

__all__=('PropertyAdmin',)


# autoregister admin Models
for model in [Classification, StatusProperty, District, AditionalThings, PositionOfSun]:
	site.register(model,RealEstateAppPopUpModelAdmin)

#site.index_template='admin/index-custom.html'