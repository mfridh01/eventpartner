# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 19:56
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artikel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artikel_namn', models.CharField(max_length=100)),
                ('antal', models.IntegerField()),
                ('pris', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Kund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namn', models.CharField(max_length=100)),
                ('adress_gata', models.CharField(max_length=100)),
                ('adress_stad', models.CharField(max_length=50)),
                ('telefonnummer', models.CharField(max_length=15)),
                ('epost', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum_resning', models.DateField()),
                ('datum_rivning', models.DateField()),
                ('pristyp', models.CharField(max_length=100)),
                ('kund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Kund')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antal', models.IntegerField()),
                ('artikel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Artikel')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
            ],
        ),
    ]
