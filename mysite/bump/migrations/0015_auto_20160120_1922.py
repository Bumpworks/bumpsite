# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bump', '0014_auto_20151212_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=75)),
                ('description', models.TextField()),
                ('points', models.IntegerField(default=0)),
                ('callback', models.TextField()),
                ('category', models.CharField(default=b'', max_length=2, choices=[(b'sg', b'Single Game Achievement'), (b'', b'No Category'), (b'mg', b'Multi Game Achievement')])),
            ],
        ),
        migrations.CreateModel(
            name='AchievementRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(related_name='achievementrecord', to='bump.Achievement')),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='finisher',
            field=models.CharField(default=b'', max_length=5, blank=True, choices=[(b'', b'Normal'), (b'sweep', b'Sweep'), (b'bfg', b'Bump for Glory'), (b'nfg', b'New Age for Glory'), (b'jfg', b'Jump for Glory'), (b'death', b'Death Ball')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='class_year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1970), django.core.validators.MaxValueValidator(2050)]),
        ),
        migrations.AddField(
            model_name='achievementrecord',
            name='player',
            field=models.ForeignKey(to='bump.Player'),
        ),
    ]
