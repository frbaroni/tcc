# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0005_auto_20150718_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipo',
            name='id',
        ),
        migrations.AlterField(
            model_name='tipo',
            name='nome',
            field=models.CharField(serialize=False, max_length=16, primary_key=True),
        ),
    ]
