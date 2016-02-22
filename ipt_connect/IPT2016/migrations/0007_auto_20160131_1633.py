# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0006_auto_20160131_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='birthdate',
            field=models.DateField(default=1868),
            preserve_default=True,
        ),
    ]
