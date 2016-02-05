# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0016_auto_20160131_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eternalrejection',
            name='eternal_rejection',
            field=models.ForeignKey(to='IPT2016.Problem'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tacticalrejection',
            name='tactical_rejection',
            field=models.ForeignKey(to='IPT2016.Problem'),
            preserve_default=True,
        ),
    ]
