# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0007_auto_20151122_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='table',
            field=models.CharField(default=b'ty', max_length=2, choices=[(b'ty', b'Brunswick'), (b'wi', b'Gray Table'), (b'ka', b'Kaighn Table'), (b'me', b'Mehul/Adil/Bryan Table'), (b'lo', b'Loop Table'), (b're', b'Rectangle Table')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
