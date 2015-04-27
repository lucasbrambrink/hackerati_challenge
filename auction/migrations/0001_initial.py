# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'')),
                ('thumbnail', models.ImageField(null=True, upload_to=b'')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('reserved_price', models.DecimalField(max_digits=100, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bought_by', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(max_digits=100, decimal_places=2)),
                ('item', models.ForeignKey(related_name='item', to='auction.InventoryItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
