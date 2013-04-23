# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.safestring import mark_safe

from real_estate_app.apps.newspapers.models import News

register = template.Library()

class NewsNode(template.Node):
        def __init__(self, var_name ,num=None):
                self.var_name=var_name

                if num:
                        self.num = int(num)
                else:
                        self.num = None

        def render(self, context):
                news = News.objects.all()

                context[self.var_name] = news[:self.num]
                return ''

def do_get_news(parser, token):

        bits = token.contents.split()

        if len(bits) == 4:
                if bits[2] != 'as':
                        raise template.TemplateSyntaxError, " Second argument to '%s' tag must be 'as'" % bits[0]
                return NewsNode(num=bits[1], var_name=bits[3])

        elif len(bits)==3:
                if bits[1]!='as':
                        raise template.TemplateSyntaxError, "Firts argument to '%s' tag must be 'as'" % bits[0]
                return NewsNode(var_name=bits[2])
        else:
                raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments: %s as [varname] %s [limit] as [varname]" % (bits[0],bits[0],bits[0])



register.tag('get_news',do_get_news)
