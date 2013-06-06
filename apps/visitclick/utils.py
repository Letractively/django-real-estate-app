# -*- coding: utf-8 -*-
import re
from user_agents import parse
from datetime import date, timedelta

IPv4_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
IPv6_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}')

def regex_ip(ip_address):
    try:
        return IPv4_RE.match(ip_address)
    except IndexError:
        return IPv6_RE.match(ip_address)
    else:
        return None

def get_ip(request):

    ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        ip_address = regex_ip(ip_address)
        if ip_address:
            ip_address = ip_address.group(0)
        else:
            ip_address = '192.168.0.1'

    return ip_address

def get_os(user_agent):
    try:
        return parse(user_agent).os
    except:
        os=''
        setattr(os,'family',"Can't detect Operating Sistem")
        setattr(os,'version_string',"0.0")
        return os

def get_browser(user_agent):
    try:
        return parse(user_agent).browser
    except:
        browser=''
        setattr(browser,'family',"Can't detect Browser")
        setattr(browser,'version_string',"0.0")
        return browser


def find_user_agents(user_agent,keyword):
    """
        True if a keyword is find in user_agent or user_agent is boot according 
        python module user_agent.
    """
    if user_agent.find(keyword) != -1:
        return True
    elif parse(user_agent).is_boot:
        return True
    return False

def get_first_dow(year, week):
    d = date(year, 1, 1)
    d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week - 1) * 7)
    return d + dlt