from django.contrib.admin import site
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class UserAdminReal(UserAdmin):

	def has_change_permission(self, request, obj=None):
		"""
			User can edit your own profile.
		"""
		if isinstance(obj,User) and obj.id == request.user.id:
			return True

		opts = self.opts
		return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())

site.unregister(User)
site.register(User,UserAdminReal)


