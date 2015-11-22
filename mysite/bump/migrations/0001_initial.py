# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('advantage', models.CharField(default=b'', max_length=2, choices=[(b'', b'Not Specified'), (b'bw', b'Break White'), (b'br', b'Break Red'), (b'hw', b'Hold White'), (b'hr', b'Hold Red')])),
                ('table', models.CharField(default=b'ty', max_length=2, choices=[(b'ty', b'Brunswick'), (b'wi', b'Gray Table'), (b'ka', b'Kaighn Table'), (b'me', b'Mehul/Adil/Bryan Table'), (b'lo', b'Loop Table')])),
                ('finisher', models.CharField(default=b'', max_length=3, choices=[(b'', b'Normal'), (b'bfg', b'Bump for Glory'), (b'jfg', b'Jump for Glory'), (b'nfg', b'New Age for Glory'), (b'swe', b'Sweep')])),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=30)),
                ('class_year', models.IntegerField()),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('duke', models.BooleanField(default=True)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(related_name='game_loser', default=2, to='bump.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='recorder',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(related_name='game_winner', default=1, to='bump.Player'),
        ),
    ]
