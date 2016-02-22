# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0022_auto_20160131_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicsfight',
            name='opponent',
            field=models.ForeignKey(related_name='opponent_team', to='IPT2016.Team'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='physicsfight',
            name='reporter',
            field=models.ForeignKey(related_name='reporter_team', to='IPT2016.Team'),
            preserve_default=True,
        ),
    ]
