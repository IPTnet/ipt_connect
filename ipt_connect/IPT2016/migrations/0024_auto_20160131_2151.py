# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0023_auto_20160131_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicsfight',
            name='reviewer',
            field=models.ForeignKey(related_name='reviewer_team', to='IPT2016.Team'),
            preserve_default=True,
        ),
    ]
