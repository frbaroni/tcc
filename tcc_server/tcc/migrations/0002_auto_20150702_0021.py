# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estatisticas',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('horario', models.DateTimeField(auto_now=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=3)),
                ('sensor', models.ForeignKey(to='tcc.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(max_length=16)),
            ],
        ),
        migrations.RemoveField(
            model_name='dados',
            name='sensor',
        ),
        migrations.DeleteModel(
            name='Dados',
        ),
        migrations.AddField(
            model_name='estatisticas',
            name='tipo',
            field=models.ForeignKey(to='tcc.Tipo'),
        ),
    ]
