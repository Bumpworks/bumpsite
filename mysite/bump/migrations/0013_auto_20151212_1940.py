# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0012_player_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='start_date',
            field=models.DateField(default=b'2015-12-01', blank=True),
        ),
    ]
