# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.text import capfirst, get_text_list

from real_estate_app.conf.settings import REAL_ESTATE_APP_MENU, REAL_ESTATE_APP_SETTINGS

register = template.Library()

class AppsMenuNode(template.Node):

	def __init__(self,var_name, menu_type='menu'):
		self.menu_type=menu_type
		self.var_name=var_name


	def render(self, context):

		from real_estate_app.admin.admin_site import site as real_site
		from django.contrib.admin.sites import site as admin_site

		if not real_site._registry.items():
			site = admin_site
		else:
			site = real_site

		app_dict = {}
		app_list = []
		request = context['request']
		user = request.user
		for model, model_admin in site._registry.items():
			app_label = model._meta.app_label
			has_module_perms = user.has_module_perms(app_label)
			if self.menu_type == 'menu':
				REAL_APPS = REAL_ESTATE_APP_MENU
			else:
				REAL_APPS = REAL_ESTATE_APP_SETTINGS

			if has_module_perms and app_label in REAL_APPS.keys():
				perms = model_admin.get_model_perms(request)
				try:
					if True in perms.values() and model.__name__.lower() in REAL_APPS[app_label]:
						model_dict = {
							'name': capfirst(model._meta.verbose_name_plural),
							'module_name':model.__name__.lower(),
							'admin_url': reverse('admin:index')+mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
							'perms': perms,
						}
						if app_label in app_dict:
							app_dict[app_label]['models'].append(model_dict)
						else:
							app_dict[app_label] = {
								'name': app_label.title(),
								'app_url': reverse('admin:index')+app_label + '/',
								'has_module_perms': has_module_perms,
								'models': [model_dict],
							}
				except KeyError:
					pass

			app_list = app_dict.values()
			app_list.sort(key=lambda x: x['name'])

			for app in app_list:
				app['models'].sort(key=lambda x: x['name'])

		context[self.var_name]=app_list

		return ''

def do_get_apps_menu(parser, token):

	bits = token.contents.split()
	"""
		{% get_apps_menu [menu_type] as [var_name] %}
		{% get_apps_menu as [var_name] %}
	"""
	if len(bits) == 4:
		if bits[2] != 'as':
			raise template.TemplateSyntaxError, " Second argument to '%s' tag must be 'as'" % bits[0]

		if bits[1] not in ('menu','settings'):
			raise template.TemplateSyntaxError, " First argument to '%s' tag must be 'menu' or 'settings' " % bits[0]

		return AppsMenuNode(menu_type=bits[1], var_name=bits[3])

	elif len(bits)==3:
		if bits[1]!='as':
			raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
		return AppsMenuNode(var_name=bits[2])
	else:
		raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname], or %s [menu_type] as [var_name]" % (bits[0],bits[0],bits[0])

register.tag('get_apps_menu', do_get_apps_menu)