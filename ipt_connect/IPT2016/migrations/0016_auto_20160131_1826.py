# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0015_auto_20160131_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eternalrejection',
            name='eternal_rejection',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
