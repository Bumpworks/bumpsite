# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0015_auto_20160120_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievementrecord',
            name='achievement',
        ),
        migrations.RemoveField(
            model_name='achievementrecord',
            name='player',
        ),
        migrations.DeleteModel(
            name='AchievementRecord',
        ),
    ]
