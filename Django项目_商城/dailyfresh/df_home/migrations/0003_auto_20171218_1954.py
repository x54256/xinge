# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-18 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_home', '0002_freshinfo_fbigpic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freshinfo',
            name='fbigpic',
            field=models.ImageField(upload_to='fresh_info_bigimg'),
        ),
    ]
