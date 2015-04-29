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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('bid_log', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hours_duration', models.IntegerField()),
                ('sold_item', models.BooleanField(default=False)),
                ('current_price', models.DecimalField(null=True, max_digits=9, decimal_places=2)),
                ('starting_price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('end_price', models.DecimalField(null=True, max_digits=9, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('price', models.DecimalField(max_digits=11, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(related_name='bids', to='auction.Auction')),
                ('user', models.ForeignKey(related_name='bids', to='base.HackeratiUser')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('image_url', models.CharField(max_length=600, default='')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('reserved_price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('category', models.CharField(max_length=50, choices=[('furniture', 'Furniture'), ('electronics', 'Electronics'), ('jewelery', 'Jewelery'), ('music_instruments', 'Instruments'), ('tickets', 'Tickets')], default='furniture')),
                ('user', models.ForeignKey(related_name='item', to='base.HackeratiUser')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('auction', models.ForeignKey(related_name='purchase', to='auction.Auction')),
                ('item', models.ForeignKey(related_name='purchase', to='auction.InventoryItem')),
                ('user', models.ForeignKey(related_name='purchases', to='base.HackeratiUser')),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='item',
            field=models.ForeignKey(related_name='auction', to='auction.InventoryItem'),
        ),
        migrations.AddField(
            model_name='auction',
            name='user',
            field=models.ForeignKey(related_name='auction', to='base.HackeratiUser'),
        ),
    ]
