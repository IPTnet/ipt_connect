# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0012_auto_20160131_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicsfight',
            name='room_number',
            field=models.ForeignKey(to='IPT2016.Room'),
            preserve_default=True,
        ),
    ]
