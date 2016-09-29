# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0006_auto_20150718_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dado',
            name='valor',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='posicaoX',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='posicaoY',
            field=models.FloatField(),
        ),
    ]
