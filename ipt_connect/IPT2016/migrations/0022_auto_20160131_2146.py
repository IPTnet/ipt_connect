# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0021_auto_20160131_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicsfight',
            name='reporter',
            field=models.ForeignKey(to='IPT2016.Team'),
            preserve_default=True,
        ),
    ]
