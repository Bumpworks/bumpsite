# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='bumpForGlory',
        ),
        migrations.RemoveField(
            model_name='game',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='game',
            name='sweep',
        ),
        migrations.RemoveField(
            model_name='player',
            name='Player_text',
        ),
        migrations.RemoveField(
            model_name='player',
            name='competitors',
        ),
        migrations.RemoveField(
            model_name='player',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='player',
            name='email',
        ),
        migrations.RemoveField(
            model_name='player',
            name='phone',
        ),
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]
