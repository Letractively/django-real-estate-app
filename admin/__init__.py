from django.contrib.admin import ModelAdmin
from django.contrib.admin import site
from options import *
from property import *
from flatpages import *
from files import *
from portlets import *
from realtor import *
from urls import *
from real_estate_app.models import Classification, StatusProperty, District, AditionalThings, \
								   PositionOfSun

# autoregister admin Models
for model in [Classification, StatusProperty, District, AditionalThings, PositionOfSun]:
	site.register(model,RealEstateAppPopUpModelAdmin)
