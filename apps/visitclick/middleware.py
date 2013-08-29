from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.urlresolvers import resolve 
from django.db.utils import DatabaseError
from django.http import Http404
from django.middleware.common import CommonMiddleware

from real_estate_app.apps.propertys.models import Property

from real_estate_app.apps.visitclick.models import Click, UntrackBoots, BannedIP
from real_estate_app.apps.visitclick.settings import (CACHE_KEY_UNTRACK_UA, CACHE_KEY_BANED_IP, CACHE_TIME, VISIT_URLS_VIEW_CHECK_CLICK, 
													  CACHE_KEY_CONTENTTYPE, CACHE_TIME_CONTENTTYPE)
from real_estate_app.apps.visitclick.utils import get_ip, find_user_agents, get_browser, get_os 

class UntrackedBootsMiddleware(CommonMiddleware):

	def untrackedboots(self,request):
		boots = unicode(request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')

		untrack_boots = cache.get(CACHE_KEY_UNTRACK_UA)

		if untrack_boots is None:
			untrack_boots = UntrackBoots.objects.all()
			cache.set(CACHE_KEY_UNTRACK_UA,untrack_boots,CACHE_TIME)

		for untrack in untrack_boots:
			if find_user_agents(boots,untrack.keyword):
				return True
		return False

	def process_response(self,request,response):

		try:
			match=resolve(request.path)
			if (request.path not in VISIT_URLS_VIEW_CHECK_CLICK and match.url_name not in VISIT_URLS_VIEW_CHECK_CLICK) and \
			   (request.path not in VISIT_URLS_VIEW_CHECK_CLICK or match.url_name not in VISIT_URLS_VIEW_CHECK_CLICK): 
				return super(UntrackedBootsMiddleware,self).process_response(request,response)
		except:
			return super(UntrackedBootsMiddleware,self).process_response(request,response)

		if self.untrackedboots(request):
			return super(UntrackedBootsMiddleware,self).process_response(request,response)

		boots = unicode(request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')
		browser = get_browser(boots)
		os = get_os(boots)
		ip = get_ip(request)
		attrs = {
			'url':request.path,
			'browser':browser.family,
			'browser_version':browser.version_string,
			'user_agent':boots,
			'ip': ip,
			'operating_system':os.family,
			'operating_system_version':os.version_string,
		}

		content_type=response.get('X-Object-Type',False)
		object_id=response.get('X-Object-Id', False)

		if content_type and object_id:

			key_cache= CACHE_KEY_CONTENTTYPE + content_type
			cache_contenttype = cache.get(key_cache)

			if cache_contenttype is None:
				from django.contrib.contenttypes.models import ContentType
				app_label, model = content_type.split('.')
				cache_contenttype=ContentType.objects.get(app_label=app_label,model=model)
				cache.set(key_cache,cache_contenttype,CACHE_TIME_CONTENTTYPE)

			attrs.update({
				'object_id':object_id,
				'content_type':cache_contenttype
			})

		click=Click(**attrs)
		
		try:
			click.save()
		except DatabaseError:
			"""
				TODO: make a register file clicks and get this register and try to insert again.
			"""
			pass

		return super(UntrackedBootsMiddleware,self).process_response(request,response)

	def process_request(self,request):

		if request.is_ajax(): return 

		if self.untrackedboots(request):
			return



class ClickMiddleware(UntrackedBootsMiddleware):

	def process_request(self,request):

		baned_ips = cache.get(CACHE_KEY_BANED_IP)
		if baned_ips is None:
			baned_ips = BannedIP.objects.all()
			cache.set(CACHE_KEY_BANED_IP,baned_ips,CACHE_TIME)

		if get_ip(request) in baned_ips:
			raise Http404

		super(ClickMiddleware,self).process_request(request)