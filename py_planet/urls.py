# -*- coding: utf8 -*-

from django.urls import re_path, include, path

from .views import CommandReceiveView
from .views import simple_get_view

app_name = 'planet'
handler404 = 'planet.views.custom_404'

urlpatterns = [
    path('simple/', simple_get_view, name='simple_get'),
    re_path(r'^bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view(), name='command'),
]