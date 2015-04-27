# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bid_log', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hours_duration', models.IntegerField()),
                ('sold_item', models.BooleanField(default=False)),
                ('current_price', models.DecimalField(null=True, max_digits=9, decimal_places=2)),
                ('starting_price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('end_price', models.DecimalField(null=True, max_digits=9, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=11, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(related_name='bids', to='auction.Auction')),
                ('user', models.ForeignKey(related_name='bids', to='base.HackeratiUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('reserved_price', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('auction', models.ForeignKey(related_name='purchase', to='auction.Auction')),
                ('item', models.ForeignKey(related_name='purchase', to='auction.InventoryItem')),
                ('user', models.ForeignKey(related_name='purchases', to='base.HackeratiUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='auction',
            name='item',
            field=models.ForeignKey(related_name='item', to='auction.InventoryItem'),
            preserve_default=True,
        ),
    ]
