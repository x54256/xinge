# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-17 02:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='user_img',
            field=models.CharField(max_length=64),
        ),
    ]
