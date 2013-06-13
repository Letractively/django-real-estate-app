# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models  import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Click(models.Model):

	date = models.DateTimeField(
		_('Date clicked'),
		default=datetime.now()
	)

	url = models.CharField(
		_('URL'),
		max_length=255,
	)

	browser = models.CharField(
		_('Web browser'),
		max_length=100,
	)

	browser_version = models.CharField(
		_('Web browser version'),
		max_length=10,
	)
	operating_system = models.CharField(
		_('Operating Sistem'),
		max_length=100,
	)

	operating_system_version = models.CharField(
		_('Operating System version'),
		max_length=10,
	)

	user_agent = models.CharField(
		_('User agent'),
		max_length=255,
	)

	ip = models.IPAddressField(
		_('IP Address')
	)
	
	# content_type = models.ForeignKey(ContentType,null=True,blank=True)
	# object_id = models.BigIntegerField(null=True,blank=True)

	# content_visited = generic.GenericForeignKey('content_type', 'object_id')

	class Meta:
		app_label = 'visitclick'
		db_table  = 'real_estate_app_apps_visitclick_click'
		get_latest_by='date'
		ordering=('-date',)
		verbose_name=_('Click')
		verbose_name_plural=_('Clicks')

class UntrackBoots(models.Model):

	keyword = models.CharField(
		_('keyword'), 
		max_length=100, 
		help_text=_('Part or all of a user-agent string.  For example, "Googlebot" here will be found in "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" and that visitor will not be tracked.')
	)

	class Meta:
		app_label = 'visitclick'
		db_table  = 'real_estate_app_apps_visitclick_untrack_boots'
		ordering = ('keyword',)
		verbose_name = _('Untracked Boots')
		verbose_name_plural = _('Untracked Boots')

class BannedIP(models.Model):

	ip= models.IPAddressField(
		_('IP Address'), 
		help_text=_('The IP address that should be banned')
	)
	class Meta:
		app_label = 'visitclick'
		db_table  = 'real_estate_app_apps_visitclick_banned_ip'
		ordering = ('ip',)
		verbose_name = _('Baned IP')
		verbose_name_plural = _('Baned IPs')



