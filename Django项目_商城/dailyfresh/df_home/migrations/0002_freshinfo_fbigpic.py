# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-18 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='freshinfo',
            name='fbigpic',
            field=models.ImageField(default='fresh_info/goods_detail.jpg', upload_to='fresh_info_bigimg'),
        ),
    ]
