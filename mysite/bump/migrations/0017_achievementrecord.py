# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0016_auto_20160120_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='AchievementRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(related_name='achievementrecord', to='bump.Achievement')),
                ('player', models.ForeignKey(to='bump.Player')),
            ],
        ),
    ]
