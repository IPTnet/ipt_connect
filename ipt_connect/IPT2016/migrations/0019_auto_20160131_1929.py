# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0018_auto_20160131_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eternalrejection',
            name='problem',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tacticalrejection',
            name='problem',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
