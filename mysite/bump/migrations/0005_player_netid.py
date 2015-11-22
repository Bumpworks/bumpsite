# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0004_auto_20151121_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='netid',
            field=models.CharField(max_length=7, null=True),
        ),
    ]
