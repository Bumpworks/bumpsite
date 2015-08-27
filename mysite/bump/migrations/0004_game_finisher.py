# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0003_auto_20150821_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='finisher',
            field=models.CharField(default=b'', max_length=3, choices=[(b'', b'Normal'), (b'bfg', b'Bump for Glory'), (b'jfg', b'Jump for Glory'), (b'nfg', b'New Age for Glory'), (b'swe', b'Sweep')]),
        ),
    ]
