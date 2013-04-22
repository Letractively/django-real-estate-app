from django.contrib.admin import ModelAdmin
from django.contrib.admin import site
from real_estate_app.admin import RealEstateAppPopUpModelAdmin
from real_estate_app.apps.propretys.models import Classification, StatusProprety, District, AditionalThings, \
								   					PositionOfSun
from proprety import PropretyAdmin

__all__=('PropretyAdmin',)


# autoregister admin Models
for model in [Classification, StatusProprety, District, AditionalThings, PositionOfSun]:
	site.register(model,RealEstateAppPopUpModelAdmin)

#site.index_template='admin/index-custom.html'