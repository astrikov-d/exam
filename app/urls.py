# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

from views import IndexView

urlpatterns = patterns('',
   url(r'^admin/', include(admin.site.urls)),
   url(r'^$', IndexView.as_view()),
)
