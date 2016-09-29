# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0008_alerta_alertaconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerta',
            name='horario',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 20, 20, 59, 16, 324863, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
