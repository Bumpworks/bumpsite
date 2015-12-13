# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0011_auto_20151212_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='start_date',
            field=models.DateField(default=b'2015-12-01'),
        ),
    ]
