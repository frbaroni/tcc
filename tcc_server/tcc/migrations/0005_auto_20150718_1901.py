# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0004_auto_20150718_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dado',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('horario', models.DateTimeField(auto_now=True)),
                ('valor', models.DecimalField(max_digits=4, decimal_places=3)),
                ('sensor', models.ForeignKey(to='tcc.Sensor')),
                ('tipo', models.ForeignKey(to='tcc.Tipo')),
            ],
        ),
        migrations.RemoveField(
            model_name='estatisticas',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='estatisticas',
            name='tipo',
        ),
        migrations.DeleteModel(
            name='Estatisticas',
        ),
    ]
