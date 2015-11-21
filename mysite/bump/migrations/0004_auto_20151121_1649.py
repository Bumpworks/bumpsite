# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0003_auto_20151121_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='class_year',
            field=models.IntegerField(),
        ),
    ]
