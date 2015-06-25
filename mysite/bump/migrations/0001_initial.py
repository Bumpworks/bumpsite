# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name=b'Date Joined LeBump')),
                ('comments', models.CharField(max_length=500)),
                ('bumpForGlory', models.BooleanField(default=False)),
                ('sweep', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Player_text', models.CharField(max_length=60)),
                ('date_joined', models.DateTimeField(verbose_name=b'Date Joined LeBump')),
                ('email', models.CharField(default=b'', max_length=60)),
                ('phone', models.CharField(default=b'', max_length=60)),
                ('competitors', models.ManyToManyField(related_name='competitors_rel_+', to='bump.Player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(related_name='game_loser', default=2, to='bump.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(related_name='game_winner', default=1, to='bump.Player'),
        ),
    ]
