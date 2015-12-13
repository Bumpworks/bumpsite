# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0013_auto_20151212_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='start_date',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
    ]
