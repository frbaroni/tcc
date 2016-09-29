# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dados',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('submissao', models.DateTimeField(auto_now=True)),
                ('arTemp', models.DecimalField(decimal_places=2, max_digits=3)),
                ('arHumidade', models.DecimalField(decimal_places=2, max_digits=3)),
                ('terraTemp', models.DecimalField(decimal_places=2, max_digits=3)),
                ('terraHumidade', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=32)),
                ('desc', models.CharField(max_length=200)),
                ('ultimaAtualizacao', models.DateTimeField()),
                ('posicaoX', models.DecimalField(decimal_places=3, max_digits=8)),
                ('posicaoY', models.DecimalField(decimal_places=3, max_digits=8)),
            ],
        ),
        migrations.AddField(
            model_name='dados',
            name='sensor',
            field=models.ForeignKey(to='tcc.Sensor'),
        ),
    ]
