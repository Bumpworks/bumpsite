# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0007_player_identifier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='name',
        ),
        migrations.AlterField(
            model_name='player',
            name='identifier',
            field=models.CharField(max_length=30),
        ),
    ]
