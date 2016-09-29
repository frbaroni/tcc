# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0007_auto_20150718_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('operador', models.CharField(max_length=1)),
                ('valor', models.FloatField()),
                ('dado', models.ForeignKey(to='tcc.Dado')),
                ('tipo', models.ForeignKey(to='tcc.Tipo')),
            ],
        ),
        migrations.CreateModel(
            name='AlertaConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('operador', models.CharField(max_length=1)),
                ('valor', models.FloatField()),
                ('tipo', models.ForeignKey(to='tcc.Tipo')),
            ],
        ),
    ]
