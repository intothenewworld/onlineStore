# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-07 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180507_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'axf_shop',
            },
        ),
    ]
