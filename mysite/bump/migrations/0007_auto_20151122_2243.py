# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0006_auto_20151122_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='advantage',
            field=models.CharField(default=b'', max_length=2, blank=True, choices=[(b'', b'Not Specified'), (b'bw', b'Break White'), (b'br', b'Break Red'), (b'hw', b'Hold White'), (b'hr', b'Hold Red')]),
        ),
        migrations.AlterField(
            model_name='game',
            name='finisher',
            field=models.CharField(default=b'', max_length=3, blank=True, choices=[(b'', b'Normal'), (b'bfg', b'Bump for Glory'), (b'jfg', b'Jump for Glory'), (b'nfg', b'New Age for Glory'), (b'swe', b'Sweep')]),
        ),
    ]
