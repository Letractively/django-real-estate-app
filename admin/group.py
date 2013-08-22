from django.contrib.admin import site
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

from real_estate_app.admin.options import FaceBoxModelAdmin

class GroupAdminRealEstateApp(GroupAdmin,FaceBoxModelAdmin):
	pass

site.unregister(Group)
site.register(Group,GroupAdminRealEstateApp)