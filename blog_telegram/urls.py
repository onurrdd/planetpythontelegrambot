# -*- coding: utf8 -*-

from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('planet/', include('py_planet.urls', namespace='planet')),
]

#handler404 = 'myapp.views.custom_404'
