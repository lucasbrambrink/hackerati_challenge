# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='category',
            field=models.CharField(default=b'furniture', max_length=50, choices=[(b'furniture', b'Furniture'), (b'electronics', b'Electronics'), (b'jewelery', b'Jewelery'), (b'music_instruments', b'Instruments'), (b'tickets', b'Tickets')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='bid_log',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
