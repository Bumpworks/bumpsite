# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0002_auto_20150815_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='advantage',
            field=models.CharField(default=b'', max_length=2, choices=[(b'', b'Not Specified'), (b'bw', b'Break White'), (b'br', b'Break Red'), (b'hw', b'Hold White'), (b'hr', b'Hold Red')]),
        ),
        migrations.AddField(
            model_name='game',
            name='table',
            field=models.CharField(default=b'ty', max_length=2, choices=[(b'ty', b'Brunswick'), (b'wi', b'Gray Table'), (b'ka', b'Kaighn Table'), (b'me', b'Mehul/Adil/Bryan Table'), (b'lo', b'Loop Table')]),
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
