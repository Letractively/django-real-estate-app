from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.urlresolvers import resolve 
from django.db.utils import DatabaseError
from django.http import Http404

from real_estate_app.apps.propertys.models import Property

from real_estate_app.apps.visitclick.models import Click, UntrackBoots, BannedIP
from real_estate_app.apps.visitclick.settings import CACHE_KEY_UNTRACK_UA, CACHE_KEY_BANED_IP, \
												     CACHE_TIME, VISIT_URLS_VIEW_CHECK_CLICK
from real_estate_app.apps.visitclick.utils import get_ip, find_user_agents, get_browser, get_os 

class UntrackedBootsMiddleware(object):

	def process_request(self,request):
		if request.is_ajax(): return 
		try:
			match=resolve(request.path)
			if match.url_name not in VISIT_URLS_VIEW_CHECK_CLICK: return
		except:
			return 

		ip = get_ip(request)
		boots = unicode(request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')

		untrack_boots = cache.get(CACHE_KEY_UNTRACK_UA)
		baned_ip = cache.get(CACHE_KEY_BANED_IP)

		if untrack_boots is None:
			untrack_boots = UntrackBoots.objects.all()
			cache.set(CACHE_KEY_UNTRACK_UA,untrack_boots,CACHE_TIME)

		for untrack in untrack_boots:
			if find_user_agents(boots,untrack.keyword):
				return 

		browser = get_browser(boots)
		browser = browser.family+' '+browser.version_string

		os = get_os(boots)
		os = os.family+' '+os.version_string
		property=Property.objects.get(id=1)

		attrs = {
			'url':request.path,
			'browser':browser,
			'user_agent':boots,
			'ip': ip,
			'operating_sistem':os,
			'content_visited':property, # do get request object
		}

		click=Click(**attrs)
		
		try:
			click.save()
		except DatabaseError:
			"""
				TODO: make a register file clicks and get this register and try to insert again.
			"""
			pass

class ClickMiddleware(UntrackedBootsMiddleware):

	def process_request(self,request):

		ips = cache.get(CACHE_KEY_BANED_IP)
		if ips is None:
			ips = BannedIP.objects.all()
			cache.set(CACHE_KEY_BANED_IP,ips,CACHE_TIME)

		if get_ip(request) in ips:
			raise Http404

		super(ClickMiddleware,self).process_request(request)