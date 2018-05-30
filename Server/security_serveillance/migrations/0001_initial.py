# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-26 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlertChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('alert_status', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AlertRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sms_record', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Snapshots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('picture', models.ImageField(upload_to='pictures')),
                ('detected_faces', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
