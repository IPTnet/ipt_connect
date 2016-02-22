# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0025_auto_20160131_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jurygrade',
            name='name',
        ),
        migrations.AddField(
            model_name='jurygrade',
            name='jury',
            field=models.CharField(default='Richard', max_length=50),
            preserve_default=False,
        ),
    ]
