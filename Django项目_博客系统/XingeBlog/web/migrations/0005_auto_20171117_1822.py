# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-17 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_article_file_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='fabulous',
        ),
        migrations.RemoveField(
            model_name='article',
            name='file_path',
        ),
        migrations.RemoveField(
            model_name='article',
            name='opposition',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='creat_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
