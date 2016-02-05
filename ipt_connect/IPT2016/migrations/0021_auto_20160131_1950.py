# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0020_auto_20160131_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eternalrejection',
            name='problem',
            field=models.ForeignKey(to='IPT2016.Problem'),
            preserve_default=True,
        ),
    ]
