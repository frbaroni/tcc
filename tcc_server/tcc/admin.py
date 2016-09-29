from django.contrib import admin

from .models import Sensor, Tipo, Dado, Alerta, AlertaConfig

admin.site.register(Sensor)
admin.site.register(Tipo)
admin.site.register(Dado)
admin.site.register(Alerta)
admin.site.register(AlertaConfig)
# Register your models here.
