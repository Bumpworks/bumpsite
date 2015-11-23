# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bio',
            field=models.TextField(default=b''),
        ),
    ]
