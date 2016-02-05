# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0003_auto_20160131_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='tourism',
            field=models.CharField(help_text=b'Would you like to stay some more days in Paris after the tournament? Please note the LOC would only book the rooms, not pay for it!', max_length=20, choices=[(b'TOURISM_0', b'No'), (b'TOURISM_1', b'Yes, one night'), (b'TOURISM_2', b'Yes, two nights')]),
            preserve_default=True,
        ),
    ]
