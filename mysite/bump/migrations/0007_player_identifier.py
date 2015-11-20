# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0006_auto_20151120_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='identifier',
            field=models.CharField(default=models.CharField(default=b'', max_length=30), max_length=30),
        ),
    ]
