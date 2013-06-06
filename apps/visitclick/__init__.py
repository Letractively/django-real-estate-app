# -*- coding: utf-8 -*-
from signals import *

try:
	import user_agents
except ImportError:
	raise Exception("You need install python module user_agents.")
try:
	import qsstats
except ImportError:
	raise Exception("You need install python module django-qsstats-magic.")

