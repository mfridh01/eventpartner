# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_artikel_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pristyp',
            field=models.CharField(default='Standard', max_length=100),
        ),
    ]
