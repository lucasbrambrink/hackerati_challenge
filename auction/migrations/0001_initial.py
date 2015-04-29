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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('bid_log', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hours_duration', models.IntegerField()),
                ('sold_item', models.BooleanField(default=False)),
                ('current_price', models.DecimalField(max_digits=9, null=True, decimal_places=2)),
                ('starting_price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('end_price', models.DecimalField(max_digits=9, null=True, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('price', models.DecimalField(max_digits=11, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(to='auction.Auction', related_name='bids')),
                ('user', models.ForeignKey(to='base.HackeratiUser', related_name='bids')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('image', models.ImageField(upload_to='', null=True)),
                ('image_url', models.CharField(default='', max_length=600)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('reserved_price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('category', models.CharField(default='furniture', choices=[('furniture', 'Furniture'), ('electronics', 'Electronics'), ('jewelery', 'Jewelery'), ('music_instruments', 'Instruments'), ('tickets', 'Tickets')], max_length=50)),
                ('user', models.ForeignKey(to='base.HackeratiUser', related_name='item')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('auction', models.ForeignKey(to='auction.Auction', related_name='purchase')),
                ('item', models.ForeignKey(to='auction.InventoryItem', related_name='purchase')),
                ('user', models.ForeignKey(to='base.HackeratiUser', related_name='purchases')),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='item',
            field=models.ForeignKey(to='auction.InventoryItem', related_name='auction'),
        ),
        migrations.AddField(
            model_name='auction',
            name='user',
            field=models.ForeignKey(to='base.HackeratiUser', related_name='auction'),
        ),
    ]
