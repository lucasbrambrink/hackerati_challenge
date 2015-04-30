# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='HackeratiUser',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, parent_link=True, auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=9, default=1000.0)),
                ('is_seller', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Auctioneer',
            fields=[
                ('hackeratiuser_ptr', models.OneToOneField(to='base.HackeratiUser', parent_link=True, auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('base.hackeratiuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
