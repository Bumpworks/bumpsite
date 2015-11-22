# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0005_player_netid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='netid',
            field=models.CharField(max_length=7, null=True, blank=True),
        ),
    ]
