# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0002_auto_20151120_1456'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='name',
            new_name='identifier',
        ),
    ]
