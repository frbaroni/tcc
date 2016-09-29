"""tcc_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from . import services

urlpatterns = [
    url(r'^$', views.index),
    url(r'^sensores$', views.sensores),
    url(r'^graficos$', views.graficos),
    url(r'^mensagens$', views.mensagens),
    url(r'^configuracoes$', views.configuracoes),
    url(r'^sensor/(?P<sensorId>\d+)/inserir$', services.inserir),
    url(r'^sensor/(?P<sensorId>\d+)/ler$', services.ler),
    url(r'^sensor/(?P<sensorId>\d+)/ler/(?P<filtroMaximo>\d+)$', services.ler),
    url(r'^sensor/(?P<sensorId>\d+)/ler/(?P<tipo>\w+)/(?P<filtroMaximo>\d+)$', services.ler),
    url(r'^sensor/(?P<sensorId>\d+)/ler/(?P<filtroData>[0-9T:\-]+)$', services.ler),
    url(r'^sensor/(?P<sensorId>\d+)/ler/(?P<tipo>\w+)$', services.ler),
    url(r'^sensor/(?P<sensorId>\d+)/ler/(?P<tipo>\w+)/(?P<filtroData>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})$', services.ler),
    url(r'^sensor/(?P<sensorId>\d+)/historico$', services.historico),
    url(r'^sensor/(?P<sensorId>\d+)/historico/(?P<filtroMaximo>\d+)$', services.historico),
    url(r'^sensor/(?P<sensorId>\d+)/historico/(?P<tipo>\w+)/(?P<filtroMaximo>\d+)$', services.historico),
    url(r'^sensor/(?P<sensorId>\d+)/historico/(?P<filtroData>[0-9T:\-]+)$', services.historico),
    url(r'^sensor/(?P<sensorId>\d+)/historico/(?P<tipo>\w+)$', services.historico),
    url(r'^sensor/(?P<sensorId>\d+)/historico/(?P<tipo>\w+)/(?P<filtroData>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})$', services.historico),

]
