# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-29 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pong', '0003_auto_20180329_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stack',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
