# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0002_auto_20150702_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estatisticas',
            name='valor',
            field=models.DecimalField(decimal_places=3, max_digits=4),
        ),
    ]
