# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20170215_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woojung',
            name='name',
            field=models.CharField(unique=True, max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='woojung_menu',
            name='day',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
