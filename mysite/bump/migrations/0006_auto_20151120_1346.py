# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0005_player_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='class_year',
            field=models.IntegerField(default=2016),
        ),
        migrations.AddField(
            model_name='player',
            name='duke',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AddField(
            model_name='player',
            name='last_name',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]
