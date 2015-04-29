# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='HackeratiUser',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=50)),
                ('balance', models.DecimalField(max_digits=9, default=1000.0, decimal_places=2)),
                ('is_seller', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Auctioneer',
            fields=[
                ('hackeratiuser_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='base.HackeratiUser')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('base.hackeratiuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
