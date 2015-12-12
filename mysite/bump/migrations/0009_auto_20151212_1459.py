# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0008_auto_20151208_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='elo',
            field=models.IntegerField(default=1000, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='losses',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='wins',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='finisher',
            field=models.CharField(default=b'', max_length=5, blank=True, choices=[(b'', b'Normal'), (b'bfg', b'Bump for Glory'), (b'jfg', b'Jump for Glory'), (b'nfg', b'New Age for Glory'), (b'sweep', b'Sweep')]),
        ),
    ]
