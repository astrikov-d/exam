# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

from django import template

register = template.Library()

@register.filter
def meta(obj):
    return obj._meta