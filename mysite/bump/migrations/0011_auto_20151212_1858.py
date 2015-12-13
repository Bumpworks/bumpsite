# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0010_auto_20151212_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
