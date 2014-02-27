# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

from views import IndexView, MCreateView

urlpatterns = patterns('',
   url(r'^admin/', include(admin.site.urls)),
   url(r'^$', IndexView.as_view()),
   url(r'^create/$', MCreateView.as_view()),
   url(r'^get-model/(?P<model_name>\w+)/$', IndexView.as_view()),
)
