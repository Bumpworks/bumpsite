# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0003_auto_20151121_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='recorder',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
