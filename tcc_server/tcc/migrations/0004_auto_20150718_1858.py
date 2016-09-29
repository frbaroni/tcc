# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0003_auto_20150702_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
